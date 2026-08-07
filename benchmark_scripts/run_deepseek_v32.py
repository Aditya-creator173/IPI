"""
run_deepseek_v32.py  —  DeepSeek V3.2
Model ID  : deepseek-v3.2
Role      : Axis D DeepSeek generational trajectory
"""

from _core import run_benchmark
from _sambanova import call_sambanova

MODEL_NAME    = "deepseek_v32"
MODEL_ID      = "deepseek-v3.2"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_sambanova(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
