"""
_azure_openai.py  —  Shared Azure OpenAI / Azure Foundry client helper.
Used for Azure UAE North endpoints (OpenAI GPT-5 family, Grok 4, DeepSeek, Phi-4, etc.)
"""

import os
import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APIConnectionError, RateLimitError

_client = None

def get_client() -> OpenAI:
    global _client
    if _client is None:
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or os.environ.get("AZURE_UAE_OPENAI_ENDPOINT")
        if not endpoint:
            try:
                endpoint = _keys.get_key("AZURE_OPENAI_ENDPOINT")
            except Exception:
                endpoint = None
        
        api_key = os.environ.get("AZURE_API_KEY") or os.environ.get("AZURE_UAE_API_KEY")
        if not api_key:
            try:
                api_key = _keys.get_key("AZURE")
            except Exception:
                api_key = None

        if not api_key or not endpoint:
            raise EnvironmentError(
                "AZURE_API_KEY or AZURE_OPENAI_ENDPOINT is missing. Please set:\n"
                "AZURE_API_KEY=your_key\n"
                "AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/openai/v1\n"
                "in your .env file."
            )

        # Normalize base_url if needed
        base_url = endpoint.rstrip("/")
        if not base_url.endswith("/v1") and "/openai/deployments" not in base_url:
            base_url = f"{base_url}/v1"

        _client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    return _client


def call_azure_openai(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 4,
    initial_backoff: float = 2.0,
    max_tokens: int = 4096,
) -> str:
    """
    Call an Azure OpenAI / Azure Foundry model endpoint.
    NOTE: Never passes temperature or top_p as GPT-5 family rejects non-default sampling.
    """
    client = get_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            start_time = time.time()
            # Do NOT pass temperature or top_p for GPT-5 compatibility
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                max_completion_tokens=max_tokens,
                timeout=timeout,
            )
            latency = int((time.time() - start_time) * 1000)
            
            if resp.usage:
                _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens
                _core._call_usage["latency_ms"]    = latency

            if not resp.choices:
                return "API_ERROR: Empty choices array returned"

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"azure_openai: content field was null "
                    f"(finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (provider content filter)"

            return content

        except APIStatusError as e:
            # 400 content filter — gateway blocked prompt, never reaches model; don't retry
            if e.status_code == 400:
                body = str(getattr(e, "body", "") or e)
                if any(k in body for k in ("content_filter", "ResponsibleAIPolicyViolation", "content_management_policy")):
                    _core._call_usage["filter_reason"] = f"azure_openai: 400 gateway content filter ({body[:120]})"
                    return "PROVIDER_FILTERED: azure gateway filter — prompt did not reach model"
            # All other APIStatusError — retry with backoff
            if attempt == max_retries:
                return f"API_ERROR: Azure OpenAI failed after {max_retries} retries: {e}"
            print(f"\n[AzureOpenAI] Attempt {attempt+1} HTTP {e.status_code}. Retrying in {backoff:.1f}s...")
            time.sleep(backoff)
            backoff *= 2.0

        except (RateLimitError, APIConnectionError) as e:
            if attempt == max_retries:
                return f"API_ERROR: Azure OpenAI failed after {max_retries} retries: {e}"
            print(f"\n[AzureOpenAI] Attempt {attempt+1} failed ({e}). Retrying in {backoff:.1f}s...")
            time.sleep(backoff)
            backoff *= 2.0

        except Exception as e:
            return f"API_ERROR: Unexpected error: {e}"

    return "API_ERROR: Exceeded max retries"
