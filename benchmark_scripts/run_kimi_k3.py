"""
run_kimi_k3.py  —  Moonshot Kimi K3 via Fireworks AI
Provider  : Fireworks AI / Moonshot
Model ID  : accounts/fireworks/models/kimi-k3
Role      : Axis 4/16 extreme context MoE flagship
Auth      : FIREWORKS_API_KEY
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from _core import run_benchmark
from _fireworks import call_fireworks

MODEL_NAME    = "kimi_k3"
MODEL_ID      = os.environ.get("FIREWORKS_KIMI_K3_ID", "accounts/fireworks/models/kimi-k3")
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_fireworks(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print("Provider: Fireworks AI | Role: Axis 4/16 Kimi K3 Flagship")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
