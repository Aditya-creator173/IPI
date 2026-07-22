"""
run_liquidai_lfm.py  —  LiquidAI LFM-7B via OpenRouter
Provider  : OpenRouter
Model ID  : liquid/lfm-7b:free
Env var   : OPENROUTER_KEY_LIQUIDAI  (or OPENROUTER_API_KEY fallback)


"""
from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "liquidai_lfm"
MODEL_ID      = "liquid/lfm-7b:free"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt, model_suffix="LIQUIDAI")

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)