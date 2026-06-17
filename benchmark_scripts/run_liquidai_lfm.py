"""
run_liquidai_lfm.py  —  LiquidAI LFM-2.5 1.2B Thinking via OpenRouter (Account 2)
Provider  : OpenRouter
Model ID  : liquid/lfm-2.5-1.2b-thinking:free
Rate limit: 50 RPD free / 1,000 RPD with $10 credit
Env var   : OPENROUTER_API_KEY  (Account 2)

Usage:
    python run_liquidai_lfm.py
    python run_liquidai_lfm.py --dry-run
    python run_liquidai_lfm.py --validate
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "liquidai_lfm"
MODEL_ID      = "liquid/lfm-2.5-1.2b-thinking:free"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)