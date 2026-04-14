from crewai import Task
from agents.medical_research_agent import medical_research_agent
from tasks.intake_task import intake_task
from tasks.protocol_retrieval_task import protocol_retrieval_task

clinical_verification_task = Task(
    agent=medical_research_agent,
    context=[intake_task, protocol_retrieval_task],
    description=(
        "You are provided with the initial symptom triage and the retrieved first aid protocols. "
        "Use your web search tool to verify these protocols against authoritative sources "
        "(Mayo Clinic, Red Cross, CDC) to ensure the information is accurate and safe."
    ),
    expected_output=(
        "A verification report confirming the validity of the first aid steps, highlighting any necessary "
        "precautions or corrections based on authoritative medical guidelines."
    )
)
