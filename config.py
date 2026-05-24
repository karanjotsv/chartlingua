# number of attempts
retry_count = 3

# options: "gemini" , "qwen"
# step 1 (extract_chart, check_chart, check_claim) 
BACKEND_STEP1 = "gemini" 
# step 2 (translate, check_translation) 
BACKEND_STEP2 = "gemini"

# gemini settings (backend = "gemini") 
MODEL_ID = "gemini-2.5-pro"
API_KEY  = ""
# qwen settings (backend = "qwen") 
QWEN_MODEL_PATH = "/home/karanjot/models/Qwen3.5-35B-A3B"
# reduce if chart JSONs are small 
QWEN_MAX_NEW_TOKENS = 16384
# gemma settings (backend = "gemma")
GEMMA_MODEL_PATH = "/home/karanjot/models/gemma4-31b"
GEMMA_MAX_NEW_TOKENS = 4096

# pipeline steps 
download = False
step_1   = False
step_2   = True
step_x   = True

# translation config 
translation_metadata = {
    "source_language_name": "English",
    "source_language_code": "en",
    "target_language_name": "Russian",
    "target_language_code": "ru",
}

ld_preload = "LD_PRELOAD=$HOME/libffi7/install/lib/libffi.so.7"
