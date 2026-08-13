"""
run_qwen3_30b_moe.py  —  Qwen 3 30B MoE via Cloudflare Workers AI
Provider  : Cloudflare Workers AI
Model ID  : qwen3-30b-a3b-fp8
Role      : Axis C non-Google MoE replication
"""

from _core import run_benchmark
from _cloudflare import call_cloudflare

MODEL_NAME    = "qwen3_30b_moe"
MODEL_ID      = "@cf/qwen/qwen3-30b-a3b-fp8"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cloudflare(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
