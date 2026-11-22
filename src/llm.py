"""Shared Gemini JSON caller with retry/backoff and a status tracker the UI can read."""
import json
import re
import time
from google import genai
from google.genai import types

# Order = preference. Modern Gemini models + auto-discovery
MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-4-hydrogen",
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

STATUS = {"llm_ok": 0, "llm_fail": 0, "last_error": "", "extract_mode": ""}


def reset_status():
    STATUS.update({"llm_ok": 0, "llm_fail": 0, "last_error": "", "extract_mode": ""})


def _clean(text: str) -> str:
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip()).strip()


_DISCOVERED_MODELS = None

def get_candidate_models(client: genai.Client) -> list:
    global _DISCOVERED_MODELS
    if _DISCOVERED_MODELS is not None:
        return _DISCOVERED_MODELS
    try:
        remote = [m.name.replace("models/", "") for m in client.models.list()]
        # Filter for flash/generative models
        valid_remote = [r for r in remote if any(k in r for k in ("flash", "hydrogen", "gemini"))]
        if valid_remote:
            _DISCOVERED_MODELS = valid_remote
            return valid_remote
    except Exception:
        pass
    _DISCOVERED_MODELS = MODELS
    return MODELS


def call_json(api_key: str, prompt: str, temperature: float = 0.0, retries: int = 2):
    """Return parsed JSON from the first model that works, else None."""
    if not api_key:
        STATUS["llm_fail"] += 1
        STATUS["last_error"] = "No Gemini API key"
        return None
    try:
        client = genai.Client(api_key=api_key)
        candidate_models = get_candidate_models(client)
    except Exception as e:
        STATUS["llm_fail"] += 1
        STATUS["last_error"] = f"Client init failed: {str(e)[:150]}"
        return None

    for model in candidate_models:
        for attempt in range(retries):
            try:
                r = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json", temperature=temperature
                    ),
                )
                if r and r.text:
                    out = json.loads(_clean(r.text))
                    STATUS["llm_ok"] += 1
                    return out
            except Exception as e:
                msg = str(e)
                STATUS["last_error"] = msg[:200]
                if any(k in msg for k in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE")):
                    time.sleep(2 * (attempt + 1))  # backoff, then retry same model
                    continue
                break  # bad model name / 404 / parse error -> next model
    STATUS["llm_fail"] += 1
    return None
