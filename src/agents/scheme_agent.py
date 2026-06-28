"""Government-scheme eligibility agent (Challenge 3 everyday impact)."""
from __future__ import annotations

from src.agents.base import Agent
from src.agents.grounding import ground
from src.contracts import AgentResult, AgentTask, ProposedAction


class SchemeAgent(Agent):
    name = "scheme_agent"
    domain = "govt_scheme"

    def can_handle(self, task: AgentTask) -> bool:
        return task.intent in {"check_scheme", "apply_scheme"}

    def run(self, task: AgentTask) -> AgentResult:
        scheme = task.params.get("scheme", "pmkisan")
        citation = ground(scheme)
        if citation is None:
            return AgentResult(answer=f"Unknown scheme '{scheme}'.")

        answer = f"You appear eligible for {citation.title}. {citation.snippet}"
        action = None
        if task.intent == "apply_scheme":
            action = ProposedAction(
                description=f"Submit an application for {citation.title}",
                domain=self.domain,
                reversible=True,  # draft application can be withdrawn
                citations=[citation],
                payload={"scheme": scheme, "applicant": task.params.get("applicant")},
            )
        return AgentResult(answer=answer, citations=[citation], proposed_action=action)
