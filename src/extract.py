"""PDF parsing + claim extraction for CiteTrue GEO.
Cleans text (drops headings, rejoins wrapped lines) -> Gemini claims -> regex top-up/fallback.
"""
import re
from typing import List, Dict, Any
import pdfplumber

from src.llm import call_json, STATUS
from src.prompts import EXTRACTION_SYSTEM_PROMPT

KEYWORDS = (r"\b(founded|acquired|acquisition|launched|released|rebranded|ipo|listed|ceo|chairman|"
            r"chief executive|headquartered|located|operates?|completed|began|valuation|revenue|"
            r"employees|beds|cities|countries|unicorns?|users)\b")
FILLER = r"^(for (example|instance)|meanwhile|however|in contrast|moreover|additionally|also)\b[,:]?\s*"
SPLIT = r"(?<=[.!?])\s+(?=[A-Z0-9\"“])|;\s+"


def parse_pdf_text(file_bytes_or_path) -> List[Dict[str, Any]]:
    pages = []
    with pdfplumber.open(file_bytes_or_path) as pdf:
        for i, page in enumerate(pdf.pages):
            pages.append({"page_number": i + 1, "text": (page.extract_text() or "").strip()})
    return pages


def is_heading(line: str) -> bool:
    l = line.strip()
    if not l:
        return True
    w = l.split()
    if l[-1] in ".!?" or len(w) > 12:
        return False
    if re.match(r"(?i)^(section|chapter|part|appendix)\b|^\d+[.)]\s", l):
        return True
    caps = sum(1 for x in w if x[0].isupper() or not x[0].isalpha())
    return caps / len(w) >= 0.6


def page_sentences(text: str) -> List[str]:
    body = " ".join(l.strip() for l in text.split("\n") if l.strip() and not is_heading(l))
    body = re.sub(r"(\w)-\s+(\w)", r"\1-\2", body)  # rejoin hyphen-wrapped words
    return [s.strip() for s in re.split(SPLIT, body) if s.strip()]


def checkable(s: str) -> bool:
    return len(s.split()) >= 6 and bool(re.search(r"\d", s) or re.search(KEYWORDS, s, re.I))


def score(s: str) -> int:
    sc = min(len(re.findall(r"\d[\d,.]*", s)), 3) * 2
    if re.search(r"\b(19|20)\d{2}\b", s):
        sc += 2
    if re.search(r"[$₹€£%]|\b(billion|million|crore|lakh|percent)\b", s, re.I):
        sc += 2
    sc += 2 * min(len(re.findall(KEYWORDS, s, re.I)), 2)
    sc += min(len(re.findall(r"\b[A-Z][a-z]+\b", s[1:])), 4)
    return sc


def clean_query(s: str) -> str:
    return re.sub(FILLER, "", s, flags=re.I).strip()[:150]


def regex_claims(pages: List[Dict[str, Any]], max_claims: int) -> List[Dict[str, Any]]:
    seen, cands = set(), []
    for p in pages:
        for s in page_sentences(p["text"]):
            k = s.lower()[:60]
            if k in seen or not checkable(s):
                continue
            seen.add(k)
            cands.append((len(cands), score(s), s))
    top = sorted(cands, key=lambda c: -c[1])[:max_claims]  # best-scored across whole doc
    top.sort(key=lambda c: c[0])                           # restore document order
    return [{"claim_id": i + 1, "quote": s, "claim_type": "statistic", "search_query": clean_query(s)}
            for i, (_, _, s) in enumerate(top)]


fallback_heuristic_extraction = lambda pages_data, max_claims=15: regex_claims(pages_data, max_claims)


def extract_claims_from_text(pages_data, gemini_api_key, max_claims: int = 15):
    STATUS["extract_mode"] = "regex"
    corpus = "\n".join(
        f"[Page {p['page_number']}] " + " ".join(page_sentences(p["text"])) for p in pages_data
    )
    claims: List[Dict[str, Any]] = []

    if gemini_api_key and corpus.strip():
        prompt = (
            f"{EXTRACTION_SYSTEM_PROMPT}\n\nRULES (override anything above that conflicts):\n"
            f"- Return a JSON array of at most {max_claims} objects with keys: claim_id (int), "
            "quote (ONE complete, self-contained sentence copied from the text, subject named; "
            "never a heading or fragment), claim_type (statistic|date|financial|technical|leadership|geography), "
            "search_query (neutral query naming the entity and the fact; no verdict words).\n"
            "- Cover the WHOLE document, every section and page. Prefer verifiable facts: numbers, dates, money, "
            "named roles, locations, launches, founding, acquisitions.\n"
            "- Include claims that look wrong or outdated. Do not invent claims.\n\n"
            f"DOCUMENT:\n{corpus[:20000]}"
        )
        data = call_json(gemini_api_key, prompt, temperature=0.1)
        items = data.get("claims", []) if isinstance(data, dict) else (data or [])
        for it in items:
            q = str(it.get("quote", "")).strip() if isinstance(it, dict) else ""
            if len(q.split()) >= 6:
                claims.append({"claim_id": 0, "quote": q,
                               "claim_type": it.get("claim_type", "statistic"),
                               "search_query": it.get("search_query") or clean_query(q)})
        if claims:
            STATUS["extract_mode"] = "llm"

    # Top up with regex claims the LLM skipped (keeps later sections covered)
    if len(claims) < max_claims:
        have = [c["quote"].lower() for c in claims]
        for c in regex_claims(pages_data, max_claims):
            if len(claims) >= max_claims:
                break
            low = c["quote"].lower()
            if not any(low[:40] in h or h[:40] in low for h in have):
                claims.append(c)
                have.append(low)

    claims = claims[:max_claims]
    for i, c in enumerate(claims):
        c["claim_id"] = i + 1
    return claims
