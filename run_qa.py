import os
import json
import logging
import requests
import pandas as pd
from tqdm import tqdm
from pathlib import Path

from config import *
from pipe import Gemini, Qwen, Gemma

# setup config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log", mode='a'), 
        logging.StreamHandler()
    ]
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

    img = [file.name for file in Path(f"{base_folder}/{cid}").iterdir() if file.name.startswith(str(row['image_id']))][0]
    ipath = f"{base_folder}/{cid}/{img}"

    # extract json + code
    jpath, cpath = pipeline_s1.extract_chart(img_path=ipath)
    # run generated code
    os.chdir(f'{base_folder}/{cid}')
    os.system(f"{ld_preload} python {cpath.split('/')[-1]} {jpath.split('/')[-1]}")
    os.chdir("../" * 3)
    # visual flaw check
    vres = pipeline_s1.check_chart()
    res['chart_check'] = vres
    # query check
    cres = pipeline_s1.check_task(task='qa', query=row['query'], label=row['label'])
    res['query_check'] = cres

    res['query'] = row['query']
    res['label'] = row['label']
    
    # save output
    with open(f"{base_folder}/{cid}/step1.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


def run_step2(cid, translation_metadata):
    res = {} 
    row = add_data[cid]

    img = [file.name for file in Path(f"{base_folder}/{cid}").iterdir() if file.name.startswith(str(row['image_id']))][0]
    ipath = f"{base_folder}/{cid}/{img}"
    # translate
    tquery, tchart, jpath = pipeline_s2.translate(img_path=ipath, query=row['query'], lang_meta=translation_metadata, task="query")
    # translation check
    chart_eval, query_eval = pipeline_s2.check_translation(lang_meta=translation_metadata, task="query")
    res['query_check'] = query_eval
    res['chart_check'] = chart_eval
    res['query'] = row['query']
    res['translated_query'] = tquery

    # run generated code with translated chart JSON
    os.chdir(f'{base_folder}/{cid}')
    os.system(f"{ld_preload} python ai-{row['image_id']}.py {jpath.split('/')[-1]}")
    os.chdir("../" * 3)

    # save output
    with open(f"{base_folder}/{cid}/{translation_metadata['target_language_code']}_step2.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    

def run_label_translation(translation_metadata, query, label):
    # translate label using step 2 pipeline - returns plain text string
    response = pipeline_s2.translate_label(lang_meta=translation_metadata, query=query, label=label)
    return response


if __name__=='__main__': 
    base_folder = './qa/augmented'
    add_data = json.load(open('./qa/test.json', 'r', encoding='utf-8'))
    
    samples = sorted([int(i) for i in os.listdir(base_folder)])
    logging.info(f"BACKEND_STEP1: {BACKEND_STEP1} | BACKEND_STEP2: {BACKEND_STEP2}")
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
    ## STEP 2
    logging.info(f"RUN STEP 2: {step_2}")
    if step_2:
        for cid in tqdm(samples, total=len(samples)):
            counter = 0
            while True:
                if counter < retry_count:
                    try:
                        run_step2(cid, translation_metadata)
                        break
                    except Exception as e:
                        logging.info(f"translation failed {cid}; {e}\ncounter: {counter}")
                        counter += 1
                        continue
                else:
                    logging.info(f"translation failed {cid}")
                    break
    ## STEP X: label translation for QA
    if step_x:
        for cid in tqdm(samples, total=len(samples)):
            ##
            img_id = add_data[cid]['image_id']
            # read json data file
            try:
                json_file = f"{base_folder}/{cid}/{translation_metadata['target_language_code']}_step2.json"
                json_data = json.load(open(json_file, 'r', encoding='utf-8'))
            except Exception as e:
                logging.info(f"failed {cid}: {e}")
                continue

            label = add_data[cid]['label']
            # query label
            json_data['label'] = label.strip()
            # check if all alphabet
            if all(ch.isalpha() or ch.isspace() for ch in label):
                try:
                    response = run_label_translation(translation_metadata, query=json_data['translated_query'], label=label,)
                    # translate_label returns plain text string - backend agnostic
                    json_data['translated_label'] = response.strip()
                except Exception as e:
                    logging.info(f"failed {cid}: {e}")
            else:
                json_data['tranlated_label'] = label.strip()
            # save updated json
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
