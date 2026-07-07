"""
[DROPPED — DO NOT RESTORE without a stated hypothesis checked against Scout's coverage]

run_llama4_maverick.py  —  Llama 4 Maverick 17B 128E via NVIDIA NIM

Decision trail (three rejections — this model has been explicitly dropped three times):

  Rejection 1 (OpenRouter era):
    Dropped on budget grounds — OpenRouter free tier cost made it non-viable.
    Reasoning: redundant with Scout, same MoE generation, Scout covers the
    research question.

  Rejection 2 (NIM era — caught and re-corrected):
    This model was silently reintroduced when NIM became available. The
    correction explicitly stated: "There is no research question here that
    Scout doesn't already answer... Dropping it again. This time it stays
    dropped."

  Rejection 3 (compiled summary):
    The Phase 4 finalized model list reintroduced this model a third time,
    tagged it as 🆕 newly proposed, moved it to NIM with no justification for
    the provider change, and encoded it as one of only four "Controlled Pairs"
    — manufacturing a justification post-hoc. This was the subject of an
    explicit correction that produced the July 7, 2026 finalized model list.

Why Scout makes Maverick unnecessary:
    Scout (Llama 4 17B 16E) answers the research question it raises on its own.
    Scout's inclusion already tests MoE routing at the Llama 4 generation. The
    "expert-count scaling" hypothesis (16E vs 128E) is a genuinely interesting
    question, but it requires both models to be in scope and on free tiers. If
    a case is made for this pair in a future session, it must:
      1. State the expert-count scaling hypothesis explicitly.
      2. Confirm Scout cannot already answer it alone.
      3. Not be inferred from "it's free and available."

Provider   : NVIDIA NIM (OpenAI-compatible)
Model ID   : meta/llama-4-maverick-17b-128e-instruct
Params     : 17B active / 128 experts
Script moved to: benchmark_scripts/legacy_models/ (July 7, 2026)
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "llama4_maverick"
MODEL_ID      = os.environ.get("NIM_MAVERICK_MODEL_ID", "meta/llama-4-maverick-17b-128e-instruct")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="MAVERICK")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
