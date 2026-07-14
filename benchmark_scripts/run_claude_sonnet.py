"""
[RETIRED — July 12 2026]
run_claude_sonnet.py  —  Claude Sonnet 4.6 via Anthropic API
Provider  : Anthropic
Model ID  : claude-sonnet-4-6
            Verify latest at console.anthropic.com/settings/models
Env var   : ANTHROPIC_API_KEY

Why manual-only: see run_claude_haiku.py.

Research role:
  CAI mid-tier flagship. Baseline model with confirmed 0% ASR in prior
  manual runs. Historical result anchor for cross-version comparison
  against Sonnet 5 (latest) and Opus 4.8.

Usage (manual probe sessions only):
    python run_claude_sonnet.py --dry-run
    python run_claude_sonnet.py --validate
"""

import os
import anthropic
import _core
from _core import run_benchmark

MODEL_NAME    = "claude_sonnet"
MODEL_ID      = "claude-sonnet-4-6"   # update if newer string confirmed
PAUSE_SECONDS = 2.0

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def call(prompt: str, system_prompt: str) -> str:
    kwargs: dict = {
        "model":      MODEL_ID,
        "max_tokens": 1024,
        "messages":   [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    resp = client.messages.create(**kwargs)
    _core._call_usage["input_tokens"]  = resp.usage.input_tokens
    _core._call_usage["output_tokens"] = resp.usage.output_tokens
    return "".join(
        block.text for block in resp.content if hasattr(block, "text")
    )


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)