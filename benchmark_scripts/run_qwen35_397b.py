"""
run_qwen35_397b.py  —  Qwen 3.5 397B via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : qwen3.5-plus
Role      : Multilingual pre-training & cross-lingual evasion
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "qwen35_397b"
MODEL_ID      = "qwen3.5-plus"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
