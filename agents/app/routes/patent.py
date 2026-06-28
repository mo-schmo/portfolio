"""Patent Compliance Bench - SSE endpoint that drives the LangGraph workflow.

Emits the following SSE event types (in order):

1. ``state``  { node, status: "running" }            -- before each node call
2. ``state``  { node, status: "done", summary }      -- after each node finishes
3. ``report`` { report: ComplianceReport, ... }      -- final memorandum payload
4. ``done``                                          -- terminator

We do not stream individual tokens here because each node returns
JSON-structured output that's only useful once complete. The timeline UI
on the frontend renders the ``state`` events as a court-reporter log.
"""

from __future__ import annotations

import logging
from typing import Any, AsyncIterator

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from ..graphs.patent import NODE_LABELS, get_graph, node_summary
from ..settings import get_settings
from ..sse import encode

log = logging.getLogger(__name__)

router = APIRouter()


class PatentRequest(BaseModel):
    draft: str = Field(..., min_length=20, max_length=20000)
    session_id: str | None = None


async def _event_stream(req: PatentRequest) -> AsyncIterator[dict[str, str]]:
    graph = get_graph()
    initial_state: dict[str, Any] = {"draft": req.draft, "iterations": 0}
    state: dict[str, Any] = dict(initial_state)

    seen_running: set[str] = set()
    final_report: dict[str, Any] | None = None
    final_revision: dict[str, Any] | None = None
    final_sections: dict[str, Any] | None = None

    try:
        # ``stream_mode="updates"`` yields ``{node_name: state_delta}`` after
        # each node executes. We synthesise a "running" event right before the
        # corresponding "done" so the timeline reads naturally.
        async for chunk in graph.astream(initial_state, stream_mode="updates"):
            for node, update in chunk.items():
                if node not in seen_running:
                    seen_running.add(node)
                    yield encode(
                        "state",
                        node=node,
                        label=NODE_LABELS.get(node, node.title()),
                        status="running",
                    )

                state.update(update or {})
                if "sections" in (update or {}):
                    final_sections = update["sections"]
                if "report" in (update or {}):
                    final_report = update["report"]
                if "revision" in (update or {}):
                    final_revision = update["revision"]

                yield encode(
                    "state",
                    node=node,
                    label=NODE_LABELS.get(node, node.title()),
                    status="done",
                    summary=node_summary(node, update or {}),
                )
                # The reviewer can run twice (initial + post-revision). Clear
                # ``seen_running`` for it so the second pass surfaces a fresh
                # "running" marker in the timeline.
                if node == "reviewer":
                    seen_running.discard("reviewer")

        yield encode(
            "report",
            sections=final_sections,
            report=final_report,
            revision=final_revision,
            iterations=int(state.get("iterations") or 0),
        )
    except Exception as exc:
        log.exception("Patent bench failed")
        yield encode("error", message=str(exc))
    finally:
        yield encode("done")


@router.post("/run")
async def run(req: PatentRequest) -> EventSourceResponse:
    return EventSourceResponse(_event_stream(req))


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "oracle": "patent",
        "model": get_settings().openrouter_model_smart,
        "nodes": list(NODE_LABELS.keys()),
    }
