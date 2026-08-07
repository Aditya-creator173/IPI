"""
run_llama4_scout.py  —  LLaMA 4 Scout via Cloudflare Workers AI
Provider  : Cloudflare Workers AI
Model ID  : llama-4-scout-17b-16e-instruct
Role      : Axis F scale midpoint & Axis H compound constituent
"""

from _core import run_benchmark
from _cloudflare import call_cloudflare

MODEL_NAME    = "llama4_scout"
MODEL_ID      = "llama-4-scout-17b-16e-instruct"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cloudflare(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
