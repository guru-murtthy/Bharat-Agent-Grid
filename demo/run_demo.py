"""End-to-end demo for Bharat Agent Grid.

Run: python -m demo.run_demo

Shows: voice intake -> planner -> domain agents -> verifier -> consent ->
trust ledger -> proof-of-help card, across English / Hindi.
"""
from __future__ import annotations

from src.orchestrator.grid import Grid

UTTERANCES = [
    "I want to apply for the Ayushman health card and book a hospital appointment",
    "\u092e\u0941\u091d\u0947 \u092a\u0940\u090f\u092e \u0915\u093f\u0938\u093e\u0928 \u092f\u094b\u091c\u0928\u093e \u0915\u0940 \u091c\u093e\u0928\u0915\u093e\u0930\u0940 \u091a\u093e\u0939\u093f\u090f",
]


def main() -> None:
    for utterance in UTTERANCES:
        grid = Grid()
        print("=" * 70)
        print(f"USER: {utterance}")
        out = grid.handle(utterance)
        print(f"LANG: {out['language']}")
        print(f"REPLY: {out['spoken']}")
        print(f"LEDGER ENTRIES: {len(out['ledger'])}  CHAIN OK: {out['chain_ok']}")
        print(out["proof_of_help"])
    print("=" * 70)


if __name__ == "__main__":
    main()
