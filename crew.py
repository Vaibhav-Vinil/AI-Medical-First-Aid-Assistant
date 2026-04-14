from crewai import Crew, Process

from agents.triage_specialist_agent import triage_specialist_agent
from agents.first_aid_protocol_agent import first_aid_protocol_agent
from agents.medical_research_agent import medical_research_agent
from agents.response_coordinator_agent import response_coordinator_agent

from tasks.intake_task import intake_task
from tasks.protocol_retrieval_task import protocol_retrieval_task
from tasks.clinical_verification_task import clinical_verification_task
from tasks.final_action_plan_task import final_action_plan_task

medical_first_aid_crew = Crew(
    agents=[triage_specialist_agent, first_aid_protocol_agent, medical_research_agent, response_coordinator_agent],
    tasks=[intake_task, protocol_retrieval_task, clinical_verification_task, final_action_plan_task],
    process=Process.sequential,
    verbose=True
)