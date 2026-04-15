"""Lightweight stdout lines for agent steps (use with verbose=False to avoid banner spam)."""

from __future__ import annotations

from typing import Any

from crewai.agents.parser import AgentAction, AgentFinish

# CrewAI sets this when the LLM does not match ReAct "Thought:/Action:" markup but the
# raw text is still used as the answer — not an execution failure.
_PARSE_FALLBACK_THOUGHT = "Failed to parse LLM response"


def _display_thought_for_finish(thought: str) -> str:
    t = thought.replace("\n", " ").strip()
    if t == _PARSE_FALLBACK_THOUGHT or "Failed to parse LLM response" in t:
        return (
            "(plain-text answer; model did not use ReAct Thought/Action lines - OK)"
        )
    return t


def _format_finish_output(out: Any) -> str:
    """Full text for logs (no mid-sentence truncation)."""
    if isinstance(out, str):
        return out.strip()
    return str(out).strip()


def agent_step_logger(step_output: Any) -> None:
    """Print step updates; works with Streamlit stdout capture."""
    thought_raw = (getattr(step_output, "thought", None) or "").replace("\n", " ").strip()

    if isinstance(step_output, AgentFinish):
        thought = _display_thought_for_finish(thought_raw)
        out_text = _format_finish_output(step_output.output)
        print(f"[final] thought: {thought} | output: {out_text}")
        return

    thought = thought_raw

    if isinstance(step_output, AgentAction):
        tool_in = (step_output.tool_input or "").strip()
        print(
            f"[tool] {step_output.tool} | thought: {thought} | input: {tool_in}"
        )
        return

    print(f"[step] {step_output!r}")
