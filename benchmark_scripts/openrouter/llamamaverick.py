"""
run_llama4_maverick.py  —  Llama 4 Maverick 17B 128E via OpenRouter (Account 1)
Provider  : OpenRouter
Model ID  : meta-llama/llama-4-maverick:free
Rate limit: 50 RPD free / 1,000 RPD with $10 credit
Env var   : OPENROUTER_API_KEY  (Account 1)

Usage:
    python run_llama4_maverick.py
    python run_llama4_maverick.py --dry-run
    python run_llama4_maverick.py --validate
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "llama4_maverick"
MODEL_ID      = "meta-llama/llama-4-maverick:free"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)