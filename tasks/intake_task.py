from crewai import Task
from agents.triage_specialist_agent import triage_specialist_agent

intake_task = Task(
    agent=triage_specialist_agent,
    description=(
        "The user has submitted the following medical query or emergency situation:\n\n"
        "{user_input}\n\n"
        "Your job is to interpret the user's input and assess the symptoms. "
        "Classify the severity of the situation. "
        "IMPORTANT: If the symptoms include 'chest pain', 'unconscious', or 'not breathing', "
        "you MUST output 'CALL EMERGENCY SERVICES' at the very top of your response."
    ),
    expected_output=(
        "A clear assessment of the reported symptoms, noting any Red Flags, and the overall severity."
    )
)
