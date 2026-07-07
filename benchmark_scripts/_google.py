"""
_google.py  —  Shared Google AI Studio client helper.
All Google model scripts import from here.
Uses the google-genai SDK.
"""

import os
import _core
from google import genai
from google.genai import types

_client = None


def get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


def call_google(
    model_id: str,
    prompt: str,
    system_prompt: str,
    thinking_level: str = "NONE",  # NONE | MINIMAL | LOW | MEDIUM | HIGH
) -> str:
    client = get_client()

    config_kwargs = {}

    # System instruction
    if system_prompt:
        config_kwargs["system_instruction"] = system_prompt

    # Thinking level for Gemini 3 models (replaces thinking_budget)
    # Set to NONE/MINIMAL for consistent non-reasoning responses across benchmark
    if thinking_level and thinking_level != "NONE":
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=0 if thinking_level == "MINIMAL" else None
        )

    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

    resp = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=config,
    )
    if resp.usage_metadata:
        _core._call_usage["input_tokens"]  = resp.usage_metadata.prompt_token_count
        _core._call_usage["output_tokens"] = resp.usage_metadata.candidates_token_count

    # Guard: Gemini can return resp.text as None when content is blocked.
    # Write filter_reason into _call_usage so _core.py can persist
    # provider-specific diagnostic detail into the CSV filter_reason column.
    # The definitive sentinel substitution is also applied in _core.py
    # (covers all providers); this guard is extra defence-in-depth.
    text = resp.text
    if text is None:
        candidates = getattr(resp, "candidates", None) or []
        finish_reason = (
            getattr(candidates[0], "finish_reason", "unknown") if candidates else "unknown"
        )
        _core._call_usage["filter_reason"] = (
            f"google: resp.text was null (finish_reason={finish_reason!r})"
        )
        return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
    return text