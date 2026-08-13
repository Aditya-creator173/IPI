"""
run_jamba15_large.py — Jamba 1.5 Large via AWS Bedrock
Model ID  : ai21.jamba-1-5-large-v1:0
Role      : Axis 10 (SSM-Transformer Hybrid Architecture)
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from _core import run_benchmark
from _bedrock import call_bedrock

MODEL_NAME    = "jamba15_large"
MODEL_ID      = "ai21.jamba-1-5-large-v1:0"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_bedrock(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
