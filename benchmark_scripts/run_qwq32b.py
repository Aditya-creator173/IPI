"""
run_qwq32b.py  —  QwQ 32B via Cloudflare Workers AI
Provider  : Cloudflare Workers AI
Model ID  : qwq-32b
Role      : Axis B cross-lab CoT replication
"""

from _core import run_benchmark
from _cloudflare import call_cloudflare

MODEL_NAME    = "qwq32b"
MODEL_ID      = "qwq-32b"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cloudflare(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
