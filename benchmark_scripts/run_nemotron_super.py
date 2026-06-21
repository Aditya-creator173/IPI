"""
run_nemotron_super.py  —  NVIDIA Nemotron 3 Super via OpenRouter
Provider  : OpenRouter
Model ID  : nvidia/nemotron-3-super-49b-v1:free
Env var   : OPENROUTER_KEY_NEMOTRON  (or OPENROUTER_API_KEY fallback)


"""
from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "nemotron_super"
MODEL_ID      = "nvidia/nemotron-3-super-49b-v1:free"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt, model_suffix="NEMOTRON")

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)