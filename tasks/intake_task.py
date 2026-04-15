from crewai import Task
from agents.triage_specialist_agent import triage_specialist_agent

intake_task = Task(
    agent=triage_specialist_agent,
    description=(
        "The user has submitted the following medical query or emergency situation:\n\n"
        "{user_input}\n\n"
        "Your job is to interpret the user's input and assess the symptoms. "
        "Classify the severity of the situation.\n\n"
        "EMERGENCY HEADER (STRICT): Put the exact line CALL EMERGENCY SERVICES as the first line "
        "ONLY if the user's message clearly reports chest pain, unconsciousness, not breathing, "
        "or an unambiguous equivalent (e.g. no pulse, not responsive, choking with inability to breathe). "
        "If none of those apply, do NOT use that phrase anywhere; start with a normal assessment heading instead."
    ),
    expected_output=(
        "A clear assessment of the reported symptoms, noting any Red Flags, and the overall severity."
    )
)
