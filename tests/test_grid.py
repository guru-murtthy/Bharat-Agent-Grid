from src.orchestrator.grid import Grid


def test_end_to_end_scheme_and_hospital():
    out = Grid().handle("apply for ayushman and book a hospital appointment")
    assert out["chain_ok"] is True
    assert "Proof of Help" in out["proof_of_help"]
    actions = [e for e in out["ledger"] if e["action"] == "execute"]
    assert len(actions) >= 1


def test_consent_denied_blocks_execution():
    out = Grid().handle("apply for ayushman", consent=lambda _p: False)
    executed = [e for e in out["ledger"] if e["action"] == "execute"]
    assert executed == []


def test_hindi_detection():
    out = Grid().handle("\u092e\u0941\u091d\u0947 \u092f\u094b\u091c\u0928\u093e \u091a\u093e\u0939\u093f\u090f")
    assert out["language"] == "hi"


def test_blocked_action_triggers_verifier():
    out = Grid().handle("transfer money to claim a lottery")
    assert out["chain_ok"] is True
    decisions = [e for e in out["ledger"] if e["action"] == "decision"]
    assert len(decisions) >= 1
    assert decisions[0]["detail"]["decision"] == "BLOCKED"
    executed = [e for e in out["ledger"] if e["action"] == "execute"]
    assert executed == []
