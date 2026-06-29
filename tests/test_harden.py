from src.orchestrator.grid import Grid
from src.contracts import AgentTask
from src.agents.scheme_agent import SchemeAgent
from src.agents.hospital_agent import HospitalAgent
from src.agents.grounding import GroundingAgent


def test_pm_kisan_eligibility_ramesh():
    agent = SchemeAgent()
    # Ramesh is eligible
    res = agent.run(AgentTask(intent="check_scheme", params={"scheme": "pmkisan", "applicant": "ramesh"}))
    assert "Eligible" in res.answer
    assert "Ramesh Kumar" in res.answer
    assert "ineligible" not in res.answer.lower()


def test_pm_kisan_eligibility_suresh():
    agent = SchemeAgent()
    # Suresh is landless -> ineligible
    res = agent.run(AgentTask(intent="check_scheme", params={"scheme": "pmkisan", "applicant": "suresh"}))
    assert "Ineligible" in res.answer
    assert "Suresh Patel" in res.answer
    assert "landless" in res.answer.lower()


def test_pm_kisan_eligibility_anil():
    agent = SchemeAgent()
    # Anil is tax payer -> ineligible
    res = agent.run(AgentTask(intent="check_scheme", params={"scheme": "pmkisan", "applicant": "anil"}))
    assert "Ineligible" in res.answer
    assert "Anil Sharma" in res.answer
    assert "income tax" in res.answer.lower()


def test_pm_kisan_eligibility_vijay():
    agent = SchemeAgent()
    # Vijay is govt employee -> ineligible
    res = agent.run(AgentTask(intent="check_scheme", params={"scheme": "pmkisan", "applicant": "vijay"}))
    assert "Ineligible" in res.answer
    assert "Vijay Singh" in res.answer
    assert "government employee" in res.answer.lower()


def test_hospital_booking_simulation_and_undo():
    grid = Grid()
    h_agent = [a for a in grid.agents if isinstance(a, HospitalAgent)][0]
    assert len(h_agent.booked_slots) == 0

    # Book slot
    out = grid.handle("book hospital slot")
    assert len(h_agent.booked_slots) == 1
    assert h_agent.booked_slots[0]["department"] == "General Medicine"

    # Undo slot
    exec_entry = [e for e in out["ledger"] if e["action"] == "execute" and e["reversible"]][0]
    ok = grid.ledger.undo(exec_entry["index"])
    assert ok is True
    assert len(h_agent.booked_slots) == 0


def test_grounding_agent():
    agent = GroundingAgent()
    # Ground PM-KISAN
    res = agent.run(AgentTask(intent="ground_claim", params={"claim": "pmkisan"}))
    assert "grounded in trusted source" in res.answer.lower()
    assert len(res.citations) == 1
    assert res.citations[0].source_id == "pmkisan"

    # Ground unknown
    res_unk = agent.run(AgentTask(intent="ground_claim", params={"claim": "unknown_claim"}))
    assert "could not be grounded" in res_unk.answer.lower()
    assert len(res_unk.citations) == 0
