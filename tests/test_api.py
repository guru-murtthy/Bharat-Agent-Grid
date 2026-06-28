from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_handle_endpoint():
    r = client.post("/handle", json={"text": "apply for ayushman", "consent": True})
    assert r.status_code == 200
    body = r.json()
    assert body["chain_ok"] is True
    assert "proof_of_help" in body
