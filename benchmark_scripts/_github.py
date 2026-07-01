"""
_github.py  —  Shared GitHub Models client helper.
All GitHub Models scripts import from here to reduce boilerplate.
"""

import os
import _core
from openai import OpenAI

# Export client so that _core.py's token rotation logic works correctly via globals() inspection
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ.get("GITHUB_TOKEN", ""),
)

def call_github(
    model_id: str,
    prompt: str,
    system_prompt: str,
    temperature: float = None,
    fold_system_prompt: bool = False,
    timeout: int = 60
) -> str:
    
    if fold_system_prompt:
        if system_prompt:
            prompt = f"{system_prompt}\n\n---\n\n{prompt}"
        messages = [{"role": "user", "content": prompt}]
    else:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
    kwargs = {
        "model": model_id,
        "messages": messages,
        "timeout": timeout,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
        
    resp = client.chat.completions.create(**kwargs)

    if resp.usage:
        _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
        _core._call_usage["output_tokens"] = resp.usage.completion_tokens

    # Guard: provider-side content filters set content=None (finish_reason="content_filter").
    # Return a sentinel string so _core.py receives a str, not None.
    # The definitive sentinel substitution is also applied in _core.py (covers all providers);
    # this guard is an extra defence-in-depth layer at the source.
    content = resp.choices[0].message.content
    if content is None:
        return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
    return content
