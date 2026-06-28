"""Project Tour Guide - a tool-using agent over the Go backend.

Unlike the Concierge (which retrieves context up front), the Tour Guide
decides *during* generation which records to pull and calls tools to fetch
them. This demonstrates an OpenRouter tool-calling loop:

1. The model streams an assistant turn.
2. If it requests tool calls, we emit ``tool_call`` events, run the tools
   (``app.tools.registry.dispatch``), emit ``tool_result`` events, append the
   results to the transcript, and re-invoke the model.
3. We repeat until the model answers without requesting tools (or we hit a
   safety cap on the number of tool rounds).

SSE event types emitted: ``token``, ``tool_call``, ``tool_result``,
``error``, ``done``.
"""

from __future__ import annotations

import json
import logging
from typing import Any, AsyncIterator

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from ..llm import stream_chat
from ..sessions import get_store
from ..settings import get_settings
from ..sse import encode
from ..tools.registry import TOOL_SPECS, dispatch

log = logging.getLogger(__name__)

router = APIRouter()

# Cap the number of tool-call rounds so a misbehaving model can't loop forever.
_MAX_TOOL_ROUNDS = 4


class TourRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None
    project_slug: str | None = Field(default=None, max_length=200)


SYSTEM_PROMPT = """You are the Project Tour Guide for Mohammed Hamza's
"Hamza & Co." portfolio - a refined, classical "Legacy Folio" archive of his
software and AI engineering work.

You walk visitors through Mohammed's projects and writings. You have tools to
fetch the live records and you SHOULD use them rather than guessing:

- ``get_project(slug)``: fetch a project's full record (description,
  technologies, case-study content).
- ``list_related_blog(query)``: find writings related to a topic or project.

Guidance:
- When a visitor asks about a specific project, call ``get_project`` first and
  ground your answer in what it returns. Cite the project by name.
- When relevant, surface related writings with ``list_related_blog``.
- If a tool returns an error or no record, say so plainly; do not invent
  details that are not in the retrieved records.
- Keep the archive's measured, classical tone: considered, concise, no
  marketing fluff, no emojis. Prefer 2-4 short paragraphs.
- Refer to him as "Mohammed" or "he"."""


def _short_history(
    transcript: list[dict[str, Any]], limit: int = 8
) -> list[dict[str, Any]]:
    """Keep only the most recent turns to stay within context budget.

    Only plain user/assistant text turns are persisted in the session
    transcript; the intermediate tool-call scaffolding lives only within a
    single request, so this is safe to replay verbatim.
    """
    return transcript[-limit:]


async def _event_stream(req: TourRequest) -> AsyncIterator[dict[str, str]]:
    settings = get_settings()
    store = get_store()
    session = store.get_or_create(req.session_id)
    transcript = session.history("tour")
    transcript.append({"role": "user", "content": req.message})

    system_content = SYSTEM_PROMPT
    if req.project_slug:
        # Anchor the conversation to a specific exhibit when launched from a
        # project page, so the first question is interpreted in context.
        system_content += (
            f"\n\nThe visitor is currently viewing the project with slug "
            f"'{req.project_slug}'. Treat ambiguous references to 'this "
            f"project' or 'it' as referring to that project, and consider "
            f"calling get_project('{req.project_slug}') to ground your reply."
        )

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_content},
        *_short_history(transcript),
    ]

    assistant_text_parts: list[str] = []
    try:
        for _round in range(_MAX_TOOL_ROUNDS + 1):
            tool_calls: list[dict[str, Any]] = []
            round_text_parts: list[str] = []

            async for event in stream_chat(
                model=settings.openrouter_model_fast,
                messages=messages,
                tools=TOOL_SPECS,
                temperature=0.4,
            ):
                if event.kind == "token" and event.text:
                    assistant_text_parts.append(event.text)
                    round_text_parts.append(event.text)
                    yield encode("token", text=event.text)
                elif event.kind == "tool_call":
                    tool_calls.append(
                        {
                            "id": event.tool_call_id or f"call_{len(tool_calls)}",
                            "name": event.tool_name or "",
                            "args": event.tool_args or {},
                        }
                    )
                elif event.kind == "finish":
                    break

            if not tool_calls:
                # The model produced a final answer with no further tool use.
                break

            # Record the assistant's tool-call turn so the follow-up request
            # has the full context the provider expects.
            messages.append(
                {
                    "role": "assistant",
                    "content": "".join(round_text_parts) or None,
                    "tool_calls": [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": json.dumps(tc["args"]),
                            },
                        }
                        for tc in tool_calls
                    ],
                }
            )

            for tc in tool_calls:
                yield encode(
                    "tool_call",
                    tool=tc["name"],
                    args=tc["args"],
                    id=tc["id"],
                )
                result, summary = await dispatch(
                    tc["name"], tc["args"], backend_url=settings.backend_url
                )
                ok = "error" not in result
                yield encode("tool_result", tool=tc["name"], ok=ok, summary=summary)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )
        else:
            # Exhausted the tool-round budget without a final answer.
            yield encode(
                "token",
                text="\n\n(The guide consulted the records repeatedly; "
                "please refine your question.)",
            )
    except Exception as exc:
        log.exception("Tour guide stream failed")
        yield encode("error", message=str(exc))
    finally:
        transcript.append(
            {"role": "assistant", "content": "".join(assistant_text_parts)}
        )
        yield encode("done")


@router.post("/chat")
async def chat(req: TourRequest) -> EventSourceResponse:
    return EventSourceResponse(_event_stream(req))


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "oracle": "tour",
        "model": get_settings().openrouter_model_fast,
        "tools": [spec["function"]["name"] for spec in TOOL_SPECS],
    }
