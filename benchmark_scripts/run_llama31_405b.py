"""
run_llama31_405b.py  —  LLaMA 3.1 405B Instruct via SambaNova Cloud
Provider  : SambaNova Cloud (OpenAI-compatible at https://api.sambanova.ai/v1)
Model ID  : Meta-Llama-3.1-405B-Instruct  (SambaNova naming convention)
Env var   : SAMBANOVA_API_KEY

Research role:
  The base model for the Nous Hermes 3 405B controlled pair.
  Nous Research confirmed via their technical report and HuggingFace model card
  that Hermes 3 405B is a full-parameter fine-tune of LLaMA 3.1 405B —
  identical base weights, one changed variable: safety-reduction fine-tuning
  vs. standard Meta RLHF alignment.

  This pairing isolates the effect of alignment fine-tuning on IPI resistance
  at the 405B scale:
    run_llama31_405b.py  →  standard Meta RLHF alignment (this script)
    run_nous_hermes_405b.py →  deliberate safety-reduction FT (OpenRouter)

  If Hermes is significantly more vulnerable, the delta is attributable to
  alignment fine-tuning, not capability or scale differences. This is the
  closest to a controlled experiment the benchmark can construct.

  SambaNova offers a free API tier for LLaMA 3.1 405B. See:
  https://cloud.sambanova.ai/

⚠️  SambaNova model IDs use PascalCase: Meta-Llama-3.1-405B-Instruct.
    Override via SAMBANOVA_MODEL_405B env var if SambaNova changes naming.

Usage:
    python run_llama31_405b.py
    python run_llama31_405b.py --dry-run
    python run_llama31_405b.py --validate
    python run_llama31_405b.py --v1-only
"""

from __future__ import annotations

import os
import time
import _core
from openai import OpenAI, APIStatusError
from _core import run_benchmark

MODEL_NAME    = "llama31_405b"
MODEL_ID      = os.environ.get("SAMBANOVA_MODEL_405B", "Meta-Llama-3.1-405B-Instruct")
BASE_URL      = "https://api.sambanova.ai/v1"
PAUSE_SECONDS = 2.0
TIMEOUT       = 90    # 405B at SambaNova is fast (batched inference); 90s conservative


def _get_client() -> OpenAI:
    key = os.environ.get("SAMBANOVA_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "SAMBANOVA_API_KEY not set. Create a free account at cloud.sambanova.ai "
            "and add the key to your .env file."
        )
    return OpenAI(base_url=BASE_URL, api_key=key)


_client: OpenAI | None = None


def call(prompt: str, system_prompt: str) -> str:
    global _client
    if _client is None:
        _client = _get_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = 2.0
    for attempt in range(4):
        try:
            resp = _client.chat.completions.create(
                model=MODEL_ID,
                messages=messages,
                timeout=TIMEOUT,
            )
            if resp.usage:
                _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"sambanova: content field was null "
                    f"(finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
            return content

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < 3:
                print(
                    f"\n[SambaNova] HTTP {e.status_code}. Retrying in {backoff:.0f}s "
                    f"(attempt {attempt + 1}/3)..."
                )
                time.sleep(backoff)
                backoff *= 2
                continue
            raise


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
