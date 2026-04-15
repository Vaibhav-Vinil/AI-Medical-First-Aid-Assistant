from crewai import Agent

from agents.groq_model import groq_llm
from agents.step_callback import agent_step_logger
from tools.medical_search_tool import search_medical_protocols

llm = groq_llm(temperature=0.3)

first_aid_protocol_agent = Agent(
    role="First Aid Protocol Agent",
    goal="Retrieve the most relevant first aid protocols for the assessed symptoms.",
    backstory=(
        "You are an expert first responder who specializes in providing immediate, "
        "evidence-based first aid guidance. You map triaged symptoms directly to established "
        "medical protocols ensuring safety and effective initial care. You use the Pinecone "
        "medical vector database to retrieve official guidelines. When calling the search tool, "
        "you pass one short query (a few keywords or one brief phrase)—never long lists or repetition."
    ),
    tools=[search_medical_protocols],
    llm=llm,
    verbose=False,
    step_callback=agent_step_logger,
    max_rpm=10,
)
