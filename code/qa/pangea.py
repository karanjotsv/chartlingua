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
from typing import Dict

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
from llava.utils import disable_torch_init
from transformers import logging as hf_logging
hf_logging.set_verbosity_error()

SUBSET_PATHS = {
    "augmented": "./data/qa/augmented",
    "human":     "./data/qa/human",
}

MODEL_PATH = "neulab/Pangea-7B"
MODEL_NAME = "Pangea-7B-qwen"
MODEL_ID   = "neulab/Pangea-7B"

LANG_PROMPTS = {
    "hi": "प्रश्न का उत्तर किसी शब्द या वाक्यांश या अंकों में संख्या का उपयोग करके दें।",
    "de": "Beantworten Sie die Frage mit einem Wort, einer Phrase oder einer Zahl in Ziffern.",
    "ru": "Ответьте на вопрос словом, фразой или числом в цифрах.",
    "ro": "Răspundeți la întrebare folosind un cuvânt, o expresie sau un număr în cifre.",
    "en": "Answer the question using a word or phrase or a number in digits.",
}


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


def run_inference(model, tokenizer, image_processor, img_path: str, query: str, prompt_lang: str) -> str:
    prompt = f"<image>\n{LANG_PROMPTS[prompt_lang]} {query}"
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
    parser = argparse.ArgumentParser(description="Evaluate Pangea on ChartLingua QA")
    parser.add_argument("--subset", required=True, choices=["augmented", "human"])
    parser.add_argument("--lang",   required=True, choices=["hi", "de", "ru", "ro", "en"])
    parser.add_argument("--gpus",   required=True, help="CUDA_VISIBLE_DEVICES value, e.g. '0' or '0,1'")
    parser.add_argument("--prompt", choices=["lang", "eng"], default="lang",
                        help="'lang' uses the target language prompt; 'eng' always uses the English prompt")
    parser.add_argument("--max-samples",  type=int, default=None, help="limit to N samples for a dry run")
    parser.add_argument("--results-file", default="results.txt", help="shared file to append results to")
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
    skipped = 0

    for folder in tqdm(folders, desc=f"pangea/{args.subset}/{args.lang}"):
        sample = load_sample(folder, args.lang)
        if sample is None:
            skipped += 1
            continue

        pred = run_inference(model, tokenizer, image_processor, sample["img_path"], sample["query"], prompt_lang)
        predictions.append(pred)
        ground_truth.append(sample["label"])

    scores = [compute_metric(gt, pred) for gt, pred in zip(ground_truth, predictions)]
    acc = np.mean(scores) if scores else 0.0

    line = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"model={MODEL_ID} | subset={args.subset} | lang={args.lang} | "
        f"prompt={args.prompt} | acc={acc:.4f} | n={len(scores)} | skipped={skipped}"
    )
    print(f"\n{line}")
    with open(args.results_file, "a") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    main()
