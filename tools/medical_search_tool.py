import os
from typing import Annotated

from dotenv import load_dotenv
from pydantic import Field
from crewai.tools import tool
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

_MAX_QUERY_LEN = 200
# Keep tool payloads tiny: long Pinecone hits can blow context / cause flaky reruns.
_TOP_K = 1
_MAX_PAIR_CHARS = 500


def _truncate(text: str | None, max_chars: int) -> str:
    if not text:
        return ""
    t = text.strip()
    if len(t) <= max_chars:
        return t
    return t[: max_chars - 3].rstrip() + "..."


def _truncate_qa_pair(question: str | None, answer: str | None, max_total: int = _MAX_PAIR_CHARS) -> tuple[str, str]:
    """Cap combined question+answer length so the tool return stays ~max_total characters."""
    q = (question or "").strip()
    a = (answer or "").strip()
    if len(q) + len(a) <= max_total:
        return q, a
    if len(q) >= max_total:
        return _truncate(q, max_total), ""
    room = max_total - len(q)
    return q, _truncate(a, room)


_QUERY = Field(
    max_length=_MAX_QUERY_LEN,
    description=(
        "Concise search text only: 3-10 words or a short phrase. "
        "No comma lists, no repeated synonyms, no padding."
    ),
)


@tool("Medical First Aid Protocol Search Tool")
def search_medical_protocols(query: Annotated[str, _QUERY]) -> list[dict]:
    """
    Search Medical First Aid Pinecone vector database for protocols relevant to the input query.

    Args:
        query: Short description of symptoms or incident (max ~200 characters).

    Returns:
        list[dict]: Best matching first aid QA pairs (length capped; text truncated).
    """
    query = (query or "").strip()[:_MAX_QUERY_LEN]
    load_dotenv()

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")

    if not api_key or not index_name:
        raise EnvironmentError("❌ 'PINECONE_API_KEY' or 'PINECONE_INDEX_NAME' is not set in .env")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
        pinecone_api_key=api_key
    )

    docs = vectorstore.similarity_search(query, k=_TOP_K)

    out: list[dict[str, str]] = []
    for doc in docs:
        raw_a = doc.metadata.get("answer", "No specific output found in metadata.")
        q, a = _truncate_qa_pair(doc.page_content, raw_a if isinstance(raw_a, str) else str(raw_a))
        out.append({"question": q, "answer": a})
    return out
