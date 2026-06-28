"""Project Tour Guide - placeholder, filled in during Phase 2."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def status() -> dict[str, str]:
    return {"oracle": "tour", "status": "scaffolded"}
