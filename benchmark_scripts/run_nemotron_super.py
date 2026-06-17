"""
run_nemotron_super.py  —  NVIDIA Nemotron 3 Super via OpenRouter (Account 2)
Provider  : OpenRouter
Model ID  : nvidia/nemotron-3-super-120b-a12b:free
Rate limit: 50 RPD free / 1,000 RPD with $10 credit
Env var   : OPENROUTER_API_KEY  (Account 2)

Usage:
    python run_nemotron_super.py
    python run_nemotron_super.py --dry-run
    python run_nemotron_super.py --validate
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "nemotron_super"
MODEL_ID      = "nvidia/nemotron-3-super-120b-a12b:free"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)