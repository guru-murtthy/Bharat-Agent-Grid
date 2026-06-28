"""Verifier agent: action-grounded anti-hallucination (Challenge 1 novelty).

No real-world action executes unless it is backed by a trusted, cited source.
"""
from __future__ import annotations

from src.contracts import ProposedAction, VerifierDecision


class Verifier:
    """Gate between planning and execution."""

    def verify(self, action: ProposedAction) -> tuple[VerifierDecision, str]:
        if not action.citations:
            return VerifierDecision.BLOCKED, "No supporting source: possible hallucination."

        if not any(c.trusted for c in action.citations):
            return VerifierDecision.BLOCKED, "No trusted source among citations."

        # High-stakes irreversible actions always require a human.
        if not action.reversible:
            return (
                VerifierDecision.NEEDS_HUMAN,
                "Irreversible action requires explicit human confirmation.",
            )

        return VerifierDecision.APPROVED, "Grounded in a trusted source and reversible."
