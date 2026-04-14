# AI Medical First Aid Assistant (CrewAI)

An agentic AI assistant built with CrewAI and Streamlit designed to provide immediate, general first aid guidance. It uses an orchestrated pipeline of specialized AI agents to triage symptoms, fetch first aid protocols from a customized Pinecone vector database and generates a calm and actionable response.

## Architecture

This project utilizes a CrewAI multi-agent hierarchy:

1. **Triage Specialist Agent**: Analyzes user input to extract symptoms and check for life-threatening "Red Flags".
2. **First Aid Protocol Agent**: Retrieves specific first aid protocols from a custom Pinecone vector database using `all-MiniLM-L6-v2` embeddings.
3. **Medical Research Agent**: Verifies protocols via the Tavily Search API, restricted solely to trusted medical domains.
4. **Response Coordinator Agent**: Synthesizes a structured, step-by-step first aid plan, ensuring the mandatory medical disclaimer is heavily featured.

## Installation

1. Clone the repository
2. Install the necessary dependencies: `pip install -r requirements.txt`
3. Configure your environment variables in a `.env` file (see `env_template.txt` for the required keys: `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `TAVILY_API_KEY`, `GROQ_API_KEY`).
4. (Optional) Run `python scripts/upload_medical_data.py` to seed your Pinecone database with custom first aid Q&A pairs (dimension: 384).

## Running the Application

To interact with the assistant via the Streamlit web interface:

```bash
python -m streamlit run app.py
```

## Important Disclaimer

**This AI is not a doctor.** This tool is for informational/educational purposes only and should never replace professional medical advice. If you are experiencing a medical emergency, call your local emergency services immediately.