"""
run_qwen3_80b.py  —  Qwen3-Next-80B-A3B via OpenRouter
Provider  : OpenRouter
Model ID  : qwen/qwen3-next-80b-a3b:free
Env var   : OPENROUTER_KEY_QWEN3_80B  (or OPENROUTER_API_KEY fallback)


"""
from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "qwen3_80b"
MODEL_ID      = "qwen/qwen3-next-80b-a3b:free"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt, model_suffix="QWEN3_80B")

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)