"""
run_minimax_m3.py  —  MiniMax M3 (427B MoE)
Model ID  : minimaxai/minimax-m3
Role      : MiniMax flagship 427B multimodal MoE
"""

from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "minimax_m3"
MODEL_ID      = "minimaxai/minimax-m3"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
