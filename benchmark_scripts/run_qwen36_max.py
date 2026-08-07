"""
run_qwen36_max.py — Qwen 3.6 Max Preview via QwenCloud (DashScope)
Provider : QwenCloud / DashScope
Model ID : qwen3.6-max-preview
"""
from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME = "qwen36_max"
MODEL_ID = "qwen3.6-max-preview"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
