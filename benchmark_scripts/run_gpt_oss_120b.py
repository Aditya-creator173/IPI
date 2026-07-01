"""
run_gpt_oss_120b.py  —  GPT-OSS 120B via Groq
Provider : Groq
Model ID : openai/gpt-oss-120b
Rate limit: Check console.groq.com

Usage:
    python run_gpt_oss_120b.py
    python run_gpt_oss_120b.py --dry-run
    python run_gpt_oss_120b.py --validate
"""

from _core import run_benchmark
from _groq import call_groq

MODEL_NAME    = "gpt_oss_120b"
MODEL_ID      = "openai/gpt-oss-120b"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_groq(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)