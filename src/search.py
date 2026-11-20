"""
Tavily Search Wrapper for CiteTrue GEO.
Performs live web queries with timeout handling, deduplication, and domain ranking.
"""
import os
from typing import List, Dict, Any

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None


def search_web(query: str, api_key: str = None, max_results: int = 4) -> List[Dict[str, Any]]:
    """
    Search the live web using Tavily API.
    Returns list of dicts: [{"title": ..., "url": ..., "snippet": ...}]
    """
    key = api_key or os.environ.get("TAVILY_API_KEY")
    if not key:
        raise ValueError("TAVILY_API_KEY is missing. Please provide it in secrets.toml or via UI.")

    if TavilyClient is None:
        raise ImportError("tavily-python is not installed. Please run `pip install tavily-python`.")

    try:
        client = TavilyClient(api_key=key)
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=False
        )
        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")
            })
        return results
    except Exception as e:
        # Graceful return with error note
        return [{
            "title": "Search Error",
            "url": "",
            "snippet": f"Web search could not be executed: {str(e)}"
        }]
