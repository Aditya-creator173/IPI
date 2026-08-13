"""
run_muse_glimmer_30b.py — Meta Muse Glimmer 30B via NVIDIA NIM
Provider  : NVIDIA NIM
Model ID  : meta/muse-glimmer-30b
Role      : Multimodal reasoning model / dense architecture analysis
"""

from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "muse_glimmer_30b"
MODEL_ID      = "meta/muse-glimmer-30b"
PAUSE_SECONDS = 1.0


def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
