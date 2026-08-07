"""
run_cohere_command_a_plus.py  —  Cohere Command A+
Model ID  : command-a-plus
Role      : Primary Cohere premium RAG flagship
"""

from _core import run_benchmark
from _cohere import call_cohere

MODEL_NAME    = "cohere_command_a_plus"
MODEL_ID      = "command-a-plus"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cohere(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
