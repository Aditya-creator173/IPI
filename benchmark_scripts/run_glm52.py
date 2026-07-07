"""
run_glm52.py  —  GLM 5.2 via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : z-ai/glm-5.2  (override via NIM_GLM52_MODEL_ID)
Env var   : NVIDIA_KEY_GLM52  (or NVIDIA_API_KEY fallback)

Research role:
  Zhipu AI's next-generation independent Chinese architecture. Replaces GLM 5.1.
  Does NOT use a LLaMA base — independently developed architecture and pretraining
  from a distinct Chinese lab. Tests how Western IPI attack patterns propagate
  through independently developed Chinese alignment, separate from both Alibaba
  (Qwen) and Moonshot (Kimi) architectures. Upgrades GLM 5.1 to the current
  generation model on the same NIM-hosted free tier.

  Paired with Kimi K2.6 (Moonshot AI) and Qwen 3.5 397B (Alibaba) for
  multi-lab Chinese ecosystem coverage with distinct architecture lineages.

⚠️  NIM model IDs shift weekly. Verify at build.nvidia.com before running.
    Set NIM_GLM52_MODEL_ID env var to override without editing this file.

Usage:
    python run_glm52.py
    python run_glm52.py --dry-run
    python run_glm52.py --validate
    python run_glm52.py --v1-only
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "glm52"
MODEL_ID      = os.environ.get("NIM_GLM52_MODEL_ID", "z-ai/glm-5.2")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="GLM52")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
