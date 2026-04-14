import os
from dotenv import load_dotenv
from crewai.tools import tool
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

@tool("Medical First Aid Protocol Search Tool")
def search_medical_protocols(query: str) -> list[dict]:
    """
    Search Medical First Aid Pinecone vector database for protocols relevant to the input query.

    Args:
        query (str): User query in natural language detailing symptoms or an incident.

    Returns:
        list[dict]: List of matching first aid QA pairs and protocols.
    """
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

    top_k = 3
    docs = vectorstore.similarity_search(query, k=top_k)

    return [
        {
            "question": doc.page_content,
            "answer": doc.metadata.get("answer", "No specific output found in metadata.")
        }
        for doc in docs
    ]
