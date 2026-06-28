"""In-memory session store with idle TTL.

Suitable for a single-process portfolio demo. Each session keeps a short
rolling transcript per bot.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from threading import Lock
from typing import Any


@dataclass
class Session:
    id: str
    created_at: float
    last_active: float
    # Per-bot transcripts: ``{ "concierge": [ {role, content}, ... ] }``
    transcripts: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    def touch(self) -> None:
        self.last_active = time.time()

    def history(self, bot: str) -> list[dict[str, Any]]:
        return self.transcripts.setdefault(bot, [])


class SessionStore:
    def __init__(self, ttl_seconds: int) -> None:
        self._ttl = ttl_seconds
        self._sessions: dict[str, Session] = {}
        self._lock = Lock()

    def get_or_create(self, session_id: str | None) -> Session:
        now = time.time()
        with self._lock:
            self._evict_locked(now)
            if session_id and session_id in self._sessions:
                session = self._sessions[session_id]
                session.touch()
                return session
            new_id = session_id or uuid.uuid4().hex
            session = Session(id=new_id, created_at=now, last_active=now)
            self._sessions[new_id] = session
            return session

    def _evict_locked(self, now: float) -> None:
        cutoff = now - self._ttl
        expired = [sid for sid, s in self._sessions.items() if s.last_active < cutoff]
        for sid in expired:
            self._sessions.pop(sid, None)


_store: SessionStore | None = None


def get_store() -> SessionStore:
    global _store
    if _store is None:
        from .settings import get_settings

        _store = SessionStore(get_settings().session_ttl_seconds)
    return _store
