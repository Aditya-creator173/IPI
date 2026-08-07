"""
run_qwen37_max.py  —  Qwen 3.7 Max via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : qwen3.7-max
Role      : Axis D 4th-gen Qwen flagship MoE
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "qwen37_max"
MODEL_ID      = "qwen3.7-max"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
