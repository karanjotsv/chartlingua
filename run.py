import os
import json
import logging
import requests
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from config import *
from pipe import Gemini, Qwen, Gemma

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log", mode="a"),
        logging.StreamHandler(),
    ],
)

# step 1 supported by gemini only
if BACKEND_STEP1 == "gemini":
    pipeline_s1 = Gemini(api_key=API_KEY, model_id=MODEL_ID, logger=logging)
else:
    raise ValueError(f"BACKEND_STEP1='{BACKEND_STEP1}' not supported. Step 1 requires Gemini.")

# step 2 supported by gemini, qwen or gemma
if BACKEND_STEP2 == "qwen":
    pipeline_s2 = Qwen(model_path=QWEN_MODEL_PATH, logger=logging, max_new_tokens=QWEN_MAX_NEW_TOKENS)
elif BACKEND_STEP2 == "gemma":
    pipeline_s2 = Gemma(model_path=GEMMA_MODEL_PATH, logger=logging, max_new_tokens=GEMMA_MAX_NEW_TOKENS)
elif BACKEND_STEP2 == "gemini":
    # reuse the same gemini instance - no double initialisation
    pipeline_s2 = pipeline_s1
else:
    raise ValueError(f"BACKEND_STEP2='{BACKEND_STEP2}' not supported. Use 'gemini', 'qwen' or 'gemma'.")


def run_step1(cid):
    res = {}
    row = add_data[cid]

    cdir = cid
    img = [file.name for file in Path(f"{base_folder}/{cdir}").iterdir() if file.name.startswith(str(cid))][0]
    ipath = f"{base_folder}/{cdir}/{img}"

    jpath, cpath = pipeline_s1.extract_chart(img_path=ipath, img_desc=row[0])

    os.chdir(f"{base_folder}/{cid}")
    os.system(f"{ld_preload} python {cpath.split('/')[-1]} {jpath.split('/')[-1]}")
    os.chdir("../" * 3)

    vres = pipeline_s1.check_chart()
    res["chart_check"] = vres

    cres = pipeline_s1.check_task(task='fv', claim=row[1])
    res["claim_check"] = cres
    res["claim"] = row[1]
    res["label"] = row[2]

    with open(f"{base_folder}/{cid}/step1.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


def run_step2(cid, translation_metadata, task):
    res = {}
    row = add_data[cid]

    cdir = cid
    img = [file.name for file in Path(f"{base_folder}/{cdir}").iterdir() if file.name.startswith(str(cid))][0]
    ipath = f"{base_folder}/{cdir}/{img}"
    
    tclaim, tchart, jpath = pipeline_s2.translate(
        img_path=ipath,
        claim=row[1],
        lang_meta=translation_metadata,
        task=task,
    )

    chart_eval, claim_eval = pipeline_s2.check_translation(
        lang_meta=translation_metadata,
        task=task,
    )

    res["claim_check"] = claim_eval
    res["chart_check"] = chart_eval
    res["claim"] = row[1]
    res["translated_claim"] = tclaim

    os.chdir(f"{base_folder}/{cid}")
    os.system(f"{ld_preload} python ai-{cid}.py {jpath.split('/')[-1]}")
    os.chdir("../" * 3)

    with open(
        f"{base_folder}/{cid}/{translation_metadata['target_language_code']}_step2.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    ###
    df = pd.read_csv("./fv/test_p2.csv")
    base_folder = "./fv/val_p2"

    os.makedirs(base_folder, exist_ok=True)

    logging.info(f"DOWNLOAD CHARTS: {download}")
    logging.info(f"BACKEND_STEP1: {BACKEND_STEP1} | BACKEND_STEP2: {BACKEND_STEP2}")

    add_data = {}
    for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
        image_url = row["CHART_IMAGE"]
        add_data[idx] = [row["CAPTION"], row["CLAIM"], row["LABEL"]]

        if download:
            try:
                response = requests.get(image_url, timeout=5)
                ext = image_url.split(".")[-1].split("?")[0]
                sub_folder = os.path.join(base_folder, str(idx))
                os.makedirs(sub_folder, exist_ok=True)

                filename = f"{idx}.{ext}"
                file_path = os.path.join(sub_folder, filename)

                with open(file_path, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                print(f"Failed at row {idx}: {e}")

    samples = sorted([int(i) for i in os.listdir(base_folder)])
    # step 1
    logging.info(f"RUN STEP 1: {step_1}")
    if step_1:
        for cid in tqdm(samples, total=len(samples)):
            counter = 0
            while True:
                if counter < retry_count:
                    try:
                        run_step1(cid)
                        break
                    except Exception as e:
                        logging.info(f"failed {cid}: {e}\ncounter: {counter}")
                        counter += 1
                        continue
                else:
                    logging.info(f"failed {cid}")
                    break
    # step 2
    logging.info(f"RUN STEP 2: {step_2}")
    if step_2:
        for cid in tqdm(samples, total=len(samples)):
            counter = 0
            while True:
                if counter < retry_count:
                    try:
                        run_step2(cid, translation_metadata, task="claim")
                        break
                    except Exception as e:
                        logging.info(f"translation failed {cid}; {e}\ncounter: {counter}")
                        counter += 1
                        continue
                else:
                    logging.info(f"translation failed {cid}")
                    break
