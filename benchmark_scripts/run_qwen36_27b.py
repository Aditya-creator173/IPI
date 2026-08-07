"""
run_qwen36_27b.py  —  Qwen 3.6 27B via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : qwen3.6-27b
Role      : Finding 7 open-vs-closed within-lab pair
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "qwen36_27b"
MODEL_ID      = "qwen3.6-27b"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
