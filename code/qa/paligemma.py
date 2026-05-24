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
from PIL import Image

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

_gpus = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == "--gpus" and i+1 < len(sys.argv)), None)
if _gpus:
    os.environ["CUDA_VISIBLE_DEVICES"] = _gpus

import torch
from transformers import PaliGemmaForConditionalGeneration, PaliGemmaProcessor
from transformers import logging as hf_logging
hf_logging.set_verbosity_error()

SUBSET_PATHS = {
    "augmented": "./data/qa/augmented",
    "human":     "./data/qa/human",
}

MODEL_IDS = {
    "p3b":  "google/paligemma2-3b-mix-448",
    "p10b": "google/paligemma2-10b-mix-448",
}

LANG_PROMPTS = {
    "hi": "प्रश्न का उत्तर किसी शब्द या वाक्यांश या अंकों में संख्या का उपयोग करके दें।",
    "de": "Beantworten Sie die Frage mit einem Wort, einer Phrase oder einer Zahl in Ziffern.",
    "ru": "Ответьте на вопрос словом, фразой или числом в цифрах.",
    "ro": "Răspundeți la întrebare folosind un cuvânt, o expresie sau un număr în cifre.",
    "en": "Answer the question using a word or phrase or a number in digits.",
}


def load_sample(folder: Path, lang: str):
    files = {f.name: f for f in folder.iterdir() if f.is_file()}

    if lang == "en":
        step_file = files.get("step1.json")
        img_file = next(
            (f for name, f in files.items()
             if name.endswith(".png") and name.split(".")[0].isdigit()),
            None,
        )
        if not step_file or not img_file:
            return None
        data = json.loads(step_file.read_text(encoding="utf-8"))
        return {
            "img_path": str(img_file),
            "query":    data["query"],
            "label":    data["label"],
        }
    else:
        step_file = files.get(f"{lang}_step2.json")
        img_file = next(
            (f for name, f in files.items()
             if name.startswith(f"ai-{lang}_") and name.endswith(".png")),
            None,
        )
        if not step_file or not img_file:
            return None
        data = json.loads(step_file.read_text(encoding="utf-8"))
        query = data.get("translated_query")
        label = data.get("translated_label") or data.get("tranlated_label")
        if not query or not label:
            return None
        return {
            "img_path": str(img_file),
            "query":    query,
            "label":    label,
        }


def compute_metric(gt: str, pred: str) -> bool:
    try:
        gt_f, pred_f = float(gt), float(pred)
        return abs(gt_f - pred_f) / abs(gt_f) <= 0.05
    except (ValueError, ZeroDivisionError):
        return str(gt).strip().lower() == str(pred).strip().lower()


def run_inference(model, processor, img_path: str, query: str, prompt_lang: str) -> str:
    prompt_text = f"{LANG_PROMPTS[prompt_lang]} {query}"
    image = Image.open(img_path).convert("RGB")

    inputs = processor(
        text=prompt_text,
        images=image,
        return_tensors="pt",
        padding="longest",
    ).to(model.device, dtype=model.dtype)

    input_len = inputs["input_ids"].shape[-1]
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False,
        )

    return processor.decode(outputs[0][input_len:], skip_special_tokens=True).strip()


def main():
    parser = argparse.ArgumentParser(description="Evaluate PaLiGemma 2 on ChartLingua QA")
    parser.add_argument("--model",  required=True, choices=["p3b", "p10b"])
    parser.add_argument("--subset", required=True, choices=["augmented", "human"])
    parser.add_argument("--lang",   required=True, choices=["hi", "de", "ru", "ro", "en"])
    parser.add_argument("--gpus",   required=True, help="CUDA_VISIBLE_DEVICES value, e.g. '0' or '0,1'")
    parser.add_argument("--prompt", choices=["lang", "eng"], default="lang",
                        help="'lang' uses the target language prompt; 'eng' always uses the English prompt")
    parser.add_argument("--max-samples",  type=int, default=None, help="limit to N samples for a dry run")
    parser.add_argument("--results-file", default="results.txt", help="shared file to append results to")
    args = parser.parse_args()

    model_id    = MODEL_IDS[args.model]
    parent_dir  = Path(SUBSET_PATHS[args.subset])
    prompt_lang = "en" if args.prompt == "eng" else args.lang

    print(f"model={model_id}  subset={args.subset}  lang={args.lang}  prompt={args.prompt}  gpus={args.gpus}")

    processor = PaliGemmaProcessor.from_pretrained(model_id)
    model = PaliGemmaForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
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
    skipped = 0

    for folder in tqdm(folders, desc=f"{args.model}/{args.subset}/{args.lang}"):
        sample = load_sample(folder, args.lang)
        if sample is None:
            skipped += 1
            continue

        pred = run_inference(model, processor, sample["img_path"], sample["query"], prompt_lang)
        predictions.append(pred)
        ground_truth.append(sample["label"])

    scores = [compute_metric(gt, pred) for gt, pred in zip(ground_truth, predictions)]
    acc = np.mean(scores) if scores else 0.0

    line = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"model={model_id} | subset={args.subset} | lang={args.lang} | "
        f"prompt={args.prompt} | acc={acc:.4f} | n={len(scores)} | skipped={skipped}"
    )
    print(f"\n{line}")
    with open(args.results_file, "a") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    main()
