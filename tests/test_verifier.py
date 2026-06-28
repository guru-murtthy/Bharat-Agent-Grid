from src.agents.verifier import Verifier
from src.contracts import Citation, ProposedAction, VerifierDecision


def _action(citations, reversible=True):
    return ProposedAction(
        description="do thing", domain="test", reversible=reversible, citations=citations
    )


def test_blocks_when_no_citations():
    decision, _ = Verifier().verify(_action([]))
    assert decision == VerifierDecision.BLOCKED


def test_blocks_when_no_trusted_source():
    c = Citation("x", "X", "http://x", trusted=False)
    decision, _ = Verifier().verify(_action([c]))
    assert decision == VerifierDecision.BLOCKED


def test_approves_grounded_reversible():
    c = Citation("x", "X", "http://x", trusted=True)
    decision, _ = Verifier().verify(_action([c], reversible=True))
    assert decision == VerifierDecision.APPROVED


def test_needs_human_for_irreversible():
    c = Citation("x", "X", "http://x", trusted=True)
    decision, _ = Verifier().verify(_action([c], reversible=False))
    assert decision == VerifierDecision.NEEDS_HUMAN
