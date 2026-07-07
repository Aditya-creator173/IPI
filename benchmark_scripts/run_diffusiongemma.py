"""
[PENDING — NOT IN ACTIVE COHORT]
Availability on NIM free tier unconfirmed. Decision requires:
  1. Live verification at build.nvidia.com that google/diffusiongemma-26b-a4b-it
     is currently free-tier accessible.
  2. Explicit sign-off on the diffusion-vs-autoregressive hypothesis below.
  3. Confirmation that the NIM chat-completions interface handles system prompts
     identically to autoregressive models (or documented caveats if not).
Do not run in automated benchmark loop until all three are satisfied.

run_diffusiongemma.py  —  DiffusionGemma 26B MoE via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : google/diffusiongemma-26b-a4b-it  (override via NIM_DIFFUSIONGEMMA_MODEL_ID)
Params    : 26B total / 4B active (MoE)
Env var   : NVIDIA_KEY_DIFFUSIONGEMMA  (or NVIDIA_API_KEY fallback)

Research role:
  THE ONLY DIFFUSION-BASED LLM IN ANY PUBLISHED IPI BENCHMARK.

  Standard LLMs generate text autoregressively: one token at a time,
  left-to-right, each token attending to all previous tokens. Injection
  attacks exploit this by inserting instructions mid-sequence that hijack
  the model's conditional generation.

  DiffusionGemma uses a fundamentally different generation mechanism:
  all output tokens are generated IN PARALLEL via iterative denoising
  (analogous to diffusion image models). There is no sequential instruction-
  following chain in the autoregressive sense.

  This creates a genuinely testable hypothesis:
    H0: IPI vulnerability is architecture-agnostic (any LLM follows injected
        instructions regardless of generation mechanism).
    H1: IPI vulnerability is tied to autoregressive attention mechanisms.
        Diffusion-based generation, lacking sequential conditioning, shows
        meaningfully different ASR profiles.

  If ASR differs from transformer counterparts of similar scale (Gemma 4 31B,
  GLM 5.2), this is a publishable architectural finding unique to this paper.

⚠️  NIM model IDs shift weekly. Verify at build.nvidia.com before running.
    Set NIM_DIFFUSIONGEMMA_MODEL_ID env var to override.
⚠️  Diffusion LLMs may not support multi-turn context or system prompts
    identically to autoregressive models. System prompt is included in the
    messages array per NIM's standard chat completions interface. Monitor
    dry-run output for any API differences. Behavior under prompt_warning
    and spotlighting defense modes should be checked carefully.

Usage:
    python run_diffusiongemma.py
    python run_diffusiongemma.py --dry-run
    python run_diffusiongemma.py --validate
    python run_diffusiongemma.py --v1-only
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "diffusiongemma"
MODEL_ID      = os.environ.get("NIM_DIFFUSIONGEMMA_MODEL_ID", "google/diffusiongemma-26b-a4b-it")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="DIFFUSIONGEMMA")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
