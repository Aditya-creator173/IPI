"""
run_qwen37_flash.py — Qwen 3.7 Flash via QwenCloud (DashScope)
Provider : QwenCloud / DashScope
Model ID : qwen3.7-flash
"""
from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME = "qwen37_flash"
MODEL_ID = "qwen3.7-flash"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
