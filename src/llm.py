"""Shared Gemini JSON caller with retry/backoff and a status tracker the UI can read."""
import json
import re
import time
from google import genai
from google.genai import types

# Order = preference. Keep only names you have confirmed in Google AI Studio.
MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.0-flash"]

STATUS = {"llm_ok": 0, "llm_fail": 0, "last_error": "", "extract_mode": ""}


def reset_status():
    STATUS.update({"llm_ok": 0, "llm_fail": 0, "last_error": "", "extract_mode": ""})


def _clean(text: str) -> str:
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip()).strip()


def call_json(api_key: str, prompt: str, temperature: float = 0.0, retries: int = 2):
    """Return parsed JSON from the first model that works, else None."""
    if not api_key:
        STATUS["llm_fail"] += 1
        STATUS["last_error"] = "No Gemini API key"
        return None
    client = genai.Client(api_key=api_key)
    for model in MODELS:
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
                break  # bad model name / parse error -> next model
    STATUS["llm_fail"] += 1
    return None
