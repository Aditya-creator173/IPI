"""
run_claude_haiku.py  —  Claude Haiku via Anthropic API
Provider  : Anthropic
Model ID  : claude-haiku-4-5-20251001
Rate limit: Depends on credits granted — pace conservatively
Env var   : ANTHROPIC_API_KEY
Note      : Smallest Constitutional AI model in the set. Anchors the
            Claude family size axis: Haiku (small) → Sonnet (mid) → Opus (flagship).

Usage:
    python run_claude_haiku.py
    python run_claude_haiku.py --dry-run
    python run_claude_haiku.py --validate
"""

import os
import anthropic
from _core import run_benchmark

MODEL_NAME    = "claude_haiku"
MODEL_ID      = "claude-haiku-4-5-20251001"
PAUSE_SECONDS = 2.0

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def call(prompt: str, system_prompt: str) -> str:
    kwargs = {
        "model":      MODEL_ID,
        "max_tokens": 1024,
        "messages":   [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    resp = client.messages.create(**kwargs)
    # Anthropic returns a list of content blocks
    return "".join(
        block.text for block in resp.content if hasattr(block, "text")
    )


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)