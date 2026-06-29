"""Planner agent: turns a natural-language request into a structured plan.

Hackathon scope uses keyword intent detection. Replace with an LLM planner
that emits the same AgentTask list.
"""
from __future__ import annotations

from src.contracts import AgentTask


def plan(utterance: str, language: str = "en") -> list[AgentTask]:
    text = utterance.lower()
    tasks: list[AgentTask] = []

    # Check for applicant name in text to pass to SchemeAgent
    applicant = None
    for name in ("ramesh", "suresh", "anil", "vijay"):
        if name in text:
            applicant = name
            break

    if any(k in text for k in ("scheme", "pmkisan", "ayushman", "yojana", "\u092f\u094b\u091c\u0928\u093e")):
        intent = "apply_scheme" if "apply" in text or "\u0906\u0935\u0947\u0926\u0928" in text else "check_scheme"
        scheme = "ayushman" if "ayushman" in text or "health card" in text else "pmkisan"
        params = {"scheme": scheme}
        if applicant:
            params["applicant"] = applicant
        tasks.append(AgentTask(intent=intent, agent_name="scheme_agent", params=params, language=language))

    if any(k in text for k in ("hospital", "doctor", "appointment", "opd", "slot")):
        intent = "book_slot" if "book" in text else "find_slot"
        tasks.append(AgentTask(intent=intent, agent_name="hospital_agent", params={}, language=language))

    if any(k in text for k in ("transfer", "send", "money", "rupees", "rs", "cash", "lottery")):
        tasks.append(AgentTask(intent="transfer_money", agent_name="money_agent", params={"amount": "10000", "recipient": "lottery"}, language=language))

    if not tasks:
        params = {"scheme": "pmkisan"}
        if applicant:
            params["applicant"] = applicant
        tasks.append(AgentTask(intent="check_scheme", agent_name="scheme_agent", params=params, language=language))
    return tasks

