"""
_azure_openai.py  —  Shared Azure OpenAI / Azure Foundry client helper.
Supports:
  - Azure OpenAI Service resources (https://<resource>.openai.azure.com/openai/v1)
  - Azure AI Foundry Serverless / MaaS (https://<model>.<region>.models.ai.azure.com/v1)
  - Azure AI Foundry Managed Compute Online Endpoints (https://<deployment>.<region>.inference.ml.azure.com/v1)
"""

from __future__ import annotations

import os
import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APIConnectionError, RateLimitError

_clients: dict[str, OpenAI] = {}

def get_client(custom_endpoint: str | None = None, custom_api_key: str | None = None) -> OpenAI:
    endpoint = custom_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT") or os.environ.get("AZURE_UAE_OPENAI_ENDPOINT")
    if not endpoint:
        try:
            endpoint = _keys.get_key("AZURE_OPENAI_ENDPOINT")
        except Exception:
            endpoint = None
    
    api_key = custom_api_key or os.environ.get("AZURE_API_KEY") or os.environ.get("AZURE_UAE_API_KEY")
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
    if not base_url.endswith("/v1") and "/openai/deployments" not in base_url and not base_url.endswith("/v1/chat/completions"):
        base_url = f"{base_url}/v1"

    cache_key = f"{base_url}:{api_key[:8]}"
    if cache_key not in _clients:
        _clients[cache_key] = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    return _clients[cache_key]


def call_azure_openai(
    model_id: str,
    prompt: str,
    system_prompt: str,
    custom_endpoint: str | None = None,
    custom_api_key: str | None = None,
    timeout: int = 120,
    max_retries: int = 4,
    initial_backoff: float = 2.0,
    max_tokens: int = 4096,
) -> str:
    """
    Call an Azure OpenAI / Azure Foundry model endpoint.
    Automatically checks per-model environment overrides (e.g. AZURE_PHI4_ENDPOINT, AZURE_GPT5_ENDPOINT).
    NOTE: Never passes temperature or top_p for GPT-5 family compatibility.
    """
    # Check per-model env overrides
    clean_id = model_id.lower().replace("-", "").replace(".", "").replace("_", "")
    if "phi4" in clean_id:
        endpoint = custom_endpoint or os.environ.get("AZURE_PHI4_ENDPOINT")
        key = custom_api_key or os.environ.get("AZURE_PHI4_API_KEY") or os.environ.get("AZURE_PHI4_KEY")
    elif "gpt5" in clean_id and not any(x in clean_id for x in ["sol", "terra", "luna", "54", "55"]):
        endpoint = custom_endpoint or os.environ.get("AZURE_GPT5_ENDPOINT")
        key = custom_api_key or os.environ.get("AZURE_GPT5_API_KEY") or os.environ.get("AZURE_GPT5_KEY")
    else:
        endpoint = custom_endpoint
        key = custom_api_key

    client = get_client(endpoint, key)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            start_time = time.time()
            kwargs: dict = {
                "model": model_id,
                "messages": messages,
                "timeout": timeout,
            }
            if "gpt" in model_id.lower():
                kwargs["max_completion_tokens"] = max_tokens
            else:
                kwargs["max_tokens"] = max_tokens

            resp = client.chat.completions.create(**kwargs)
            latency = int((time.time() - start_time) * 1000)

            if resp.usage:
                _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens or 0
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens or 0
                _core._call_usage["latency_ms"]    = latency

            if not resp.choices:
                return "API_ERROR: Empty choices array returned"

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"azure_openai: content field was null "
                    f"(finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (Azure content filter)"

            return content

        except (APIStatusError, RateLimitError) as e:
            status = getattr(e, "status_code", 429)
            err_msg = str(e).lower()
            if status == 400 and ("content_filter" in err_msg or "content management policy" in err_msg):
                _core._call_usage["filter_reason"] = "azure_openai: content management policy triggered (HTTP 400 content_filter)"
                return "PROVIDER_FILTERED: content management policy triggered (Azure content filter)"
            if status in (429, 500, 502, 503) and attempt < max_retries:
                print(f"\n[AzureOpenAI] Attempt {attempt+1} HTTP {status}. Retrying in {backoff:.1f}s...")
                time.sleep(backoff)
                backoff *= 2.0
                continue
            if attempt == max_retries:
                return f"API_ERROR: Azure OpenAI failed after {max_retries} retries: {e}"
            raise

        except APIConnectionError as e:
            if attempt < max_retries:
                print(f"\n[AzureOpenAI] Attempt {attempt+1} Connection error. Retrying in {backoff:.1f}s...")
                time.sleep(backoff)
                backoff *= 2.0
                continue
            return f"API_ERROR: Connection error after {max_retries} retries: {e}"

        except Exception as e:
            return f"API_ERROR: Unexpected error: {e}"

    return "API_ERROR: Exceeded max retries"
