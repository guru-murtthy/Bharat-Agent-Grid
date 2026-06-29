"""Trust-as-growth flywheel (Challenge 2).

Every successfully completed, verified task produces a shareable proof-of-help
card. Trust is the growth engine: family delegation + vernacular referral loop.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ProofOfHelpCard:
    task_summary: str
    verified: bool
    language: str
    referral_code: str

    def render(self) -> str:
        badge = "\u2705 Verified by Bharat Agent Grid" if self.verified else ""
        return (
            "--- Proof of Help ---\n"
            f"{self.task_summary}\n"
            f"{badge}\n"
            f"Help your family too: code {self.referral_code}\n"
            "---------------------"
        )


def make_card(task_summary: str, verified: bool, language: str, user_id: str) -> ProofOfHelpCard:
    referral_code = f"BAG-{abs(hash(user_id)) % 100000:05d}"
    return ProofOfHelpCard(task_summary, verified, language, referral_code)


def generate_proof_of_help_card_from_entry(entry: Any, language: str = "en") -> ProofOfHelpCard:
    """Generate a shareable Proof-of-Help card from a completed Trust Ledger execute entry."""
    if isinstance(entry, dict):
        actor = entry.get("actor", "agent")
        detail = entry.get("detail", {})
        index = entry.get("index", 0)
    else:
        actor = getattr(entry, "actor", "agent")
        detail = getattr(entry, "detail", {})
        index = getattr(entry, "index", 0)

    action_desc = detail.get("action", "Service executed")
    
    # Prettier agent titles
    agent_title = "Bharat Assistant"
    if actor == "scheme_agent":
        agent_title = "Govt Scheme Portal"
    elif actor == "hospital_agent":
        agent_title = "District OPD Registry"
    elif actor == "money_agent":
        agent_title = "Financial Services Gate"

    # Prettier summary
    if language == "hi":
        summary = f"सफलतापूर्वक पूरा किया गया: {action_desc} ({agent_title} द्वारा सत्यापित)"
    elif language == "kn":
        summary = f"ಯಶಸ್ವಿಯಾಗಿ ಪೂರ್ಣಗೊಂಡಿದೆ: {action_desc} ({agent_title} ರಿಂದ ಪರಿಶೀಲಿಸಲಾಗಿದೆ)"
    else:
        summary = f"Successfully Completed: {action_desc} (Verified via {agent_title})"

    # Referral code
    referral_code = f"BAG-{abs(hash(str(index))) % 100000:05d}"
    
    return ProofOfHelpCard(
        task_summary=summary,
        verified=True,
        language=language,
        referral_code=referral_code
    )
