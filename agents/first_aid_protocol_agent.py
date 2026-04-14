from crewai import Agent, LLM
from tools.medical_search_tool import search_medical_protocols

llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3)

first_aid_protocol_agent = Agent(
    role="First Aid Protocol Agent",
    goal="Retrieve the most relevant first aid protocols for the assessed symptoms.",
    backstory=(
        "You are an expert first responder who specializes in providing immediate, "
        "evidence-based first aid guidance. You map triaged symptoms directly to established "
        "medical protocols ensuring safety and effective initial care. You use the Pinecone "
        "medical vector database to retrieve official guidelines."
    ),
    tools=[search_medical_protocols],
    llm=llm,
    verbose=True,
)
