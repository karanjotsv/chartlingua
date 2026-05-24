import sys
import os
import json
import warnings
import logging
import argparse
import numpy as np
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
from typing import Optional

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

_gpus = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == "--gpus" and i+1 < len(sys.argv)), None)
if _gpus:
    os.environ["CUDA_VISIBLE_DEVICES"] = _gpus

import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
from transformers import logging as hf_logging
hf_logging.set_verbosity_error()

SUBSET_PATHS = {
    "val_p1": "./data/fv/val_p1",
    "val_p2": "./data/fv/val_p2",
}

MODEL_IDS = {
    "g2b": "google/gemma-4-E2B-it",
    "g4b": "google/gemma-4-E4B-it",
}

LANG_PROMPTS = {
    "en": "Is the following claim supported by the chart? Answer either supports or refutes. Do not generate additional explanation. Claim: {claim}, Answer:",
    "hi": "क्या निम्नलिखित दावा चार्ट द्वारा समर्थित है? supports या refutes में उत्तर दें। अतिरिक्त स्पष्टीकरण न दें। दावा: {claim}, उत्तर:",
    "de": "Wird die folgende Behauptung durch das Diagramm gestützt? Antworten Sie entweder mit supports oder refutes. Keine zusätzliche Erklärung. Behauptung: {claim}, Antwort:",
    "ru": "Подтверждается ли следующее утверждение графиком? Ответьте либо supports, либо refutes. Без дополнительных объяснений. Утверждение: {claim}, Ответ:",
    "ro": "Este susținută de grafic afirmația de mai jos? Răspundeți cu supports sau refutes. Fără explicații suplimentare. Afirmație: {claim}, Răspuns:",
    "pa": "ਕੀ ਹੇਠਾਂ ਦਿੱਤਾ ਦਾਅਵਾ ਚਾਰਟ ਦੁਆਰਾ ਸਮਰਥਿਤ ਹੈ? supports ਜਾਂ refutes ਵਿੱਚ ਜਵਾਬ ਦਿਓ। ਵਾਧੂ ਵਿਆਖਿਆ ਨਾ ਦਿਓ। ਦਾਅਵਾ: {claim}, ਜਵਾਬ:",
    "el": "Υποστηρίζεται ο παρακάτω ισχυρισμός από το γράφημα; Απαντήστε με supports ή refutes. Χωρίς πρόσθετες εξηγήσεις. Ισχυρισμός: {claim}, Απάντηση:",
}

REFUTE_KEYWORDS = [
    "refutes", "refute", "refuted",
    "verwerfen", "widerlegt",
    "नहीं", "रद्द करें", "असत्य",
    "опровергает", "не поддерживает",
]
SUPPORT_KEYWORDS = [
    "supports", "support", "supported",
    "unterstützt",
    "suporta", "suport", "susțin", "susține",
    "सहायक", "सत्य", "समर्थित", "सहायता", "सही है",
    "поддерживает", "подтверждает",
]


def load_sample(folder: Path, lang: str) -> Optional[dict]:
    files = {f.name: f for f in folder.iterdir() if f.is_file()}
    fid = folder.name

    gt_file = files.get("step1.json")
    if not gt_file:
        return None
    gt = json.loads(gt_file.read_text(encoding="utf-8"))
    label = 1 if gt["label"] else 0

    if lang == "en":
        img_file = files.get(f"ai-{fid}.png")
        if not img_file:
            return None
        return {"img_path": str(img_file), "claim": gt["claim"], "label": label}
    else:
        step_file = files.get(f"{lang}_step2.json")
        img_file = files.get(f"ai-{lang}_{fid}.png")
        if not step_file or not img_file:
            return None
        data = json.loads(step_file.read_text(encoding="utf-8"))
        claim = data.get("translated_claim") or data.get("claim")
        if not claim:
            return None
        return {"img_path": str(img_file), "claim": claim, "label": label}


def parse_prediction(text: str) -> Optional[int]:
    t = text.lower()
    for kw in REFUTE_KEYWORDS:
        if kw.lower() in t:
            return 0
    for kw in SUPPORT_KEYWORDS:
        if kw.lower() in t:
            return 1
    first = t.strip().split()[0].rstrip(".,!?") if t.strip() else ""
    if first == "yes":
        return 1
    if first == "no":
        return 0
    return None


def compute_scores(labels, preds):
    if not preds:
        return 0.0, 0.0
    acc = float(np.mean([p == g for p, g in zip(preds, labels)]))
    tp = sum(p == 1 and g == 1 for p, g in zip(preds, labels))
    fp = sum(p == 1 and g == 0 for p, g in zip(preds, labels))
    fn = sum(p == 0 and g == 1 for p, g in zip(preds, labels))
    tn = sum(p == 0 and g == 0 for p, g in zip(preds, labels))
    p1 = tp / (tp + fp) if tp + fp else 0.0
    r1 = tp / (tp + fn) if tp + fn else 0.0
    f1_pos = 2 * p1 * r1 / (p1 + r1) if p1 + r1 else 0.0
    p0 = tn / (tn + fn) if tn + fn else 0.0
    r0 = tn / (tn + fp) if tn + fp else 0.0
    f1_neg = 2 * p0 * r0 / (p0 + r0) if p0 + r0 else 0.0
    return acc, (f1_pos + f1_neg) / 2


def run_inference(model, processor, img_path: str, claim: str, prompt_lang: str) -> str:
    prompt_text = LANG_PROMPTS[prompt_lang].format(claim=claim)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": str(Path(img_path).resolve())},
                {"type": "text",  "text": prompt_text},
            ],
        }
    ]
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    input_len = inputs["input_ids"].shape[-1]
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False,
            pad_token_id=processor.tokenizer.eos_token_id,
        )

    return processor.decode(outputs[0][input_len:], skip_special_tokens=True).strip()


def main():
    parser = argparse.ArgumentParser(description="Evaluate Gemma 4 on ChartLingua FV")
    parser.add_argument("--model",  required=True, choices=["g2b", "g4b"])
    parser.add_argument("--subset", required=True, choices=["val_p1", "val_p2"])
    parser.add_argument("--lang",   required=True, choices=["en", "hi", "de", "ru", "ro", "pa", "el"])
    parser.add_argument("--gpus",   required=True, help="CUDA_VISIBLE_DEVICES value, e.g. '0' or '0,1'")
    parser.add_argument("--prompt", choices=["lang", "eng"], default="eng",
                        help="'lang' uses the target language prompt; 'eng' always uses the English prompt")
    parser.add_argument("--max-samples",  type=int, default=None, help="limit to N samples for a dry run")
    parser.add_argument("--results-file", default="results_fv.txt", help="shared file to append results to")
    args = parser.parse_args()

    model_id    = MODEL_IDS[args.model]
    parent_dir  = Path(SUBSET_PATHS[args.subset])
    prompt_lang = "en" if args.prompt == "eng" else args.lang

    print(f"model={model_id}  subset={args.subset}  lang={args.lang}  prompt={args.prompt}  gpus={args.gpus}")

    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForImageTextToText.from_pretrained(
        model_id,
        dtype="auto",
        device_map="auto",
    )
    model.eval()

    folders = sorted(
        [p for p in parent_dir.iterdir() if p.is_dir() and p.name.isdigit()],
        key=lambda p: int(p.name),
    )
    if args.max_samples:
        folders = folders[:args.max_samples]

    ground_truth, predictions = [], []
    skipped = garbage = 0

    for folder in tqdm(folders, desc=f"{args.model}/{args.subset}/{args.lang}"):
        sample = load_sample(folder, args.lang)
        if sample is None:
            skipped += 1
            continue

        pred_text = run_inference(model, processor, sample["img_path"], sample["claim"], prompt_lang)
        pred = parse_prediction(pred_text)

        if pred is None:
            garbage += 1
            pred = 1 - sample["label"]  # penalise: count as wrong

        predictions.append(pred)
        ground_truth.append(sample["label"])

    acc, f1 = compute_scores(ground_truth, predictions)

    line = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"model={model_id} | subset={args.subset} | lang={args.lang} | "
        f"prompt={args.prompt} | acc={acc:.4f} | f1={f1:.4f} | "
        f"n={len(predictions)} | skipped={skipped} | garbage={garbage}"
    )
    print(f"\n{line}")
    with open(args.results_file, "a") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    main()
