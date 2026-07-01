"""
run_deepseek_r1_0528.py  —  DeepSeek R1-0528 via OpenRouter
Provider  : OpenRouter
Model ID  : deepseek/deepseek-r1-0528:free
Rate limit: 50 RPD free / 1,000 RPD with $10 credit
Env var   : OPENROUTER_API_KEY

Usage:
    python run_deepseek_r1_0528.py
    python run_deepseek_r1_0528.py --dry-run
    python run_deepseek_r1_0528.py --validate
    python run_deepseek_r1_0528.py --full
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "deepseek_r1"
MODEL_ID      = "deepseek/deepseek-r1-0528:free"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt, model_suffix="DEEPSEEK_R1_0528")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)