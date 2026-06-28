"""Legal Clause Explainer - single-shot structured (JSON) output.

Given a contract clause, returns a ``ClauseExplanation`` produced by a single
``complete_json`` call against the smart model. There is no streaming and no
session state: the request is stateless and the response is a validated JSON
object the frontend renders as a two-pane "Memorandum of Counsel".
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..llm import complete_json
from ..schemas.clause import ClauseExplanation
from ..settings import get_settings

log = logging.getLogger(__name__)

router = APIRouter()


class ClauseRequest(BaseModel):
    clause: str = Field(..., min_length=10, max_length=8000)


SYSTEM_PROMPT = """You are a measured, plain-spoken contracts attorney. Given
a single contract clause, produce a ClauseExplanation JSON object that:

- ``clause_summary``: one sentence stating what the clause does.
- ``plain_english``: 2-4 sentences explaining it to a non-lawyer, without
  legalese.
- ``obligations``: enumerate each duty the clause imposes, naming the bound
  party (e.g. "Licensee", "Disclosing Party", "Both parties").
- ``risks``: flag risks or unfavourable exposures, each rated "low",
  "medium", or "high" severity.
- ``suggested_redlines``: concrete edits, each with the original phrase, a
  proposed replacement, and a short rationale. Return an empty list only if
  the clause is genuinely well-drafted and balanced.

Be specific and grounded in the clause text. Do not invent facts about the
broader agreement. This is an educational demonstration, not legal advice."""


@router.post("/explain")
async def explain(req: ClauseRequest) -> ClauseExplanation:
    settings = get_settings()
    try:
        return await complete_json(
            model=settings.openrouter_model_smart,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Explain the following contract clause. Respond with "
                        "ONLY the JSON object.\n\n"
                        f"--- CLAUSE START ---\n{req.clause}\n--- CLAUSE END ---"
                    ),
                },
            ],
            temperature=0.2,
            schema=ClauseExplanation,
        )
    except Exception as exc:
        log.exception("Clause explainer failed")
        raise HTTPException(
            status_code=502,
            detail=f"The clause explainer could not produce a memorandum: {exc}",
        ) from exc


@router.get("/status")
async def status() -> dict[str, str]:
    return {
        "oracle": "clause",
        "model": get_settings().openrouter_model_smart,
    }
