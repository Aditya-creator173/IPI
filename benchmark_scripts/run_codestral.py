"""
run_codestral.py  —  Codestral 2508
Model ID  : codestral-2508
Role      : Axis G European code-specialized model
"""

from _core import run_benchmark
from _mistral import call_mistral

MODEL_NAME    = "codestral"
MODEL_ID      = "codestral-2508"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_mistral(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
