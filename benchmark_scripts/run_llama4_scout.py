"""
run_llama4_scout.py  —  Llama 4 Scout 17B 16E via Groq
Provider : Groq
Model ID : meta-llama/llama-4-scout-17b-16e-instruct
Rate limit: Check console.groq.com — MoE model, limits vary

Usage:
    python run_llama4_scout.py
    python run_llama4_scout.py --dry-run
    python run_llama4_scout.py --validate
"""

from _core import run_benchmark
from _groq import call_groq

MODEL_NAME    = "llama4_scout"
MODEL_ID      = "meta-llama/llama-4-scout-17b-16e-instruct"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_groq(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)