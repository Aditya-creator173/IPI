"""
run_grok4.py  —  Grok 4.3 via AWS Bedrock (Mantle Endpoint)
Provider  : AWS Bedrock
Model ID  : xai.grok-4.3
Role      : Minimal-safety baseline & Axis 4 xAI flagship anchor
Auth      : AWS_BEARER_TOKEN_BEDROCK / BEDROCK_API_KEY_1
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from _core import run_benchmark
from _bedrock import call_bedrock

MODEL_NAME    = "grok4"
MODEL_ID      = "xai.grok-4.3"
PAUSE_SECONDS = 1.5

def call(prompt: str, system_prompt: str) -> str:
    return call_bedrock(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print("Provider: AWS Bedrock (Mantle Endpoint) | Role: Minimal-Safety Baseline")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
