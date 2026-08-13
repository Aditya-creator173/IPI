"""
run_qwen35_397b.py — Legacy: Qwen 3.5 397B via NVIDIA NIM
Provider  : NVIDIA NIM
Model ID  : qwen/qwen3.5-397b-a17b
Role      : Alternative open-weight 397B dense model endpoint on NIM
Note      : Preserved in legacy_models directory to avoid confusion with QwenCloud's qwen3.5-plus.
"""

from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "qwen35_397b"
MODEL_ID      = "qwen/qwen3.5-397b-a17b"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
