"""
run_qwen36_27b.py  —  Qwen 3.6 27B via Groq
Provider : Groq
Model ID : qwen/qwen3.6-27b (verified from API)
Rate limit: Groq Limits

Usage:
    python run_qwen36_27b.py
    python run_qwen36_27b.py --dry-run
    python run_qwen36_27b.py --validate
"""

from _core import run_benchmark
from _groq import call_groq

MODEL_NAME    = "qwen36_27b"
MODEL_ID      = "qwen/qwen3.6-27b"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_groq(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
