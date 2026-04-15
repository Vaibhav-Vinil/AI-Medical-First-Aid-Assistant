from crewai import Agent

from agents.groq_model import groq_llm
from tools.medical_research_tool import search_medical_research

llm = groq_llm(temperature=0)

medical_research_agent = Agent(
    role="Medical Research Agent",
    goal="Verify first aid protocols and gather authoritative clinical guidelines.",
    backstory=(
        "You are a meticulous clinical researcher who verifies medical information. "
        "You check queried symptoms and suggested first aid responses against reliable sources "
        "like the Mayo Clinic, Red Cross, and CDC to ensure recommendations are accurate, up-to-date, "
        "and medically sound. When calling your search tool, you pass a single short query string "
        "(a few keywords or one short phrase)—never long keyword lists or repeated wording."
    ),
    tools=[search_medical_research],
    llm=llm,
    verbose=True,
    max_rpm=10,
)
