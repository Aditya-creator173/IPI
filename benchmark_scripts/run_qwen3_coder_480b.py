"""
run_qwen3_coder_480b.py  —  Qwen 3 Coder 480B MoE via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : qwen3-coder-480b-a35b-instruct
Role      : Axis G Chinese lab code-specialized model
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "qwen3_coder_480b"
MODEL_ID      = "qwen3-coder-480b-a35b-instruct"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
