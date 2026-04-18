"""
run_nous_hermes_405b.py  —  Nous Hermes 3 405B via OpenRouter (Account 1)
Provider  : OpenRouter
Model ID  : nousresearch/hermes-3-405b-instruct:free
Rate limit: 50 RPD free / 1,000 RPD with $10 credit
Env var   : OPENROUTER_API_KEY  (Account 1)

Usage:
    python run_nous_hermes_405b.py
    python run_nous_hermes_405b.py --dry-run
    python run_nous_hermes_405b.py --validate
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "nous_hermes_405b"
MODEL_ID      = "nousresearch/hermes-3-405b-instruct:free"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)