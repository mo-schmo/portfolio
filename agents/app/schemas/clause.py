"""Pydantic schema for the Legal Clause Explainer.

This is the single-shot JSON contract the model must return. It mirrors the
``ClauseExplanation`` TypeScript interface in
``frontend/src/lib/api/agents.ts`` field-for-field.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["low", "medium", "high"]


class Obligation(BaseModel):
    """A duty the clause places on a particular party."""

    party: str = Field(
        ...,
        description="The party bound by the obligation, e.g. 'Licensee', 'Both parties'.",
    )
    obligation: str = Field(
        ..., description="What that party is required (or forbidden) to do."
    )


class Risk(BaseModel):
    """A risk or unfavourable exposure created by the clause."""

    severity: Severity = Field(
        ..., description="Relative severity of the risk: low, medium, or high."
    )
    description: str = Field(
        ..., description="A concise explanation of the risk and who it affects."
    )


class Redline(BaseModel):
    """A suggested edit to the clause language."""

    original: str = Field(
        ..., description="The original phrase or sentence being redlined."
    )
    suggestion: str = Field(
        ..., description="The proposed replacement language."
    )
    rationale: str = Field(
        ..., description="Why the change is recommended."
    )


class ClauseExplanation(BaseModel):
    """A structured, plain-English memorandum on a single contract clause."""

    clause_summary: str = Field(
        ...,
        description="A one-sentence summary of what the clause does.",
    )
    plain_english: str = Field(
        ...,
        description=(
            "A clear, plain-English explanation of the clause for a "
            "non-lawyer, in 2-4 sentences."
        ),
    )
    obligations: list[Obligation] = Field(
        default_factory=list,
        description="Enumerated obligations the clause imposes, by party.",
    )
    risks: list[Risk] = Field(
        default_factory=list,
        description="Risks or unfavourable exposures the clause creates.",
    )
    suggested_redlines: list[Redline] = Field(
        default_factory=list,
        description="Concrete suggested edits with rationale.",
    )
