from crewai import Task
from agents.response_coordinator_agent import response_coordinator_agent
from tasks.intake_task import intake_task
from tasks.protocol_retrieval_task import protocol_retrieval_task
from tasks.clinical_verification_task import clinical_verification_task

final_action_plan_task = Task(
    agent=response_coordinator_agent,
    context=[intake_task, protocol_retrieval_task, clinical_verification_task],
    description=(
        "Based on the symptom assessment, retrieved protocols, and clinical verification, "
        "synthesize a final, easy-to-read, step-by-step action plan for the user.\n\n"
        "MANDATORY REQUIREMENT: Your final output MUST start with the EXACT following text:\n"
        "'DISCLAIMER: I am an AI assistant providing general first aid information. I am not a doctor. "
        "If this is a life-threatening emergency, call your local emergency number immediately.'"
    ),
    expected_output=(
        "DISCLAIMER: I am an AI assistant providing general first aid information. I am not a doctor. "
        "If this is a life-threatening emergency, call your local emergency number immediately.\n\n"
        "<Step-by-step clear action plan based on the assessment and verified protocols>"
    )
)
