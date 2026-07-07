"""
[MANUAL ONLY — do not use in automated benchmark runs]
run_claude_opus.py  —  Claude Opus 4.8 via Anthropic API
Provider  : Anthropic
Model ID  : claude-opus-4-8
            Verify at console.anthropic.com/settings/models before running.
            Fallback: claude-opus-4-7 if 4.8 not yet on API.
Env var   : ANTHROPIC_API_KEY

Why manual-only: see run_claude_haiku.py. Opus is the most expensive
per-token Anthropic model — automated runs would drain credits fastest.

Research role:
  Largest CAI model. Tests whether maximum Constitutional AI capability
  tier improves IPI resistance vs. Haiku and Sonnet.

Usage (manual probe sessions only):
    python run_claude_opus.py --dry-run
    python run_claude_opus.py --validate
"""

import os
import anthropic
import _core
from _core import run_benchmark

MODEL_NAME    = "claude_opus"
MODEL_ID      = "claude-opus-4-8"    # verify at console.anthropic.com
PAUSE_SECONDS = 3.0                   # extra pause — highest per-token cost

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