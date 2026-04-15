from crewai import Agent

from agents.groq_model import groq_llm
from agents.step_callback import agent_step_logger

llm = groq_llm(temperature=0)

triage_specialist_agent = Agent(
    role="Triage Specialist",
    goal=(
        "Assess the user's reported symptoms or emergency situation. "
        "Begin your answer with the exact line CALL EMERGENCY SERVICES only when the user clearly "
        "reports chest pain, unconsciousness, not breathing, or an unambiguous equivalent. "
        "Otherwise never use that line; give a standard triage assessment without it."
    ),
    backstory=(
        "You are a highly trained medical triage specialist. Your job is to swiftly and "
        "accurately assess symptoms reported in plain English, categorize the medical situation, "
        "and extract vital details to pass along to first aid and medical research teams. "
        "You always prioritize life-threatening conditions (Red Flags) above all else."
    ),
    llm=llm,
    tools=[],
    verbose=False,
    step_callback=agent_step_logger,
    max_rpm=10,
)
