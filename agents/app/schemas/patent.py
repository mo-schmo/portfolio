"""Pydantic schemas for the Patent Compliance Bench.

These are the JSON contracts that the Drafter, Reviewer, and Revisor agents
must conform to. They're shared between the LangGraph workflow and the
route handler that streams structured events to the browser.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["low", "medium", "high"]


class PatentSections(BaseModel):
    """Structured extraction of a draft patent application into its
    canonical sections. Empty strings are acceptable when the input draft
    omits a section.
    """

    title: str = Field("", description="The proposed title of the invention")
    abstract: str = Field("", description="The abstract paragraph")
    field_of_invention: str = Field("", description="Field of the invention")
    background: str = Field("", description="Background or prior art discussion")
    summary: str = Field("", description="Summary of the invention")
    detailed_description: str = Field("", description="Specification body")
    drawings_description: str = Field(
        "", description="Description of drawings (if any)"
    )
    claims: list[str] = Field(
        default_factory=list,
        description="Ordered list of claim texts, claim 1 first",
    )
    notes: str = Field(
        "",
        description="Short, candid notes from the Drafter about what was inferred or rearranged",
    )


class Finding(BaseModel):
    """One compliance finding raised by the Reviewer."""

    severity: Severity
    rule: str = Field(
        ...,
        description=(
            "Concise rule citation, e.g. '35 USC 112(b) - definiteness', "
            "'37 CFR 1.75 - claim form', or 'antecedent basis'."
        ),
    )
    location: str = Field(
        ...,
        description=(
            "Where in the draft the issue appears, e.g. 'Claim 1', "
            "'Abstract', 'Detailed description, paragraph 3'."
        ),
    )
    description: str = Field(
        ..., description="One- or two-sentence explanation of the issue."
    )
    recommendation: str = Field(
        ..., description="A concrete, actionable revision the Revisor can apply."
    )


class ComplianceReport(BaseModel):
    """The Reviewer's verdict on a draft patent application."""

    overall: Severity = Field(
        ..., description="Worst severity across all findings; 'low' if clean."
    )
    summary: str = Field(
        ...,
        description=(
            "Two- to four-sentence executive summary of the draft's compliance "
            "posture, written in the voice of a measured patent attorney."
        ),
    )
    findings: list[Finding] = Field(default_factory=list)


class RevisionResult(BaseModel):
    """What the Revisor returns after addressing high-severity findings."""

    revised_claims: list[str] = Field(default_factory=list)
    revised_abstract: str = Field("")
    change_log: list[str] = Field(
        default_factory=list,
        description="Brief notes for each material change the Revisor made.",
    )
