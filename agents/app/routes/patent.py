"""Patent Compliance Bench - placeholder, filled in during Phase 1."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def status() -> dict[str, str]:
    return {"oracle": "patent", "status": "scaffolded"}
