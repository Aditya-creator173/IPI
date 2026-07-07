"""
_groq.py  —  Shared Groq client helper.
All Groq model scripts import from here to reduce boilerplate.
"""

import os
import time
import _core
from groq import Groq, APIStatusError

_client = None


def get_client() -> Groq:
    global _client
    if _client is None:
        key = os.environ.get("GROQ_API_KEY", "")
        if not key:
            raise EnvironmentError(
                "No Groq API key found. Set GROQ_API_KEY in your .env file."
            )
        _client = Groq(api_key=key)
    return _client


def call_groq(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 60,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    """
    Call a Groq model with exponential backoff retry on 429/5xx errors.

    Groq's free tier has per-model RPM ceilings tighter than the raw RPD
    figure suggests; transient 429s should be retried rather than written
    as API_ERROR rows that silently degrade data quality.
    """
    client = get_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=timeout,
            )
            if resp.usage:
                _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            # Guard: provider-side content filters set content=None.
            # Write filter_reason into _call_usage so _core.py can persist
            # provider-specific diagnostic detail into the CSV filter_reason column.
            # The definitive sentinel substitution is also applied in _core.py
            # (covers all providers); this guard is extra defence-in-depth.
            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"groq: content field was null "
                    f"(finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
            return content

        except APIStatusError as e:
            # Retry on 429 (rate limits) and 5xx (server errors)
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                print(
                    f"\n[Groq] HTTP {e.status_code}. Retrying in {backoff:.0f}s "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
