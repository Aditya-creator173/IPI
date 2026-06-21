"""
run_gemma4_26b_moe.py  —  Gemma 4 26B MoE via Google AI Studio
Provider  : Google AI Studio
Model ID  : gemma-4-26b-a4b-it
Rate limit: 1,500 RPD (shared pool)
Env var   : GOOGLE_API_KEY

Usage:
    python run_gemma4_26b_moe.py
    python run_gemma4_26b_moe.py --dry-run
    python run_gemma4_26b_moe.py --validate
"""

from _core import run_benchmark
from _google import call_google

MODEL_NAME    = "gemma4_26b_moe"
MODEL_ID      = "gemma-4-26b-a4b-it"
PAUSE_SECONDS = 1.5


def call(prompt: str, system_prompt: str) -> str:
    return call_google(MODEL_ID, prompt, system_prompt, thinking_level="NONE")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)