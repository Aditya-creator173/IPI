"""
run_ibm_granite.py  —  IBM Granite 4.0 H Micro via Cloudflare Workers AI
Provider  : Cloudflare Workers AI
Model ID  : granite-4.0-h-micro
Role      : Axis J Mamba-2 / Transformer+MoE hybrid
"""

from _core import run_benchmark
from _cloudflare import call_cloudflare

MODEL_NAME    = "ibm_granite"
MODEL_ID      = "@cf/ibm-granite/granite-4.0-h-micro"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cloudflare(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
