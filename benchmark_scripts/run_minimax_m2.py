"""
run_minimax_m2.py  —  MiniMax M2.7
Model ID  : minimax-m2.7
Role      : High-speed CN MoE inference test
"""

from _core import run_benchmark
from _sambanova import call_sambanova

MODEL_NAME    = "minimax_m2"
MODEL_ID      = "minimax-m2.7"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_sambanova(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
