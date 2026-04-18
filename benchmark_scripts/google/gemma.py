"""
run_gemma4_31b.py  —  Gemma 4 31B Dense via Google AI Studio
Provider  : Google AI Studio
Model ID  : gemma-4-31b-it
Rate limit: 1,500 RPD (shared pool with other Google models on same key)
Env var   : GOOGLE_API_KEY
Note      : Gemma 4 models accessed via Gemini API using same key.
            No thinking_level needed — Gemma 4 is not a reasoning model.

Usage:
    python run_gemma4_31b.py
    python run_gemma4_31b.py --dry-run
    python run_gemma4_31b.py --validate
"""

from _core import run_benchmark
from _google import call_google

MODEL_NAME    = "gemma4_31b"
MODEL_ID      = "gemma-4-31b-it"
PAUSE_SECONDS = 1.5


def call(prompt: str, system_prompt: str) -> str:
    return call_google(MODEL_ID, prompt, system_prompt, thinking_level="NONE")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)