"""
run_mistral_large3.py  —  Mistral Large 3 via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : mistralai/mistral-large-3  (override via NIM_MISTRAL_LARGE3_MODEL_ID)
Params    : ~675B dense
Env var   : NVIDIA_KEY_MISTRAL_LARGE3  (or NVIDIA_API_KEY fallback)

Research role:
  Only European-origin flagship in the benchmark. Built under EU AI Act
  cultural and regulatory pressure. Replaces Mistral Medium 3.5 128B — upgraded
  to the full flagship so the paper can state "each lab's flagship evaluated"
  without qualification, matching the principle applied when swapping
  Nemotron Super → Nemotron Ultra.

  Tests whether EU regulatory alignment pressure produces different IPI
  resistance patterns than voluntary safety training approaches (RLHF, CAI).
  Framed as hypothesis, not a settled causal claim — confounds include
  training data, RLHF recipe, and scale.

⚠️  NIM model IDs shift weekly. Verify at build.nvidia.com before running.
    Set NIM_MISTRAL_LARGE3_MODEL_ID env var to override without editing this file.
⚠️  timeout=150 — 675B model under NIM's 40 RPM cap. Per-call latency is
    significantly higher than smaller models. If timeouts persist, increase
    NIM_MISTRAL_LARGE3_TIMEOUT env var (default 150).

Usage:
    python run_mistral_large3.py
    python run_mistral_large3.py --dry-run
    python run_mistral_large3.py --validate
    python run_mistral_large3.py --v1-only
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "mistral_large3"
MODEL_ID      = os.environ.get("NIM_MISTRAL_LARGE3_MODEL_ID", "mistralai/mistral-large-3-675b-instruct-2512")
TIMEOUT       = int(os.environ.get("NIM_MISTRAL_LARGE3_TIMEOUT", "150"))
PAUSE_SECONDS = 3.0   # extra pause for 675B — conservative at 40 RPM

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="MISTRAL_LARGE3", timeout=TIMEOUT)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
