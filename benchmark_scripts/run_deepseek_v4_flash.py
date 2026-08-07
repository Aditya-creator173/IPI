"""
run_deepseek_v4_flash.py  —  DeepSeek V4 Flash via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : deepseek-v4-flash-0731
Role      : Axis I student arm distillation test
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "deepseek_v4_flash"
MODEL_ID      = "deepseek-v4-flash-0731"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
