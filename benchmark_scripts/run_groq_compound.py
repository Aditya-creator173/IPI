"""
run_groq_compound.py  —  Groq Compound System via Groq
Provider : Groq
Model ID : groq-compound-it
"""

from _core import run_benchmark
from _groq import call_groq

MODEL_NAME    = "groq_compound"
MODEL_ID      = "groq-compound-it"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    return call_groq(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
