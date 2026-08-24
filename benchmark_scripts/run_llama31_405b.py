"""
run_llama31_405b.py  —  Llama 3.1 405B Instruct via Fireworks AI
Provider  : Fireworks AI
Model ID  : accounts/fireworks/models/llama-v3p1-405b-instruct
Role      : Axis 1 Scale Ceiling (405B) & Axis 6 RLHF Base
Auth      : FIREWORKS_API_KEY
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from _core import run_benchmark
from _fireworks import call_fireworks

MODEL_NAME    = "llama31_405b"
MODEL_ID      = os.environ.get("FIREWORKS_LLAMA_405B_ID", "accounts/fireworks/models/llama-v3p1-405b-instruct")
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_fireworks(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print("Provider: Fireworks AI | Role: Axis 1 Scale Ceiling (405B)")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
