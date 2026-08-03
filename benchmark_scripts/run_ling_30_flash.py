"""
run_ling_30_flash.py  —  Ling 3.0 Flash via OpenRouter
Provider  : OpenRouter (Free tier)
Model ID  : inclusionai/ling-3.0-flash:free
Env var   : OPENROUTER_API_KEY

Research role:
  Inclusion AI's lightweight flagship model hosted on OpenRouter free tier.
  Evaluates IPI resistance on open-weights efficient reasoning models.

Usage:
    python run_ling_30_flash.py              # full run
    python run_ling_30_flash.py --dry-run    # first 3 cases, mode=none
    python run_ling_30_flash.py --validate   # A001 x 4 modes, phrase check
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "ling_30_flash"
MODEL_ID      = "inclusionai/ling-3.0-flash:free"
PAUSE_SECONDS = 1.5

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
