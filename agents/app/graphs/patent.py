"""Patent Compliance Bench - a LangGraph workflow with three counsels.

Nodes
-----
- ``drafter``  : Parses the raw input draft into ``PatentSections`` so the
                 rest of the bench has a clean, addressable structure to
                 reason about.
- ``reviewer`` : Produces a ``ComplianceReport`` with severity-tiered
                 findings against well-known patent drafting rules
                 (35 USC 112 clarity / enablement / written description,
                 37 CFR 1.75 claim form, antecedent basis, single-sentence
                 claim form, etc.).
- ``revisor``  : If the report contains any HIGH severity findings AND we
                 haven't already revised once, propose a revision
                 addressing them, then loop back to the reviewer for a
                 second-look verdict.

The graph is compiled at import time; route handlers re-use it.
"""

from __future__ import annotations

import logging
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from ..llm import complete_json
from ..schemas.patent import (
    ComplianceReport,
    Finding,
    PatentSections,
    RevisionResult,
)
from ..settings import get_settings

log = logging.getLogger(__name__)


class PatentState(TypedDict, total=False):
    draft: str
    sections: dict[str, Any]
    report: dict[str, Any]
    revision: dict[str, Any]
    iterations: int


# ---------------------------------------------------------------------------
# Node prompts
# ---------------------------------------------------------------------------

_DRAFTER_SYSTEM = """You are a meticulous patent paralegal. Given a raw
patent application draft, extract its canonical sections into the requested
JSON schema. Preserve the applicant's language whenever possible; do NOT
rewrite content here. If a section is missing, leave the field as an empty
string (or empty list for claims). The ``notes`` field is for your candid
short note on what was inferred or rearranged."""

_REVIEWER_SYSTEM = """You are a measured, senior patent attorney sitting in
compliance review of a draft US utility patent application. Produce a
ComplianceReport JSON object identifying issues against well-known rules,
including (non-exhaustively):

- 35 USC 112(a): written description, enablement.
- 35 USC 112(b): definiteness ("particularly pointing out and distinctly claiming").
- 35 USC 112(d)-(f): dependent claim form, means-plus-function constructions.
- 37 CFR 1.75: claim format, single-sentence claim form, dependency.
- Antecedent basis: every "the X" must have a prior "an X" in the same claim chain.
- Claim 1 should be the broadest independent claim.
- Abstract length and content (no purely promotional language; <=150 words).
- Drawings referenced in the specification should be described.

Rate each finding's severity as "low", "medium", or "high" and propose a
concrete, applicable recommendation. Set ``overall`` to the worst severity.
The ``summary`` is a 2-4 sentence executive synopsis in the voice of a
measured attorney. Be specific, professional, and constructive."""

_REVISOR_SYSTEM = """You are a patent attorney revising a draft to address
HIGH severity compliance findings only. Output a RevisionResult JSON with:
- ``revised_claims``: the full revised claim set (independent and dependent),
  fixing antecedent basis, definiteness, and claim form issues raised.
- ``revised_abstract``: a revised abstract if one was flagged, else "".
- ``change_log``: brief notes (one item per material change) explaining what
  changed and why, citing the finding it addresses.

Do not invent new substantive technical matter; stay within the scope of
the draft. Keep the applicant's terminology where compliant."""


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------


def _model_for_node() -> str:
    return get_settings().openrouter_model_smart


async def drafter(state: PatentState) -> PatentState:
    draft = state.get("draft", "") or ""
    sections = await complete_json(
        model=_model_for_node(),
        messages=[
            {"role": "system", "content": _DRAFTER_SYSTEM},
            {
                "role": "user",
                "content": (
                    "Extract the following draft into the PatentSections JSON schema. "
                    "Respond with ONLY the JSON object.\n\n"
                    f"--- DRAFT START ---\n{draft}\n--- DRAFT END ---"
                ),
            },
        ],
        schema=PatentSections,
        temperature=0.1,
    )
    return {"sections": sections.model_dump()}


async def reviewer(state: PatentState) -> PatentState:
    sections = state.get("sections") or {}
    revision = state.get("revision") or {}

    payload = {"sections": sections}
    if revision:
        payload["proposed_revision"] = revision

    report = await complete_json(
        model=_model_for_node(),
        messages=[
            {"role": "system", "content": _REVIEWER_SYSTEM},
            {
                "role": "user",
                "content": (
                    "Review the following draft sections (and any proposed revision) "
                    "and produce a ComplianceReport. Respond with ONLY the JSON object.\n\n"
                    f"{payload}"
                ),
            },
        ],
        schema=ComplianceReport,
        temperature=0.2,
    )
    return {"report": report.model_dump()}


async def revisor(state: PatentState) -> PatentState:
    sections = state.get("sections") or {}
    report = state.get("report") or {}
    iterations = int(state.get("iterations") or 0)

    revision = await complete_json(
        model=_model_for_node(),
        messages=[
            {"role": "system", "content": _REVISOR_SYSTEM},
            {
                "role": "user",
                "content": (
                    "Address the HIGH severity findings in the report below by "
                    "revising the claims (and abstract if flagged). Respond with "
                    "ONLY the JSON object.\n\n"
                    f"SECTIONS:\n{sections}\n\nREPORT:\n{report}"
                ),
            },
        ],
        schema=RevisionResult,
        temperature=0.2,
    )
    return {
        "revision": revision.model_dump(),
        "iterations": iterations + 1,
    }


# ---------------------------------------------------------------------------
# Edges
# ---------------------------------------------------------------------------


def _should_revise(state: PatentState) -> str:
    report = state.get("report") or {}
    findings: list[dict[str, Any]] = report.get("findings", []) or []
    has_high = any(
        (f.get("severity") or "").lower() == "high" for f in findings
    )
    iterations = int(state.get("iterations") or 0)
    if has_high and iterations < 1:
        return "revisor"
    return END


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------


def _build_graph():
    graph: StateGraph = StateGraph(PatentState)
    graph.add_node("drafter", drafter)
    graph.add_node("reviewer", reviewer)
    graph.add_node("revisor", revisor)
    graph.set_entry_point("drafter")
    graph.add_edge("drafter", "reviewer")
    graph.add_conditional_edges(
        "reviewer", _should_revise, {"revisor": "revisor", END: END}
    )
    graph.add_edge("revisor", "reviewer")
    return graph.compile()


_compiled = None


def get_graph():
    """Lazily compile the graph the first time it's needed."""
    global _compiled
    if _compiled is None:
        _compiled = _build_graph()
    return _compiled


# Friendly labels for the timeline UI.
NODE_LABELS = {
    "drafter": "Drafter",
    "reviewer": "Reviewer",
    "revisor": "Revisor",
}


def node_summary(node: str, update: dict[str, Any]) -> str:
    """Render a one-line human summary of what a node produced.

    Streamed to the UI so the timeline reads like a court reporter's log.
    """
    if node == "drafter":
        sections = update.get("sections") or {}
        claim_count = len(sections.get("claims") or [])
        title = (sections.get("title") or "").strip() or "untitled draft"
        return f"Parsed draft '{title}' into structured sections ({claim_count} claims)."
    if node == "reviewer":
        report = update.get("report") or {}
        findings = report.get("findings") or []
        overall = (report.get("overall") or "").lower() or "unknown"
        high = sum(
            1 for f in findings if (f.get("severity") or "").lower() == "high"
        )
        return (
            f"Compliance review complete. {len(findings)} findings "
            f"({high} high). Overall: {overall.upper()}."
        )
    if node == "revisor":
        rev = update.get("revision") or {}
        n_changes = len(rev.get("change_log") or [])
        return f"Revision proposed addressing high-severity findings ({n_changes} changes)."
    return f"Updated state from {node}."


__all__ = [
    "ComplianceReport",
    "Finding",
    "NODE_LABELS",
    "PatentSections",
    "RevisionResult",
    "get_graph",
    "node_summary",
]
