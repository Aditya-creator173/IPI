"""
run_liquid_lfm25.py — LiquidAI LFM 2.5-2.6B via OpenRouter
Provider  : OpenRouter
Model ID  : liquid/lfm-2.5-2.6b:free
Role      : Compact reasoning model / hybrid architecture analysis
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "liquid_lfm25"
MODEL_ID      = "liquid/lfm-2.5-2.6b:free"
PAUSE_SECONDS = 1.0


def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
