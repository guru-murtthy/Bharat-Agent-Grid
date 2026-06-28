"""Common agent interface so every agent is pluggable."""
from __future__ import annotations

from abc import ABC, abstractmethod

from src.contracts import AgentResult, AgentTask


class Agent(ABC):
    """Base class for all domain agents."""

    name: str = "agent"
    domain: str = "generic"

    @abstractmethod
    def can_handle(self, task: AgentTask) -> bool:
        """Return True if this agent can serve the given task intent."""

    @abstractmethod
    def run(self, task: AgentTask) -> AgentResult:
        """Execute the task and return a result (with optional proposed action)."""
