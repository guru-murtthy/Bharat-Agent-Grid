"""Hospital appointment agent (Challenge 3 everyday impact)."""
from __future__ import annotations

from src.agents.base import Agent
from src.agents.grounding import ground
from src.contracts import AgentResult, AgentTask, ProposedAction


class HospitalAgent(Agent):
    name = "hospital_agent"
    domain = "hospital"

    def can_handle(self, task: AgentTask) -> bool:
        return task.intent in {"find_slot", "book_slot"}

    def run(self, task: AgentTask) -> AgentResult:
        citation = ground("hospital_slots")
        dept = task.params.get("department", "general medicine")
        date = task.params.get("date", "tomorrow")
        answer = f"A {dept} OPD slot is available for {date}."
        action = None
        if task.intent == "book_slot":
            action = ProposedAction(
                description=f"Book a {dept} OPD slot for {date}",
                domain=self.domain,
                reversible=True,  # bookings can be cancelled
                citations=[citation] if citation else [],
                payload={"department": dept, "date": date},
            )
        return AgentResult(
            answer=answer,
            citations=[citation] if citation else [],
            proposed_action=action,
        )
