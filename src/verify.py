"""Verification for CiteTrue GEO: grounded verdicts, entity-match guard, no keyword-overlap 'Verified'."""
import datetime
from typing import Dict, Any, List
from urllib.parse import urlparse

from src.llm import call_json
from src.prompts import VERIFICATION_SYSTEM_PROMPT

BLOCKED = {"linkedin.com", "instagram.com", "youtube.com", "youtu.be", "scribd.com", "facebook.com",
           "tiktok.com", "pinterest.com", "quora.com", "reddit.com", "twitter.com", "x.com"}
PREFERRED = ("wikipedia.org", "reuters.com", "economictimes", "livemint.com", "moneycontrol.com",
             "business-standard.com", "nseindia.com", "bseindia.com", "techcrunch.com", "apple.com",
             ".gov", ".edu", "britannica.com", "crunchbase.com", "thehindu.com")
VALID = {"Verified", "Inaccurate", "False", "Unverified"}


def _host(url: str) -> str:
    return urlparse(url).netloc.lower().replace("www.", "")


def _filter(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ok = [r for r in results
          if r.get("url") and not any(_host(r["url"]) == d or _host(r["url"]).endswith("." + d) for d in BLOCKED)]
    return sorted(ok, key=lambda r: 0 if any(p in _host(r["url"]) for p in PREFERRED) else 1)


def judge_claim(claim: Dict[str, Any], search_results: List[Dict[str, Any]], gemini_api_key: str) -> Dict[str, Any]:
    quote = claim.get("quote", "")
    results = _filter(search_results or [])
    if not results:
        return {"verdict": "False", "evidence_summary": "No usable web evidence found for this claim.",
                "corrected_fact": "No evidence found in public sources.", "sources": []}

    urls, text = [], ""
    for i, r in enumerate(results[:6], 1):
        urls.append(r["url"])
        text += f"\n[Result {i}] {r.get('title', '')}\nURL: {r['url']}\nSnippet: {r.get('snippet', '')}\n"

    prompt = (
        f"{VERIFICATION_SYSTEM_PROMPT}\n\nTODAY: {datetime.date.today().isoformat()}\n"
        f'CLAIM: "{quote}"\nTYPE: {claim.get("claim_type", "statistic")}\n\nSEARCH RESULTS:{text}\n'
        "STRICT RULES (override anything above that conflicts):\n"
        "1. Judge ONLY from the results above, and only results about the SAME entity as the claim's subject. "
        "Results about a different company, person or product are not evidence.\n"
        "2. Verified = results explicitly confirm every key figure, date and name in the claim.\n"
        "3. Inaccurate = right entity, but a figure/date/name is wrong or out of date as of TODAY "
        "(e.g. 'planning an IPO' when it already listed).\n"
        "4. False = results contradict the claim or show it is fabricated (e.g. wrong person in a role, absurd magnitude).\n"
        "5. Unverified = results are off-topic, thin or conflicting, or the claim is incomplete (e.g. a missing number). Never guess.\n"
        "6. corrected_fact: for Inaccurate/False give the correct fact with the number/date; for Verified state the "
        "confirmed fact in one short sentence (e.g. 'Founded December 2015 in San Francisco'). Never write only 'Confirmed'.\n"
        'Return JSON: {"verdict": "...", "evidence_summary": "1-2 sentences naming the source", '
        '"corrected_fact": "...", "source_indices": [1, 2]}'
    )

    out = call_json(gemini_api_key, prompt, temperature=0.0)
    if not isinstance(out, dict):
        return {"verdict": "Unverified",
                "evidence_summary": "AI judge unavailable (rate limit or quota). Not verified; retry shortly.",
                "corrected_fact": "Not checked.", "sources": urls[:3]}

    verdict = str(out.get("verdict", "")).strip().capitalize()
    if verdict not in VALID:
        verdict = "Unverified"
    idx = [i for i in out.get("source_indices", []) if isinstance(i, int) and 1 <= i <= len(urls)]
    sources = list(dict.fromkeys([urls[i - 1] for i in idx] + urls))[:3]
    return {"verdict": verdict,
            "evidence_summary": out.get("evidence_summary", "Evaluation completed."),
            "corrected_fact": out.get("corrected_fact", "N/A"),
            "sources": sources}


def heuristic_judge(quote: str, snippets_text: str, sources: List[str]) -> Dict[str, Any]:
    """Kept for compatibility. Keyword overlap must never produce 'Verified'."""
    return {"verdict": "Unverified", "evidence_summary": "AI judge unavailable.",
            "corrected_fact": "Not checked.", "sources": sources[:3]}
