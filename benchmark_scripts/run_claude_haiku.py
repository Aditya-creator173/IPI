"""
[MANUAL ONLY — do not use in automated benchmark runs]
run_claude_haiku.py  —  Claude Haiku 4.5 via Anthropic API
Provider  : Anthropic
Model ID  : claude-haiku-4-5-20251001
            Verify latest at console.anthropic.com/settings/models
Env var   : ANTHROPIC_API_KEY

Why manual-only:
  Anthropic models are evaluated via the Claude.ai web interface or the
  API in dedicated manual sessions, not in the automated benchmark loop.
  The API key costs real money at scale; manual collection is more
  deliberate and avoids runaway spend.

  Script is kept on disk so the call() function can be reused for
  ad-hoc probing sessions or future controlled manual runs.

Research role:
  Size floor for the Constitutional AI (CAI) family.
  Anchors the Haiku → Sonnet → Opus capability-size axis.

Usage (manual probe sessions only):
    python run_claude_haiku.py --dry-run
    python run_claude_haiku.py --validate
"""


import os
import anthropic
import _core
from _core import run_benchmark

MODEL_NAME    = "claude_haiku"
MODEL_ID      = "claude-haiku-4-5-20251001"   # update if 4.8 ID confirmed
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