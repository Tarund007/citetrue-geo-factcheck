"""
Verification and judgment module for CiteTrue GEO.
Compares extracted claims against live search snippets to determine:
- Verified
- Inaccurate (with real-world corrected fact)
- False (with real-world corrected fact or debunking evidence)
"""
import json
from typing import Dict, Any, List
from google import genai
from google.genai import types

from src.prompts import VERIFICATION_SYSTEM_PROMPT


def judge_claim(claim: Dict[str, Any], search_results: List[Dict[str, Any]], gemini_api_key: str) -> Dict[str, Any]:
    """
    Evaluates a single claim against live search snippets using Gemini.
    """
    quote = claim.get("quote", "")
    claim_type = claim.get("claim_type", "statistic")

    # Format snippets for prompt
    snippets_text = ""
    sources = []
    for idx, res in enumerate(search_results):
        url = res.get("url", "")
        title = res.get("title", "")
        snippet = res.get("snippet", "")
        if url and url not in sources:
            sources.append(url)
        snippets_text += f"\n[Result {idx+1}] {title}\nURL: {url}\nSnippet: {snippet}\n"

    if not snippets_text.strip():
        return {
            "verdict": "False",
            "evidence_summary": "No live web search results were found to corroborate this claim.",
            "corrected_fact": "Unverified / No evidence found in public records.",
            "sources": []
        }

    client = genai.Client(api_key=gemini_api_key)

    prompt = (
        f"{VERIFICATION_SYSTEM_PROMPT}\n\n"
        f"CLAIM TO EVALUATE:\n\"{quote}\"\n"
        f"CLAIM TYPE: {claim_type}\n\n"
        f"LIVE RETRIEVED SEARCH SNIPPETS:\n{snippets_text}\n\n"
        f"Provide verdict, evidence_summary, and corrected_fact in JSON format."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
        raw_json = response.text.strip()
        if raw_json.startswith("```json"):
            raw_json = raw_json[7:]
        if raw_json.startswith("```"):
            raw_json = raw_json[3:]
        if raw_json.endswith("```"):
            raw_json = raw_json[:-3]

        parsed = json.loads(raw_json.strip())
        return {
            "verdict": parsed.get("verdict", "False"),
            "evidence_summary": parsed.get("evidence_summary", "Evaluation completed."),
            "corrected_fact": parsed.get("corrected_fact", "N/A"),
            "sources": sources[:3]
        }
    except Exception as e:
        # Fallback evaluation
        return {
            "verdict": "Inaccurate",
            "evidence_summary": f"Automated judgement encountered rate-limit or parsing issue: {str(e)[:100]}",
            "corrected_fact": "Manual verification recommended via provided sources.",
            "sources": sources[:2]
        }
