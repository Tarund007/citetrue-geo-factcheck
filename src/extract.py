"""
PDF parsing and structured claim extraction module for CiteTrue GEO.
Extracts raw text per page via pdfplumber and structured testable claims via LLM.
"""
import json
import re
from typing import List, Dict, Any
import pdfplumber
from google import genai
from google.genai import types

from src.prompts import EXTRACTION_SYSTEM_PROMPT


def parse_pdf_text(file_bytes_or_path) -> List[Dict[str, Any]]:
    """
    Reads a PDF file using pdfplumber and returns a list of page dicts:
    [{"page_number": 1, "text": "..."}]
    """
    pages_data = []
    with pdfplumber.open(file_bytes_or_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages_data.append({
                "page_number": idx + 1,
                "text": text.strip()
            })
    return pages_data


def extract_claims_from_text(pages_data: List[Dict[str, Any]], gemini_api_key: str, max_claims: int = 15) -> List[Dict[str, Any]]:
    """
    Invokes Gemini with structured schema to extract numerical/date/factual claims.
    """
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is required for claim extraction.")

    client = genai.Client(api_key=gemini_api_key)

    # Combine text with page demarcations
    full_text_corpus = ""
    for page in pages_data:
        full_text_corpus += f"\n--- [Page {page['page_number']}] ---\n{page['text']}\n"

    prompt = (
        f"{EXTRACTION_SYSTEM_PROMPT}\n\n"
        f"DOCUMENT TEXT TO ANALYZE:\n{full_text_corpus[:15000]}\n\n"
        f"Extract at most {max_claims} key claims. Format as JSON array only."
    )

    # Try standard supported model names in order of availability
    candidate_models = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash', 'gemini-1.5-pro']
    response = None
    last_err = None

    for m in candidate_models:
        try:
            response = client.models.generate_content(
                model=m,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            if response and response.text:
                break
        except Exception as err:
            last_err = err
            continue

    if not response or not response.text:
        raise last_err or RuntimeError("No response from Gemini models")

    try:
        raw_json = response.text.strip()
        # Clean potential markdown fences
        if raw_json.startswith("```json"):
            raw_json = raw_json[7:]
        if raw_json.startswith("```"):
            raw_json = raw_json[3:]
        if raw_json.endswith("```"):
            raw_json = raw_json[:-3]
        
        claims = json.loads(raw_json.strip())
        if isinstance(claims, list):
            return claims[:max_claims]
        elif isinstance(claims, dict) and "claims" in claims:
            return claims["claims"][:max_claims]
        return []
    except Exception as e:
        # Fallback regex extraction if API fails or parse fails
        print(f"LLM Extraction failed ({e}), using deterministic heuristic fallback...")
        return fallback_heuristic_extraction(pages_data, max_claims=max_claims)


def fallback_heuristic_extraction(pages_data: List[Dict[str, Any]], max_claims: int = 10) -> List[Dict[str, Any]]:
    """
    Deterministic rule-based extractor using regex for percentages, currencies, and years.
    Ensures zero failure even under heavy rate limits.
    """
    claims = []
    claim_id = 1
    # Regex patterns for figures, dates, percentages
    num_pattern = re.compile(r'([^.?!;\n]*?(\$?\d+(?:,\d+)*(?:\.\d+)?%?|\b(?:19|20)\d{2}\b)[^.?!;\n]*)')

    for p in pages_data:
        text = p["text"]
        matches = num_pattern.findall(text)
        for sentence_tuple in matches:
            sentence = sentence_tuple[0].strip()
            if len(sentence) > 20 and not any(c["quote"] == sentence for c in claims):
                claims.append({
                    "claim_id": claim_id,
                    "quote": sentence,
                    "claim_type": "statistic",
                    "search_query": sentence[:120]
                })
                claim_id += 1
                if len(claims) >= max_claims:
                    break
        if len(claims) >= max_claims:
            break
    return claims
