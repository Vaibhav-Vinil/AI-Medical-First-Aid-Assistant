"""Single Groq chat model for the first-aid crew (shared TPM bucket; pace via crew max_rpm)."""

from crewai import LLM

GROQ_CHAT_MODEL = "groq/llama-3.3-70b-versatile"


def groq_llm(*, temperature: float) -> LLM:
    return LLM(model=GROQ_CHAT_MODEL, temperature=temperature)
