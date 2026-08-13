"""
_vertex_ai.py — Shared Vertex AI (Anthropic Claude / xAI Grok) client helper.

Auth:   Service account JSON at path GCP_SERVICE_ACCOUNT_JSON (from .env),
        or optional GCP_API_KEY for generateContent endpoints.
Scope:  https://www.googleapis.com/auth/cloud-platform

Endpoints:
  - Claude: rawPredict (Anthropic Messages API body)
  - Grok (xAI): generateContent (Gemini-style API body) at locations/global/publishers/xai/models/{model_id}:generateContent
"""

from __future__ import annotations

import os
import time

import _core

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import google.auth.transport.requests
    import google.oauth2.service_account
    import requests as _requests
    _GOOGLE_AUTH_OK = True
except ImportError:
    _GOOGLE_AUTH_OK = False


# ── Auth helpers ──────────────────────────────────────────────────────────────

_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
_credentials = None  # cached SA credentials object


def _get_credentials():
    global _credentials
    if _credentials is not None:
        return _credentials

    if not _GOOGLE_AUTH_OK:
        raise ImportError(
            "google-auth and requests are required. "
            "Run: pip install google-auth requests"
        )

    key_path = os.environ.get("GCP_SERVICE_ACCOUNT_JSON", "").strip()
    if not key_path:
        raise EnvironmentError(
            "GCP_SERVICE_ACCOUNT_JSON not set in .env."
        )
    if not os.path.exists(key_path):
        raise FileNotFoundError(
            f"Service account JSON not found at: {key_path!r}. "
            "Check GCP_SERVICE_ACCOUNT_JSON in .env."
        )

    _credentials = google.oauth2.service_account.Credentials.from_service_account_file(
        key_path, scopes=_SCOPES
    )
    return _credentials


def _get_access_token() -> str:
    """Return a valid Bearer token, refreshing if expired."""
    creds = _get_credentials()
    request = google.auth.transport.requests.Request()
    if not creds.valid:
        creds.refresh(request)
    return creds.token


# ── Config helpers ────────────────────────────────────────────────────────────

def _project() -> str:
    p = os.environ.get("GCP_PROJECT_ID", "").strip()
    if not p:
        raise EnvironmentError("GCP_PROJECT_ID not set in .env.")
    return p


def _location() -> str:
    return os.environ.get("GCP_LOCATION", "us-east5").strip()


# ── Claude Caller (rawPredict) ────────────────────────────────────────────────

def call_vertex_ai(
    model_id: str,
    prompt: str,
    system_prompt: str,
    publisher: str = "anthropic",
    timeout: int = 120,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    """
    Call a Vertex AI Anthropic Claude model via rawPredict (Anthropic Messages API format).
    """
    project = _project()
    location = _location()

    url = (
        f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}"
        f"/locations/{location}/publishers/{publisher}/models/{model_id}:rawPredict"
    )

    payload = {
        "anthropic_version": "vertex-2023-10-16",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        payload["system"] = system_prompt

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            token = _get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            resp = _requests.post(url, headers=headers, json=payload, timeout=timeout)

            if resp.status_code == 200:
                data = resp.json()
                try:
                    text = data["content"][0]["text"]
                    usage = data.get("usage", {})
                    if usage:
                        _core._call_usage["input_tokens"] = usage.get("input_tokens")
                        _core._call_usage["output_tokens"] = usage.get("output_tokens")
                    return text
                except (KeyError, IndexError):
                    stop = data.get("stop_reason", "unknown")
                    _core._call_usage["filter_reason"] = (
                        f"vertex_ai: no text in response (stop_reason={stop!r})"
                    )
                    return f"PROVIDER_FILTERED: no text in response (stop_reason={stop!r})"

            elif resp.status_code in (429, 500, 502, 503, 529) and attempt < max_retries:
                print(f"\n[VertexAI] HTTP {resp.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue

            elif resp.status_code == 401:
                if attempt < max_retries:
                    print("\n[VertexAI] 401 — refreshing SA token and retrying...")
                    global _credentials
                    _credentials = None
                    time.sleep(1)
                    continue
                raise PermissionError(
                    f"[VertexAI] 401 Unauthorized. Check GCP_SERVICE_ACCOUNT_JSON and key validity.\n"
                    f"Response: {resp.text[:300]}"
                )

            elif resp.status_code == 403:
                raise PermissionError(
                    f"[VertexAI] 403 Forbidden — service account likely missing roles/aiplatform.user.\n"
                    f"Project: {project}, Model: {model_id}\n"
                    f"Response: {resp.text[:300]}"
                )

            elif resp.status_code == 404:
                raise ValueError(
                    f"[VertexAI] 404 — model not found or not enabled in this region.\n"
                    f"Model: {model_id}, Location: {location}\n"
                    f"Response: {resp.text[:300]}"
                )

            else:
                raise RuntimeError(
                    f"[VertexAI] HTTP {resp.status_code}: {resp.text[:400]}"
                )

        except (PermissionError, ValueError, RuntimeError):
            raise
        except Exception as e:
            if attempt < max_retries:
                print(f"\n[VertexAI] Connection error attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise


# ── Grok Caller (generateContent) ─────────────────────────────────────────────

def call_vertex_grok(
    model_id: str,
    prompt: str,
    system_prompt: str,
    publisher: str = "xai",
    location: str = "global",
    timeout: int = 120,
    max_retries: int = 4,
    initial_backoff: float = 2.0,
    max_tokens: int = 4096,
) -> str:
    """
    Call an xAI Grok model on GCP Vertex AI via generateContent endpoint.

    model_id examples:
      grok-4.1-fast-reasoning
      grok-4.1-fast-non-reasoning
      grok-4.20-reasoning
      grok-4.20-non-reasoning
    """
    project = _project()

    url = (
        f"https://aiplatform.googleapis.com/v1/projects/{project}"
        f"/locations/{location}/publishers/{publisher}/models/{model_id}:generateContent"
    )

    api_key = os.environ.get("GCP_API_KEY", "").strip()

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"max_output_tokens": max_tokens},
    }
    if system_prompt:
        payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            token = _get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            resp = _requests.post(url, headers=headers, json=payload, timeout=timeout)

            if resp.status_code == 200:
                data = resp.json()
                try:
                    candidates = data.get("candidates", [])
                    if not candidates:
                        _core._call_usage["filter_reason"] = "vertex_grok: empty candidates array"
                        return "PROVIDER_FILTERED: empty candidates array"

                    first = candidates[0]
                    parts = first.get("content", {}).get("parts", [])
                    if not parts:
                        finish = first.get("finishReason", "unknown")
                        _core._call_usage["filter_reason"] = f"vertex_grok: empty parts (finishReason={finish!r})"
                        return f"PROVIDER_FILTERED: empty parts (finishReason={finish!r})"

                    text = parts[0].get("text", "")

                    usage = data.get("usageMetadata", {})
                    if usage:
                        _core._call_usage["input_tokens"] = usage.get("promptTokenCount")
                        _core._call_usage["output_tokens"] = usage.get("candidatesTokenCount")

                    if not text:
                        finish = first.get("finishReason", "unknown")
                        _core._call_usage["filter_reason"] = f"vertex_grok: empty text (finishReason={finish!r})"
                        return f"PROVIDER_FILTERED: empty text (finishReason={finish!r})"

                    return text

                except (KeyError, IndexError) as e:
                    _core._call_usage["filter_reason"] = f"vertex_grok: parse error ({e})"
                    return f"PROVIDER_FILTERED: parse error ({e})"

            elif resp.status_code in (429, 500, 502, 503, 529) and attempt < max_retries:
                print(f"\n[VertexGrok] HTTP {resp.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2.0
                continue

            elif resp.status_code == 401 and attempt < max_retries:
                print("\n[VertexGrok] 401 — refreshing credentials and retrying...")
                global _credentials
                _credentials = None
                time.sleep(1)
                continue

            else:
                raise RuntimeError(
                    f"[VertexGrok] HTTP {resp.status_code}: {resp.text[:400]}"
                )

        except RuntimeError:
            raise
        except Exception as e:
            if attempt < max_retries:
                print(f"\n[VertexGrok] Connection error attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2.0
                continue
            raise
