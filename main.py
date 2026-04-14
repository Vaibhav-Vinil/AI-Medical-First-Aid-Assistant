from dotenv import load_dotenv
from crew import medical_first_aid_crew

load_dotenv()

def run(user_input: str):
    result = medical_first_aid_crew.kickoff(inputs={"user_input": user_input})

    print("-"*50)
    print(result)
    print("-" * 50)

if __name__ == "__main__":
    user_input = (
        "My 60 year old Male collapsed and is clutching his chest. "
        "He says he is having severe chest pain. What should I do?"
    )

    run(user_input)
