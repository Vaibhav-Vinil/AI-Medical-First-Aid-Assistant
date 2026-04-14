import json
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# 1. Load Data
file_path = 'firstaidqa_v1.json'
if not os.path.exists(file_path):
    # Try one level up if not in current directory
    file_path = os.path.join(os.path.dirname(__file__), '..', 'firstaidqa_v1.json')

with open(file_path, 'r') as f:
    data = json.load(f)

documents = [
    Document(
        page_content=item['question'], 
        metadata={'answer': item['answer']}
    ) for item in data
]

# 2. Setup Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

# Create index if it doesn't exist (Serverless)
if index_name not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=384, # Match HuggingFace all-MiniLM-L6-v2 dimension
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

# 3. Embed and Upload
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = PineconeVectorStore.from_documents(
    documents, 
    embeddings, 
    index_name=index_name
)
print(f"Medical data ({len(documents)} documents) uploaded to Pinecone index '{index_name}'!")
