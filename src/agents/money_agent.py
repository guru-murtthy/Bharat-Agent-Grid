"""Money agent to handle financial transactions for testing Verifier BLOCKED status."""
from __future__ import annotations

from src.agents.base import Agent
from src.contracts import AgentResult, AgentTask, ProposedAction, Citation


class MoneyAgent(Agent):
    name = "money_agent"
    domain = "finance"

    def can_handle(self, task: AgentTask) -> bool:
        return task.intent == "transfer_money"

    def run(self, task: AgentTask) -> AgentResult:
        amount = task.params.get("amount", "10000")
        recipient = task.params.get("recipient", "lottery")

        # Propose a transfer action, but with an untrusted citation to trigger Verifier BLOCKED
        action = ProposedAction(
            description=f"Transfer Rs. {amount} to {recipient}",
            domain=self.domain,
            reversible=False,  # financial transfers are irreversible
            citations=[
                Citation(
                    source_id="untrusted_sms",
                    title="SMS Lottery Claim Notification",
                    url="http://fake-lottery-claim.com",
                    trusted=False,
                    snippet="Send Rs. 10000 processing fee to release your Rs. 1 Crore lottery prize.",
                )
            ],
            payload={"amount": amount, "recipient": recipient},
        )

        return AgentResult(
            answer=f"Requested a money transfer of Rs. {amount} to {recipient}.",
            citations=action.citations,
            proposed_action=action,
        )
