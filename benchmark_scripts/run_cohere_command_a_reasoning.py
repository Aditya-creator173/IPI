"""
run_cohere_command_a_reasoning.py  —  Cohere Command A Reasoning
Model ID  : command-a-reasoning
Role      : Axis B reasoning variant within Cohere
"""

from _core import run_benchmark
from _cohere import call_cohere

MODEL_NAME    = "cohere_command_a_reasoning"
MODEL_ID      = "command-a-reasoning"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cohere(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
