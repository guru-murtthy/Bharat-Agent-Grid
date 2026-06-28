"""Trust Ledger: append-only, hash-chained, consent-gated, reversible audit log.

This is the signature primitive of Bharat Agent Grid. Every agent step, consent
prompt, verifier decision, and executed action is recorded as a tamper-evident
entry. Reversible actions register an undo handle.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

GENESIS_HASH = "0" * 64


@dataclass
class LedgerEntry:
    index: int
    timestamp: float
    actor: str
    action: str
    detail: dict[str, Any]
    consent: str  # "n/a" | "requested" | "granted" | "denied"
    reversible: bool
    prev_hash: str
    entry_hash: str = ""

    def compute_hash(self) -> str:
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "action": self.action,
            "detail": self.detail,
            "consent": self.consent,
            "reversible": self.reversible,
            "prev_hash": self.prev_hash,
        }
        raw = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()


@dataclass
class TrustLedger:
    entries: list[LedgerEntry] = field(default_factory=list)
    _undo_handles: dict[int, Callable[[], None]] = field(default_factory=dict)

    def _prev_hash(self) -> str:
        return self.entries[-1].entry_hash if self.entries else GENESIS_HASH

    def record(
        self,
        actor: str,
        action: str,
        detail: dict[str, Any] | None = None,
        consent: str = "n/a",
        reversible: bool = False,
        undo: Callable[[], None] | None = None,
    ) -> LedgerEntry:
        entry = LedgerEntry(
            index=len(self.entries),
            timestamp=time.time(),
            actor=actor,
            action=action,
            detail=detail or {},
            consent=consent,
            reversible=reversible,
            prev_hash=self._prev_hash(),
        )
        entry.entry_hash = entry.compute_hash()
        self.entries.append(entry)
        if reversible and undo is not None:
            self._undo_handles[entry.index] = undo
        return entry

    def undo(self, index: int) -> bool:
        """Reverse a reversible action and record the reversal."""
        handle = self._undo_handles.get(index)
        if handle is None:
            return False
        handle()
        self.record(
            actor="user",
            action="undo",
            detail={"reversed_entry": index},
            reversible=False,
        )
        del self._undo_handles[index]
        return True

    def verify_chain(self) -> bool:
        """Return True if the hash chain is intact (tamper-evident check)."""
        prev = GENESIS_HASH
        for e in self.entries:
            if e.prev_hash != prev or e.entry_hash != e.compute_hash():
                return False
            prev = e.entry_hash
        return True

    def export(self) -> list[dict[str, Any]]:
        return [asdict(e) for e in self.entries]
