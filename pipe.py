import os
import re
import json
import torch
from abc import ABC, abstractmethod
from PIL import Image
from transformers import AutoProcessor, AutoTokenizer, AutoModelForImageTextToText, AutoModelForCausalLM

import google.generativeai as genai
from prompt import *


class Base(ABC):
    """
    A pipeline for chart extraction, validation, and translation using Generative AI.
    """
    def __init__(self, logger):
        """
        Initialize the Base pipeline with a logger and load all prompts.

        Parameters
        ----------
        logger : logging.Logger
            Logger instance for structured output.
        """
        self.logger = logger
        # chart data extraction
        self.p_extraction  = p_extraction
        # chart validation
        self.p_chart_check = p_chart_check
        # claim validation
        self.p_claim_check = p_claim_check
        # query answer validation
        self.p_query_check = p_query_check
        # translation
        self.p_trans       = p_translation
        self.p_trans_label = p_label_translation
        # translation validation
        self.p_trans_check = p_translation_check

    @abstractmethod
    def _generate(self, content):
        """
        Send a request to the backend model to generate content based on the input.

        Parameters
        ----------
        content : list
            A list of content to be processed. The list should contain a string with the prompt, and either a PIL Image or a file path to an image.

        Returns
        -------
        response : dict
            The response from the Generative AI model, which should contain a 'status' key with value 'success', and a 'content' key with the generated content.
        """

    @abstractmethod
    def _parse_json(self, response) -> dict:
        """
        Extract and return a JSON dict from a backend response.

        Parameters
        ----------
        response : str or object
            Raw response from the backend model.

        Returns
        -------
        dict
            Parsed JSON as a Python dictionary.
        """

    def _raw_text(self, response) -> str:
        """
        Extract the raw text string from a backend response object.

        Parameters
        ----------
        response : str or object
            Raw response returned by _generate(). Strings are returned
            as-is; Gemini response objects are unwrapped via .text.

        Returns
        -------
        str
            Plain text content of the response.
        """
        # str responses come from qwen; object responses come from gemini
        if isinstance(response, str):
            return response
        return response.text

    def extract_chart(self, img_path, img_desc=None):
        """
        Extract chart data and generate code from the given chart image.

        Parameters
        ----------
        img_path : str
            The file path to the image containing the chart.
        img_desc : str
            A description of the image content.

        Returns
        -------
        tuple
            A tuple containing the paths to the generated JSON and Python code files.
        """
        self.logger.info(f"[INFO] instance path: {img_path}\n[INFO] instance description: {img_desc}")
        self.logger.info(f"[STEP] extracting chart data and code from image: {img_path}")

        # set the image path and determine the base path for output files
        self.img_path = img_path
        base_path = os.path.splitext(img_path)[0]
        self.out_path = f"{os.path.dirname(base_path)}/ai-{os.path.basename(base_path)}"

        # generate JSON and code
        if img_desc:
            response = self._generate([
                self.p_extraction.format(
                    filename=f"{self.out_path}.png",
                    image_description=img_desc
                ),
                Image.open(self.img_path)
            ])
        else:
            response = self._generate([
                self.p_extraction.format(
                    filename=f"{self.out_path}.png",
                ),
                Image.open(self.img_path)
            ])

        # split into JSON and Python code blocks
        code_blocks = [block.strip("```jsonpython\n") for block in self._raw_text(response).split("```\n```")]
        json_str, code_str = code_blocks[0], code_blocks[1]

        # extracted JSON data to a file
        json_file = f"{self.out_path}.json"
        chart_data = json.loads(json_str)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(chart_data, f, ensure_ascii=False, indent=4)
        # generated Python code to a file
        code_file = f"{self.out_path}.py"
        with open(code_file, "w", encoding="utf-8") as f:
            f.write(code_str)

        self.logger.info("[DONE]")

        return json_file, code_file

    def check_chart(self):
        """
        Perform a visual consistency check between the original and generated charts.

        Returns
        -------
        dict
            A dictionary containing the evaluation results.
        """
        self.logger.info("[STEP] running visual consistency check between original and generated charts.")

        # generate visual consistency check response
        response = self._generate([
            self.p_chart_check,
            Image.open(self.img_path),           # original chart image
            Image.open(f"{self.out_path}.png")   # rendered chart image
        ])
        self.logger.info("[DONE]")

        # JSON response as a dictionary
        return self._parse_json(response)

    def check_task(self, task, claim=None, query=None, label=None):
        """
        Validate a claim or query-answer pair against the generated chart.

        Parameters
        ----------
        task : str
            Task type - 'fv' for fact verification (claim check) or 'qa' for question answering.
        claim : str, optional
            The claim to validate. Required when task='fv'.
        query : str, optional
            The question to validate. Required when task='qa'.
        label : str, optional
            The proposed answer. Required when task='qa'.

        Returns
        -------
        dict
            A dictionary containing the evaluation results.
        """
        if task == "fv":
            self.logger.info(f"[STEP] validating claim: '{claim}'")
            response = self._generate([
                self.p_claim_check,
                Image.open(f"{self.out_path}.png"),  # rendered chart image
                claim
            ])
        elif task == "qa":
            self.logger.info(f"[STEP] validating query: '{query}' | label: '{label}'")
            response = self._generate([
                self.p_query_check,
                Image.open(f"{self.out_path}.png"),  # rendered chart image
                query,
                label
            ])
        else:
            raise ValueError(f"task='{task}' not supported. use 'fv' or 'qa'.")

        self.logger.info("[DONE]")
        return self._parse_json(response)

    def translate(self, lang_meta, task, img_path=None, claim=None, query=None):
        """
        Translate the text and chart JSON from source language to target language.

        Parameters
        ----------
        lang_meta : dict
            A dictionary containing language metadata with keys:
            - 'source_language_name'
            - 'source_language_code'
            - 'target_language_name'
            - 'target_language_code'
        task : str
            Task type string used to key the translation prompt (e.g. 'claim', 'query').
        img_path : str, optional
            The file path to the chart image.
        claim : str, optional
            The claim string to translate. Used for FV task.
        query : str, optional
            The query string to translate. Used for QA task.

        Returns
        -------
        tuple
            A tuple containing the translated claim and the path to the JSON file with translated chart data.
        """
        self.logger.info(f"[INFO] instance path: {img_path}\n[INFO] text: {claim or query}")

        # language metadata
        src_lang_name = lang_meta['source_language_name']
        src_lang_code = lang_meta['source_language_code']
        tgt_lang_name = lang_meta['target_language_name']
        tgt_lang_code = lang_meta['target_language_code']

        # claim or query 
        self.text = claim if claim is not None else query
        self.chart_data = json.load(open(f"{os.path.dirname(img_path)}/ai-{os.path.splitext(os.path.basename(img_path))[0]}.json"))
        # initialize
        self.trans_text, self.trans_chart_data, trans_json_file = None, None, None
        # path for translated files
        self.trans_path = f"{os.path.dirname(img_path)}/ai-{tgt_lang_code}_{os.path.splitext(os.path.basename(img_path))[0]}"
        self.logger.info(f"[STEP] translating {task} and chart JSON from {src_lang_code} to {tgt_lang_code}.")

        # prompt for forward translation
        prompt_fwd = self.p_trans.format(
            source_language_name=src_lang_name,
            source_language_code=src_lang_code,
            target_language_name=tgt_lang_name,
            target_language_code=tgt_lang_code,
            task_type=task,
        )
        # use json.dumps to ensure null instead of Python None
        # payload key is dynamic - driven by task type (e.g. claim_to_translate, query_to_translate)
        payload = json.dumps({
            "chart_json_data": self.chart_data,
            f"{task}_to_translate": self.text
        }, ensure_ascii=False)
        
        # run forward translation
        response = self._generate([prompt_fwd, payload])
        translated = self._parse_json(response)

        # log parsed keys to diagnose structure mismatches
        self.logger.info(f"[DEBUG] translated keys: {list(translated.keys())}")

        self.trans_chart_data = translated['translated_chart_json']
        self.trans_text = translated[f'translated_{task}']

        self.logger.info(f"[INFO] translated text: {self.trans_text}")
        self.logger.info("[DONE]")

        # prompt for back-translation
        self.logger.info(f"[STEP] back-translating translated text and chart JSON from {tgt_lang_code} to {src_lang_code}.")
        prompt_bwd = self.p_trans.format(
            source_language_name=tgt_lang_name,
            source_language_code=tgt_lang_code,
            target_language_name=src_lang_name,
            target_language_code=src_lang_code,
            task_type=task,
        )
        # use json.dumps to ensure null instead of Python None
        # payload key is dynamic - driven by task type (e.g. claim_to_translate, query_to_translate)
        payload = json.dumps({
            "chart_json_data": self.trans_chart_data,
            f"{task}_to_translate": self.trans_text
        }, ensure_ascii=False)

        # run back-translation
        response = self._generate([prompt_bwd, payload])
        back_trans = self._parse_json(response)
        self.bt_chart_data = back_trans['translated_chart_json']
        self.bt_text = back_trans[f'translated_{task}']

        self.logger.info(f"[INFO] back-translated {task}: {self.bt_text}")
        self.logger.info("[DONE]")

        # translated chart data to a JSON file
        trans_json_file = f"{self.trans_path}.json"
        with open(trans_json_file, "w", encoding="utf-8") as f:
            json.dump(self.trans_chart_data, f, ensure_ascii=False, indent=4)

        return self.trans_text, self.trans_chart_data, trans_json_file

    def translate_label(self, lang_meta, query=None, label=None):
        """
        """
        # language metadata
        src_lang_name = lang_meta['source_language_name']
        src_lang_code = lang_meta['source_language_code']
        tgt_lang_name = lang_meta['target_language_name']
        tgt_lang_code = lang_meta['target_language_code']

        # prompt for forward translation
        prompt_fwd = self.p_trans_label.format(
            source_language_name=src_lang_name,
            source_language_code=src_lang_code,
            target_language_name=tgt_lang_name,
            target_language_code=tgt_lang_code
        )
        # use json.dumps to ensure null instead of Python None
        payload = json.dumps({
            "translated_query": query,
            "label_to_translate": label
        }, ensure_ascii=False)
        # run forward translation
        response = self._generate([prompt_fwd, payload])
        # return plain text - backend agnostic via _raw_text
        return self._raw_text(response).strip()

    def check_translation(self, lang_meta, task):
        """
        Perform a translation fidelity check for both the chart JSON and task's text.

        Returns
        -------
        tuple
            A tuple containing evaluation results for the chart JSON and task's text.
        """
        # language metadata
        src_lang_name = lang_meta['source_language_name']
        src_lang_code = lang_meta['source_language_code']
        # for translation fidelity check
        prompt_check = self.p_trans_check.format(
            source_language_name=src_lang_name,
            source_language_code=src_lang_code,
            task_type=task,
            task_type_cap=task.capitalize(),
        )

        # check translation fidelity for chart JSON
        self.logger.info("[STEP] running translation check for chart JSON.")
        # use json.dumps to ensure null instead of Python None
        chart_payload = json.dumps({
            "context": "Chart JSON",
            "original_content": self.chart_data,
            "back_translated_content": self.bt_chart_data
        }, ensure_ascii=False)
        response = self._generate([prompt_check, chart_payload])
        chart_eval = self._parse_json(response)
        self.logger.info("[DONE]")

        # check translation fidelity for the claim
        self.logger.info(f"[STEP] running translation check for the {task}.")
        # use json.dumps to ensure null instead of Python None
        payload = json.dumps({
            "context": task.capitalize(),
            "original_content": self.text,
            "back_translated_content": self.bt_text
        }, ensure_ascii=False)
        response = self._generate([prompt_check, payload])
        query_eval = self._parse_json(response)
        self.logger.info("[DONE]")

        return chart_eval, query_eval


class Gemini(Base):
    """
    Gemini API backend. 
    """
    def __init__(self, api_key, model_id, logger):
        """
        Initialize the Gemini pipeline with the specified API key and model ID.

        Parameters
        ----------
        api_key : str
            The API key for the Generative AI service.
        model_id : str
            The ID of the model to use.
        logger : logging.Logger
            Logger instance for structured output.
        """
        super().__init__(logger)
        # provided model ID and API key
        self.model_id = model_id
        self.api_key  = api_key
        genai.configure(api_key=self.api_key)
        # initialize gemini model
        self.model = genai.GenerativeModel(self.model_id)

    def _generate(self, content):
        """
        Send a request to the Generative AI model to generate content based on the input content.

        Parameters
        ----------
        content : list
            A list of content to be processed. The list should contain a string with the prompt, and either a PIL Image or a file path to an image.

        Returns
        -------
        response : dict
            The response from the Generative AI model, which should contain a 'status' key with value 'success', and a 'content' key with the generated content.
        """
        return self.model.generate_content(content)

    def _parse_json(self, response) -> dict:
        """
        Extract and return a JSON dict from a Gemini response object.

        Parameters
        ----------
        response : object
            Raw Gemini response with a .text attribute.

        Returns
        -------
        dict
            Parsed JSON as a Python dictionary.
        """
        # strip markdown fences gemini sometimes wraps around JSON
        text = self._raw_text(response).strip("```json\n").strip("```\n")
        return json.loads(text)


class Qwen(Base):
    """
    Local Qwen transformers backend. 
    """
    def __init__(self, model_path, logger, max_new_tokens=4096):
        """
        Initialize the Qwen pipeline by loading the model and tokenizer from disk.

        Parameters
        ----------
        model_path : str
            Path to the local Qwen model directory.
        logger : logging.Logger
            Logger instance for structured output.
        max_new_tokens : int, optional
            Maximum number of tokens to generate per call. Default is 4096.
            Reduce to speed up inference if outputs are typically short.
        """
        super().__init__(logger)
        # configurable token budget - tune based on typical chart JSON size
        self.max_new_tokens = max_new_tokens
        self.logger.info(f"[INIT] loading Qwen model from {model_path}")
        # load tokenizer and model onto available GPUs
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            device_map="auto",
        )
        self.model.eval()
        self.logger.info("[INIT] Loaded Qwen")

    def _generate(self, content) -> str:
        """
        Send a request to the local Qwen model to generate content based on the input.

        Parameters
        ----------
        content : list
            A list of content to be processed. The list should contain a string with the prompt, and either a PIL Image or a file path to an image.

        Returns
        -------
        response : str
            The response from the Qwen model as a plain string.
        """
        # join text parts only; pil images are not supported in text-only qwen
        prompt = "\n".join(c for c in content if isinstance(c, str))
        messages = [
            # system prompt enforces JSON-only output format
            {"role": "system", "content": "You are a precise JSON translation assistant. Always return only valid JSON with the exact output keys specified in the instructions. Never echo back the input structure."},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,  # skip thinking trace - go straight to JSON output
        )
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        # log input token count to help tune max_new_tokens
        self.logger.info(f"[INFO] input tokens: {inputs['input_ids'].shape[-1]} | max_new_tokens: {self.max_new_tokens}")

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,   # greedy decoding for deterministic JSON output
                temperature=None,
                top_p=None,
            )
        # decode only the newly generated tokens
        new_ids = output_ids[0][inputs["input_ids"].shape[1]:]
        response = self.tokenizer.decode(new_ids, skip_special_tokens=True)

        # log output token count to detect truncation
        self.logger.info(f"[INFO] output tokens: {len(new_ids)}")

        # strip thinking traces qwen emits before the actual response
        return re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    def _parse_json(self, response) -> dict:
        """
        Extract and return a JSON dict from a Qwen response string.

        Parameters
        ----------
        response : str
            Raw string response returned by _generate().

        Returns
        -------
        dict
            Parsed JSON as a Python dictionary.
        """
        text = self._raw_text(response)

        # handle markdown fences qwen may wrap around JSON
        fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if fenced:
            text = fenced.group(1).strip()

        # fallback: extract first { ... } block if extra text surrounds the JSON
        obj_match = re.search(r"\{[\s\S]*\}", text)
        if obj_match:
            text = obj_match.group(0)

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # log full raw response to diagnose what went wrong
            self.logger.error(f"[ERROR] JSON parse failed: {e}")
            self.logger.error(f"[ERROR] raw response was:\n{text}")
            raise

    # step 1 methods are not supported in qwen 
    def extract_chart(self, *args, **kwargs):
        raise NotImplementedError("Qwen does not support Step 1. Set BACKEND_STEP1='gemini' in config.py.")

    def check_chart(self, *args, **kwargs):
        raise NotImplementedError("Qwen does not support Step 1. Set BACKEND_STEP1='gemini' in config.py.")

    def check_task(self, *args, **kwargs):
        raise NotImplementedError("Qwen does not support Step 1. Set BACKEND_STEP1='gemini' in config.py.")


class Gemma(Base):
    """
    Local Gemma 4 transformers backend.
    """
    def __init__(self, model_path, logger, max_new_tokens=8192):
        """
        Initialize the Gemma pipeline by loading the model and processor from disk.

        Parameters
        ----------
        model_path : str
            Path to the local Gemma model directory.
        logger : logging.Logger
            Logger instance for structured output.
        max_new_tokens : int, optional
            Maximum number of tokens to generate per call. Default is 8192.
            Reduce to speed up inference if outputs are typically short.
        """
        super().__init__(logger)
        # configurable token budget - tune based on typical chart JSON size
        self.max_new_tokens = max_new_tokens
        self.logger.info(f"[INIT] loading Gemma model from {model_path}")
        # load processor and model onto available GPUs
        self.processor = AutoProcessor.from_pretrained(model_path)
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            device_map="auto",
        )
        self.model.eval()
        self.logger.info("[INIT] Loaded Gemma")

    def _generate(self, content) -> str:
        """
        Send a request to the local Gemma model to generate content based on the input.

        Parameters
        ----------
        content : list
            A list of content to be processed. The list should contain a string with the prompt, and either a PIL Image or a file path to an image.
            Note: PIL Images are silently skipped as this is a text-only step.

        Returns
        -------
        response : str
            The response from the Gemma model as a plain string.
        """
        # join text parts only; pil images are not supported in text-only step
        prompt = "\n".join(c for c in content if isinstance(c, str))
        messages = [
            # system prompt enforces JSON-only output format
            {"role": "system", "content": "You are a precise JSON translation assistant. Always return only valid JSON with the exact output keys specified in the instructions. Never echo back the input structure."},
            {"role": "user", "content": prompt}
        ]
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            add_generation_prompt=True,
        ).to(self.model.device)

        # log input token count to help tune max_new_tokens
        self.logger.info(f"[INFO] input tokens: {inputs['input_ids'].shape[-1]} | max_new_tokens: {self.max_new_tokens}")

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,   # greedy decoding for deterministic JSON output
            )
        # decode only the newly generated tokens
        new_ids = output_ids[0][inputs["input_ids"].shape[1]:]
        response = self.processor.decode(new_ids, skip_special_tokens=True)

        # log output token count to detect truncation
        self.logger.info(f"[INFO] output tokens: {len(new_ids)}")

        return response.strip()

    def _parse_json(self, response) -> dict:
        """
        Extract and return a JSON dict from a Gemma response string.

        Parameters
        ----------
        response : str
            Raw string response returned by _generate().

        Returns
        -------
        dict
            Parsed JSON as a Python dictionary.
        """
        text = self._raw_text(response)

        # handle markdown fences gemma may wrap around JSON
        fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if fenced:
            text = fenced.group(1).strip()

        # fallback: extract first { ... } block if extra text surrounds the JSON
        obj_match = re.search(r"\{[\s\S]*\}", text)
        if obj_match:
            text = obj_match.group(0)

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # log full raw response to diagnose what went wrong
            self.logger.error(f"[ERROR] JSON parse failed: {e}")
            self.logger.error(f"[ERROR] raw response was:\n{text}")
            raise

    # step 1 methods are not supported in gemma
    def extract_chart(self, *args, **kwargs):
        raise NotImplementedError("Gemma does not support Step 1. Set BACKEND_STEP1='gemini' in config.py.")

    def check_chart(self, *args, **kwargs):
        raise NotImplementedError("Gemma does not support Step 1. Set BACKEND_STEP1='gemini' in config.py.")

    def check_task(self, *args, **kwargs):
        raise NotImplementedError("Gemma does not support Step 1. Set BACKEND_STEP1='gemini' in config.py.")
