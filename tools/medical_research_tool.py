import os
from typing import Annotated

from dotenv import load_dotenv
from pydantic import Field
from crewai.tools import tool
from tavily import TavilyClient

load_dotenv()

# Groq rejects oversized / repetitive tool-call JSON; keep schema and runtime bounded.
_MAX_QUERY_LEN = 200
_QUERY = Field(
    max_length=_MAX_QUERY_LEN,
    description=(
        "Concise search text only: 3-10 words or a short phrase. "
        "No comma lists, no repeated synonyms, no padding."
    ),
)

# Trusted medical domains
MEDICAL_SOURCES = [
    "mayoclinic.org",
    "redcross.org",
    "cdc.gov"
]

def _is_medical_source(url: str) -> bool:
    """Check if a URL belongs to one of the trusted medical domains."""
    return any(domain in url for domain in MEDICAL_SOURCES)


_MAX_TAVILY_RESULTS = 2
_MAX_TITLE_CHARS = 120
_MAX_SUMMARY_CHARS = 400


def _truncate(text: str | None, max_chars: int) -> str:
    if not text:
        return ""
    t = text.strip()
    if len(t) <= max_chars:
        return t
    return t[: max_chars - 3].rstrip() + "..."


@tool("Medical Research Search Tool")
def search_medical_research(query: Annotated[str, _QUERY]) -> list[dict]:
    """
    Use Tavily Search to find medical first aid protocols and verification from authoritative sources.

    Args:
        query: Short symptom or topic string (max ~200 characters). Example: "glass cut first aid splinter".

    Returns:
        list[dict]: Relevant guidelines, summaries, and links from trusted medical sources.
    """
    query = (query or "").strip()[:_MAX_QUERY_LEN]
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("❌ 'TAVILY_API_KEY' not found in .env file")

    client = TavilyClient(api_key=api_key)

    search_query = f"site:{' OR site:'.join(MEDICAL_SOURCES)} {query}"

    response = client.search(
        query=search_query,
        max_results=_MAX_TAVILY_RESULTS,
    )

    raw_results = response.get("results", [])
    medical_results = [
        {
            "title": _truncate(item.get("title"), _MAX_TITLE_CHARS),
            "summary": _truncate(item.get("content"), _MAX_SUMMARY_CHARS),
            "link": item.get("url"),
        }
        for item in raw_results
        if _is_medical_source(item.get("url", ""))
    ]

    return medical_results if medical_results else [{
        "title": "No relevant medical records found",
        "summary": "No matching results found from trusted medical sources.",
        "link": None
    }]
