"""
run_mistral_large3.py  —  Mistral Large 3
Model ID  : mistral-large-2512
Role      : High-throughput European flagship MoE
"""

from _core import run_benchmark
from _mistral import call_mistral

MODEL_NAME    = "mistral_large3"
MODEL_ID      = "mistral-large-2512"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_mistral(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
