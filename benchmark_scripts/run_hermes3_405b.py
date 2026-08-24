"""
run_hermes3_405b.py  —  Nous Hermes 3 405B via Fireworks AI
Provider  : Fireworks AI
Model ID  : accounts/nous/models/hermes-3-llama-3.1-405b
Role      : Axis 1 RLHF-tuned twin of LLaMA 3.1 405B
Auth      : FIREWORKS_API_KEY
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from _core import run_benchmark
from _fireworks import call_fireworks

MODEL_NAME    = "hermes3_405b"
MODEL_ID      = os.environ.get("FIREWORKS_HERMES_405B_ID", "accounts/nous/models/hermes-3-llama-3.1-405b")
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_fireworks(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print("Provider: Fireworks AI | Role: Axis 1 Nous Hermes 3 405B Twin")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
