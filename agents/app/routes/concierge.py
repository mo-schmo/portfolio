"""Portfolio Concierge - placeholder, filled in during Phase 1."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


async def warm_index() -> None:
    """No-op until the concierge RAG index is implemented."""
    return None


@router.get("/status")
async def status() -> dict[str, str]:
    return {"oracle": "concierge", "status": "scaffolded"}
