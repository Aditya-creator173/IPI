"""
run_deepseek_v3.py  —  DeepSeek V3-0324 via OpenRouter (Account 2)
Provider  : OpenRouter
Model ID  : deepseek/deepseek-chat-v3-0324:free
Rate limit: 50 RPD free / 1,000 RPD with $10 credit
Env var   : OPENROUTER_API_KEY  (Account 2 — different key from Account 1)

Usage:
    python run_deepseek_v3.py
    python run_deepseek_v3.py --dry-run
    python run_deepseek_v3.py --validate
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "deepseek_v3"
MODEL_ID      = "deepseek/deepseek-chat-v3-0324:free"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)