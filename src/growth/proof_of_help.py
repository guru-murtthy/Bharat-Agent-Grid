"""Trust-as-growth flywheel (Challenge 2).

Every successfully completed, verified task produces a shareable proof-of-help
card. Trust is the growth engine: family delegation + vernacular referral loop.
"""
from __future__ import annotations

from dataclasses import dataclass


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
