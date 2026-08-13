"""
run_kimi_k2.py  —  Kimi K2.6 via Cloudflare Workers AI
Provider  : Cloudflare Workers AI
Model ID  : kimi-k2-6
Role      : Extreme long-context MoE
"""

from _core import run_benchmark
from _cloudflare import call_cloudflare

MODEL_NAME    = "kimi_k2"
MODEL_ID      = "@cf/moonshotai/kimi-k2.6"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cloudflare(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
