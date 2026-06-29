"""Execution grid: routes tasks to agents, runs the verifier, gates on consent,
writes every step to the Trust Ledger, and emits a proof-of-help card.
"""
from __future__ import annotations

from typing import Callable

from src.agents.base import Agent
from src.agents.hospital_agent import HospitalAgent
from src.agents.scheme_agent import SchemeAgent
from src.agents.money_agent import MoneyAgent
from src.agents.grounding import GroundingAgent
from src.agents.verifier import Verifier
from src.contracts import AgentTask, VerifierDecision
from src.growth.proof_of_help import make_card, generate_proof_of_help_card_from_entry
from src.orchestrator.llm_planner import plan
from src.trust_ledger.ledger import TrustLedger
from src.voice import voice_io

ConsentFn = Callable[[str], bool]


def _auto_consent(_prompt: str) -> bool:
    """Default consent function for non-interactive demo runs."""
    return True


class Grid:
    def __init__(self, agents: list[Agent] | None = None) -> None:
        self.agents = agents or [SchemeAgent(), HospitalAgent(), MoneyAgent(), GroundingAgent()]
        self.verifier = Verifier()
        self.ledger = TrustLedger()

    def _route(self, task: AgentTask) -> Agent | None:
        if task.agent_name:
            for agent in self.agents:
                if agent.name == task.agent_name:
                    return agent
        for agent in self.agents:
            if agent.can_handle(task):
                return agent
        return None

    def _undo_action(self, agent_name: str, payload: dict) -> None:
        for agent in self.agents:
            if agent.name == agent_name:
                if hasattr(agent, "undo"):
                    agent.undo(payload)
                    return

    def handle(self, utterance: str, user_id: str = "demo-user", consent: ConsentFn = _auto_consent) -> dict:
        language = voice_io.detect_language(utterance)
        text = voice_io.speech_to_text(utterance, language)
        self.ledger.record("user", "utterance", {"text": text, "language": language})

        tasks = plan(text, language)
        self.ledger.record("planner", "plan_created", {"steps": [t.intent for t in tasks]})

        spoken: list[str] = []
        all_verified = True

        for task in tasks:
            agent = self._route(task)
            if agent is None:
                continue
            result = agent.run(task)
            self.ledger.record(agent.name, "result", {"answer": result.answer})
            spoken.append(result.answer)

            action = result.proposed_action
            if action is None:
                continue

            decision, reason = self.verifier.verify(action)
            self.ledger.record(
                "verifier", "decision", {"decision": decision.value, "reason": reason}
            )

            if decision == VerifierDecision.BLOCKED:
                all_verified = False
                spoken.append(f"I could not safely do that: {reason}")
                continue

            prompt = f"Do you approve: {action.description}?"
            self.ledger.record("system", "consent_prompt", {"prompt": prompt}, consent="requested")
            granted = consent(prompt)
            if not granted:
                self.ledger.record("user", "consent", {"prompt": prompt}, consent="denied")
                spoken.append("Okay, I did not proceed.")
                continue

            self.ledger.record("user", "consent", {"prompt": prompt}, consent="granted")
            
            # Execute state change on the agent if it has an execute method
            if hasattr(agent, "execute"):
                agent.execute(action.payload)

            entry = self.ledger.record(
                agent.name,
                "execute",
                {"action": action.description, "payload": action.payload},
                consent="granted",
                reversible=action.reversible,
                undo=lambda a_name=agent.name, p=action.payload: self._undo_action(a_name, p) if action.reversible else None,
            )
            spoken.append(
                f"Done: {action.description}."
                + (" You can undo this anytime." if action.reversible else "")
            )
            if action.reversible:
                self.ledger.record("system", "undo_available", {"entry": entry.index})

        summary = " ".join(spoken)
        
        # Try to find a successfully completed execute entry to generate the Proof-of-Help card
        exec_entry = None
        for e in self.ledger.entries:
            if e.action == "execute" and e.consent == "granted":
                exec_entry = e
                break

        if exec_entry:
            card = generate_proof_of_help_card_from_entry(exec_entry, language=language)
        else:
            card = make_card(summary, verified=all_verified, language=language, user_id=user_id)

        return {
            "language": language,
            "spoken": voice_io.text_to_speech(summary, language),
            "ledger": self.ledger.export(),
            "chain_ok": self.ledger.verify_chain(),
            "proof_of_help": card.render(),
        }
