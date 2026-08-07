"""
run_qwen38_max.py  —  Qwen 3.8 Max via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : qwen3.8-max
Role      : Axis D 5th-gen Qwen flagship 2.4T MoE
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "qwen38_max"
MODEL_ID      = "qwen3.8-max"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
