from src.trust_ledger.ledger import TrustLedger


def test_chain_integrity():
    led = TrustLedger()
    led.record("user", "utterance", {"text": "hi"})
    led.record("planner", "plan_created", {"steps": ["check_scheme"]})
    assert led.verify_chain() is True


def test_tamper_detected():
    led = TrustLedger()
    led.record("user", "utterance", {"text": "hi"})
    led.entries[0].detail["text"] = "tampered"
    assert led.verify_chain() is False


def test_undo_reversible_action():
    led = TrustLedger()
    state = {"booked": True}
    entry = led.record(
        "hospital_agent", "execute", {"action": "book"},
        consent="granted", reversible=True,
        undo=lambda: state.update(booked=False),
    )
    assert led.undo(entry.index) is True
    assert state["booked"] is False
    assert led.verify_chain() is True


def test_undo_nonexistent_returns_false():
    led = TrustLedger()
    assert led.undo(99) is False
