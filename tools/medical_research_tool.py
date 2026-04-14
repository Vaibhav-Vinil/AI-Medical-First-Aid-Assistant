import os
from dotenv import load_dotenv
from crewai.tools import tool
from tavily import TavilyClient

load_dotenv()

# Trusted medical domains
MEDICAL_SOURCES = [
    "mayoclinic.org",
    "redcross.org",
    "cdc.gov"
]

def _is_medical_source(url: str) -> bool:
    """Check if a URL belongs to one of the trusted medical domains."""
    return any(domain in url for domain in MEDICAL_SOURCES)

@tool("Medical Research Search Tool")
def search_medical_research(query: str) -> list[dict]:
    """
    Use Tavily Search to find medical first aid protocols and verification from authoritative sources.

    Args:
        query (str): The structured medical symptom or first aid query.

    Returns:
        list[dict]: Relevant guidelines, summaries, and links from trusted medical sources.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("❌ 'TAVILY_API_KEY' not found in .env file")

    client = TavilyClient(api_key=api_key)

    search_query = f"site:{' OR site:'.join(MEDICAL_SOURCES)} {query}"

    response = client.search(
        query=search_query,
        max_results=10
    )

    raw_results = response.get("results", [])
    medical_results = [
        {
            "title": item.get("title"),
            "summary": item.get("content"),
            "link": item.get("url")
        }
        for item in raw_results
        if _is_medical_source(item.get("url", ""))
    ]

    return medical_results if medical_results else [{
        "title": "No relevant medical records found",
        "summary": "No matching results found from trusted medical sources.",
        "link": None
    }]
