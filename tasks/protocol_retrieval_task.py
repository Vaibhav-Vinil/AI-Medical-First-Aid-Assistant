from crewai import Task
from agents.first_aid_protocol_agent import first_aid_protocol_agent
from tasks.intake_task import intake_task

protocol_retrieval_task = Task(
    agent=first_aid_protocol_agent,
    context=[intake_task],
    description=(
        "Using the symptom assessment from the previous task, search the medical "
        "first aid database using your Pinecone tool to query for relevant protocols.\n\n"
        "Use a single short query string (a few keywords or one brief phrase) per search—"
        "not long keyword lists or repeated wording.\n\n"
        "Retrieve the top matches that correspond to the triaged condition."
    ),
    expected_output=(
        "A list of relevant first aid procedures and protocols retrieved from the database."
    )
)
