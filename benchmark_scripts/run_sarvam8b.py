"""
run_sarvam8b.py  —  Sarvam 8B
Model ID  : sarvam/sarvam-8b
Role      : Regional Hindi specialization vs safety hierarchy
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "sarvam8b"
MODEL_ID      = "sarvam/sarvam-8b"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
