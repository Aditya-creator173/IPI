"""
run_llama4_maverick.py  —  Llama 4 Maverick 17B 128E via OpenRouter
Provider  : OpenRouter
Model ID  : meta-llama/llama-4-maverick:free
Env var   : OPENROUTER_KEY_MAVERICK  (or OPENROUTER_API_KEY fallback)


"""
from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "llama4_maverick"
MODEL_ID      = "meta-llama/llama-4-maverick:free"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt, model_suffix="MAVERICK")

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)