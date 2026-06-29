"""Shared typed contracts passed between agents in the grid."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class VerifierDecision(str, Enum):
    APPROVED = "APPROVED"
    BLOCKED = "BLOCKED"
    NEEDS_HUMAN = "NEEDS_HUMAN"


@dataclass
class Citation:
    """A verified source backing a claim or action."""
    source_id: str
    title: str
    url: str
    trusted: bool
    snippet: str = ""


@dataclass
class AgentTask:
    """A single unit of work routed to a domain agent."""
    intent: str
    agent_name: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    language: str = "en"


@dataclass
class ProposedAction:
    """A real-world action an agent wants to perform, pending verification + consent."""
    description: str
    domain: str
    reversible: bool
    citations: list[Citation] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Output of a domain agent: a human-readable answer plus optional action."""
    answer: str
    citations: list[Citation] = field(default_factory=list)
    proposed_action: ProposedAction | None = None
