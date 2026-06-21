"""
run_llama32_3b.py  —  LLaMA 3.2 3B via OpenRouter
Provider  : OpenRouter
Model ID  : meta-llama/llama-3.2-3b-instruct:free
Env var   : OPENROUTER_KEY_LLAMA32_3B  (or OPENROUTER_API_KEY fallback)


"""
from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "llama32_3b"
MODEL_ID      = "meta-llama/llama-3.2-3b-instruct:free"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt, model_suffix="LLAMA32_3B")

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)