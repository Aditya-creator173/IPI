"""
run_gemini3_flash.py  —  Gemini 3 Flash via Google AI Studio
Provider  : Google AI Studio
Model ID  : gemini-3-flash-preview
Rate limit: 1,500 RPD — fastest Google model to complete
Env var   : GOOGLE_API_KEY
Note      : thinking_level set to MINIMAL for consistent non-reasoning
            responses comparable to other models in the benchmark.

Usage:
    python run_gemini3_flash.py
    python run_gemini3_flash.py --dry-run
    python run_gemini3_flash.py --validate
"""

from _core import run_benchmark
from _google import call_google

MODEL_NAME    = "gemini3_flash"
MODEL_ID      = "gemini-3-flash-preview"
PAUSE_SECONDS = 1.0   # 1,500 RPD is generous


def call(prompt: str, system_prompt: str) -> str:
    return call_google(MODEL_ID, prompt, system_prompt, thinking_level="MINIMAL")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)