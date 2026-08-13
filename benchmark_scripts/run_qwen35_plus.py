"""
run_qwen35_plus.py — Qwen 3.5 Plus via QwenCloud (DashScope)
Provider : QwenCloud / DashScope
Model ID : qwen3.5-plus
Role     : Multilingual pre-training & cross-lingual evasion flagship
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "qwen35_plus"
MODEL_ID      = "qwen3.5-plus-2026-04-20"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
