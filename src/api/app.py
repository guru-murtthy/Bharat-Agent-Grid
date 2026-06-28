"""FastAPI backend for Bharat Agent Grid.

Endpoints:
  GET  /            -> serves the voice frontend
  GET  /health      -> liveness
  POST /handle      -> run a request end to end (returns reply, ledger, card)
  POST /undo        -> undo a reversible ledger entry

A single in-memory session grid is kept for the demo so /undo can act on the
last run. Production would key this by authenticated user/session.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.orchestrator.grid import Grid

app = FastAPI(title="Bharat Agent Grid")

_FRONTEND = Path(__file__).resolve().parents[2] / "frontend" / "index.html"

# Demo-scope single session grid (retains ledger for undo).
_grid = Grid()


class HandleRequest(BaseModel):
    text: str
    user_id: str = "demo-user"
    consent: bool = True


class UndoRequest(BaseModel):
    entry_index: int


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(str(_FRONTEND))


@app.post("/handle")
def handle(req: HandleRequest) -> dict:
    global _grid
    _grid = Grid()  # fresh ledger per request for a clean demo view
    return _grid.handle(req.text, user_id=req.user_id, consent=lambda _p: req.consent)


@app.post("/undo")
def undo(req: UndoRequest) -> dict:
    ok = _grid.ledger.undo(req.entry_index)
    return {
        "undone": ok,
        "ledger": _grid.ledger.export(),
        "chain_ok": _grid.ledger.verify_chain(),
    }
