"""
run_deepseek_v3.py  —  DeepSeek V3-0324 via OpenRouter
Provider  : OpenRouter
Model ID  : deepseek/deepseek-chat-v3-0324:free
Env var   : OPENROUTER_KEY_DEEPSEEK_V3  (or OPENROUTER_API_KEY fallback)
"""
from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "deepseek_v3"
MODEL_ID      = "deepseek/deepseek-chat-v3-0324:free"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt, model_suffix="DEEPSEEK_V3")

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)