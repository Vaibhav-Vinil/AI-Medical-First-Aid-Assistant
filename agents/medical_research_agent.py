from crewai import Agent, LLM
from tools.medical_research_tool import search_medical_research

llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0)

medical_research_agent = Agent(
    role="Medical Research Agent",
    goal="Verify first aid protocols and gather authoritative clinical guidelines.",
    backstory=(
        "You are a meticulous clinical researcher who verifies medical information. "
        "You check queried symptoms and suggested first aid responses against reliable sources "
        "like the Mayo Clinic, Red Cross, and CDC to ensure recommendations are accurate, up-to-date, "
        "and medically sound."
    ),
    tools=[search_medical_research],
    llm=llm,
    verbose=True,
)
