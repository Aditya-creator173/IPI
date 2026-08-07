"""
run_deepseek_r1.py  —  DeepSeek R1 via OpenRouter
Provider  : OpenRouter
Model ID  : deepseek/deepseek-r1
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "deepseek_r1"
MODEL_ID      = "deepseek/deepseek-r1"
PAUSE_SECONDS = 1.5

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)

