"""
run_llama31_8b.py  —  LLaMA 3.1 8B via Groq
Provider : Groq
Model ID : llama-3.1-8b-instant
Rate limit: ~14,400 RPD (most generous on Groq)

Usage:
    python run_llama31_8b.py              # full run
    python run_llama31_8b.py --dry-run    # first 3 cases, mode=none
    python run_llama31_8b.py --validate   # A001 x 4 modes, phrase check
"""

from _core import run_benchmark
from _groq import call_groq

MODEL_NAME     = "llama3.1_8b"
MODEL_ID       = "llama-3.1-8b-instant"
PAUSE_SECONDS  = 1.5   # conservative; 8B has the highest limit on Groq

def call(prompt: str, system_prompt: str) -> str:
    return call_groq(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)