"""Grounding agent: returns verified source data for a task.

Hackathon scope uses a small in-memory verified-source store. In production this
becomes retrieval over government/health/financial source-of-truth APIs.
"""
from __future__ import annotations

from src.agents.base import Agent
from src.contracts import Citation, AgentResult, AgentTask

_VERIFIED_SOURCES: dict[str, Citation] = {
    "pmkisan": Citation(
        source_id="pmkisan",
        title="PM-KISAN Scheme Eligibility",
        url="https://pmkisan.gov.in",
        trusted=True,
        snippet="Landholding farmer families are eligible for income support.",
    ),
    "ayushman": Citation(
        source_id="ayushman",
        title="Ayushman Bharat (PM-JAY)",
        url="https://pmjay.gov.in",
        trusted=True,
        snippet="Eligible families get health cover up to a defined limit per year.",
    ),
    "hospital_slots": Citation(
        source_id="hospital_slots",
        title="District Hospital Appointment Registry",
        url="https://example-hospital.gov.in/slots",
        trusted=True,
        snippet="Live OPD appointment slots by department and date.",
    ),
}


def ground(source_id: str) -> Citation | None:
    """Return a verified citation for a source id, or None if unknown."""
    return _VERIFIED_SOURCES.get(source_id)


class GroundingAgent(Agent):
    name = "grounding_agent"
    domain = "grounding"

    def can_handle(self, task: AgentTask) -> bool:
        return task.intent == "ground_claim"

    def run(self, task: AgentTask) -> AgentResult:
        claim = task.params.get("claim", "")
        citation = ground(claim)
        if citation:
            return AgentResult(
                answer=f"Claim '{claim}' grounded in trusted source: {citation.title}.",
                citations=[citation]
            )
        return AgentResult(
            answer=f"Claim '{claim}' could not be grounded in any trusted sources.",
            citations=[]
        )
