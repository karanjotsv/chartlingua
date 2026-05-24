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
from typing import Dict, Optional

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

_gpus = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == "--gpus" and i+1 < len(sys.argv)), None)
if _gpus:
    os.environ["CUDA_VISIBLE_DEVICES"] = _gpus

import torch
import re
from PIL import Image
import cv2
import transformers
from llava.model.builder import load_pretrained_model
from llava.constants import IGNORE_INDEX, DEFAULT_IMAGE_TOKEN, IMAGE_TOKEN_INDEX
from transformers import logging as hf_logging
hf_logging.set_verbosity_error()

SUBSET_PATHS = {
    "val_p1": "./data/fv/val_p1",
    "val_p2": "./data/fv/val_p2",
}

MODEL_PATH = "neulab/Pangea-7B"
MODEL_NAME = "Pangea-7B-qwen"
MODEL_ID   = "neulab/Pangea-7B"

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


def preprocess_qwen(
    sources,
    tokenizer: transformers.PreTrainedTokenizer,
    has_image: bool = False,
    max_len: int = 2048,
    system_message: str = "You are a helpful assistant.",
) -> Dict:
    roles = {"human": "<|im_start|>user", "gpt": "<|im_start|>assistant"}
    im_start, im_end = tokenizer.additional_special_tokens_ids
    nl_tokens   = tokenizer("\n").input_ids
    _system     = tokenizer("system").input_ids + nl_tokens
    input_ids   = []
    source      = sources
    if roles[source[0]["from"]] != roles["human"]:
        source = source[1:]
    input_id, target = [], []
    system = [im_start] + _system + tokenizer(system_message).input_ids + [im_end] + nl_tokens
    input_id += system
    target   += [im_start] + [IGNORE_INDEX] * (len(system) - 3) + [im_end] + nl_tokens
    assert len(input_id) == len(target)
    for j, sentence in enumerate(source):
        role = roles[sentence["from"]]
        if has_image and sentence["value"] is not None and "<image>" in sentence["value"]:
            num_image = len(re.findall(DEFAULT_IMAGE_TOKEN, sentence["value"]))
            texts = sentence["value"].split("<image>")
            _input_id = tokenizer(role).input_ids + nl_tokens
            for i, text in enumerate(texts):
                _input_id += tokenizer(text).input_ids
                if i < len(texts) - 1:
                    _input_id += [IMAGE_TOKEN_INDEX] + nl_tokens
            _input_id += [im_end] + nl_tokens
            assert sum([i == IMAGE_TOKEN_INDEX for i in _input_id]) == num_image
        else:
            if sentence["value"] is None:
                _input_id = tokenizer(role).input_ids + nl_tokens
            else:
                _input_id = (
                    tokenizer(role).input_ids
                    + nl_tokens
                    + tokenizer(sentence["value"]).input_ids
                    + [im_end]
                    + nl_tokens
                )
        input_id += _input_id
    input_ids.append(input_id)
    return torch.tensor(input_ids, dtype=torch.long)


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


def run_inference(model, tokenizer, image_processor, img_path: str, claim: str, prompt_lang: str) -> str:
    prompt_text = LANG_PROMPTS[prompt_lang].format(claim=claim)
    prompt = f"<image>\n{prompt_text}"
    try:
        imm = Image.open(img_path).convert("RGB")
    except Exception:
        imm = cv2.imread(img_path)

    image_tensor = image_processor.preprocess(imm, return_tensors="pt")["pixel_values"]
    image_tensors = [image_tensor.half().cuda()]

    input_ids = preprocess_qwen(
        [{"from": "human", "value": prompt}, {"from": "gpt", "value": None}],
        tokenizer,
        has_image=True,
    ).cuda()

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensors,
            do_sample=False,
            temperature=0,
            num_beams=1,
            max_new_tokens=10,
            use_cache=True,
        )

    return tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()


def main():
    parser = argparse.ArgumentParser(description="Evaluate Pangea on ChartLingua FV")
    parser.add_argument("--subset", required=True, choices=["val_p1", "val_p2"])
    parser.add_argument("--lang",   required=True, choices=["en", "hi", "de", "ru", "ro", "pa", "el"])
    parser.add_argument("--gpus",   required=True, help="CUDA_VISIBLE_DEVICES value, e.g. '0' or '0,1'")
    parser.add_argument("--prompt", choices=["lang", "eng"], default="eng",
                        help="'lang' uses the target language prompt; 'eng' always uses the English prompt")
    parser.add_argument("--max-samples",  type=int, default=None, help="limit to N samples for a dry run")
    parser.add_argument("--results-file", default="results_fv.txt", help="shared file to append results to")
    args = parser.parse_args()

    parent_dir  = Path(SUBSET_PATHS[args.subset])
    prompt_lang = "en" if args.prompt == "eng" else args.lang

    print(f"model={MODEL_ID}  subset={args.subset}  lang={args.lang}  prompt={args.prompt}  gpus={args.gpus}")

    tokenizer, model, image_processor, _ = load_pretrained_model(
        MODEL_PATH, None, MODEL_NAME, multimodal=True, attn_implementation="sdpa"
    )

    folders = sorted(
        [p for p in parent_dir.iterdir() if p.is_dir() and p.name.isdigit()],
        key=lambda p: int(p.name),
    )
    if args.max_samples:
        folders = folders[:args.max_samples]

    ground_truth, predictions = [], []
    skipped = garbage = 0

    for folder in tqdm(folders, desc=f"pangea/{args.subset}/{args.lang}"):
        sample = load_sample(folder, args.lang)
        if sample is None:
            skipped += 1
            continue

        pred_text = run_inference(model, tokenizer, image_processor, sample["img_path"], sample["claim"], prompt_lang)
        pred = parse_prediction(pred_text)

        if pred is None:
            garbage += 1
            pred = 1 - sample["label"]  # penalise: count as wrong

        predictions.append(pred)
        ground_truth.append(sample["label"])

    acc, f1 = compute_scores(ground_truth, predictions)

    line = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"model={MODEL_ID} | subset={args.subset} | lang={args.lang} | "
        f"prompt={args.prompt} | acc={acc:.4f} | f1={f1:.4f} | "
        f"n={len(predictions)} | skipped={skipped} | garbage={garbage}"
    )
    print(f"\n{line}")
    with open(args.results_file, "a") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    main()
