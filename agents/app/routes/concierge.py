"""Portfolio Concierge - retrieval-augmented chat over the portfolio corpus.

Flow per request:
1. Look up (or create) the session and append the user message to its
   transcript.
2. Retrieve the top-k chunks for the user's message.
3. Emit ``citation`` SSE events for each retrieved chunk (so the UI can
   render citation chips while tokens are still streaming).
4. Build a grounded prompt with the citation ids inline.
5. Stream LLM tokens through ``app.llm.stream_chat``.
"""

from __future__ import annotations

import logging
from typing import Any, AsyncIterator

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from ..llm import stream_chat
from ..rag.index import get_index
from ..sessions import get_store
from ..settings import get_settings
from ..sse import encode

log = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None


SYSTEM_PROMPT = """You are the Portfolio Concierge for Mohammed Hamza's
"Hamza & Co." portfolio - a refined, classical "Legacy Folio" archive
showcasing his work as a software engineer with a growing focus on agentic
AI engineering.

You answer visitor questions about Mohammed's experience, projects, blog
posts, and skills using ONLY the context provided below. Each piece of
context is labelled with a citation id like [resume:experience:0] or
[project:foo:overview]. When you use information from a context block, cite
it inline using square brackets, e.g. "Mohammed led a GCP migration at Ford
Credit [resume:experience:0]."

Rules:
- If the answer isn't supported by the context, say so plainly and suggest
  where on the site a visitor might look (resume on the home page, projects
  in the Folio, writings in the Blog).
- Keep responses concise, considered, and in keeping with the archive's
  classical tone (no marketing fluff, no emojis).
- Prefer 2-4 short paragraphs. Use lists only when genuinely enumerative.
- Refer to him as "Mohammed" or "he" (first-person voice is reserved for him).
"""


async def warm_index() -> None:
    """Build the RAG index at server startup so the first user query is fast."""
    settings = get_settings()
    try:
        await get_index().build(settings.backend_url)
    except Exception:
        log.exception("Concierge index build failed; will retry on first query")


def _build_context(retrieved) -> tuple[str, list[dict[str, Any]]]:
    """Return (formatted context block, citation event payloads)."""
    if not retrieved:
        return "(no relevant context retrieved)", []

    seen: set[str] = set()
    blocks: list[str] = []
    citations: list[dict[str, Any]] = []
    for r in retrieved:
        c = r.chunk
        blocks.append(f"[{c.id}] ({c.source_type}) {c.title}\n{c.text}")
        # Surface one citation per source for the UI (collapse duplicates).
        key = c.href + "|" + c.title
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            {
                "id": c.id,
                "title": c.title,
                "href": c.href,
                "snippet": c.text[:240],
            }
        )
    return "\n\n---\n\n".join(blocks), citations


def _short_history(transcript: list[dict[str, Any]], limit: int = 6) -> list[dict[str, Any]]:
    """Keep only the most recent N turns to stay within context budget."""
    return transcript[-limit:]


async def _event_stream(req: ChatRequest) -> AsyncIterator[dict[str, str]]:
    settings = get_settings()
    store = get_store()
    session = store.get_or_create(req.session_id)
    transcript = session.history("concierge")
    transcript.append({"role": "user", "content": req.message})

    index = get_index()
    if not index.ready:
        # Lazy build if startup warmup didn't complete (e.g. backend offline at boot).
        try:
            await index.build(settings.backend_url)
        except Exception:
            log.exception("Lazy index build failed")

    retrieved = await index.search(req.message, k=5) if index.ready else []
    context_block, citations = _build_context(retrieved)
    for payload in citations:
        yield encode("citation", **payload)

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": (
                "Context from the portfolio archive (cite by id in [brackets]):\n\n"
                f"{context_block}"
            ),
        },
    ]
    messages.extend(_short_history(transcript))

    assistant_text_parts: list[str] = []
    try:
        async for event in stream_chat(
            model=settings.openrouter_model_fast,
            messages=messages,
            temperature=0.4,
        ):
            if event.kind == "token" and event.text:
                assistant_text_parts.append(event.text)
                yield encode("token", text=event.text)
            elif event.kind == "finish":
                break
    except Exception as exc:
        log.exception("Concierge stream failed")
        yield encode("error", message=str(exc))
    finally:
        transcript.append(
            {"role": "assistant", "content": "".join(assistant_text_parts)}
        )
        yield encode("done")


@router.post("/chat")
async def chat(req: ChatRequest) -> EventSourceResponse:
    return EventSourceResponse(_event_stream(req))


@router.get("/status")
async def status() -> dict[str, Any]:
    index = get_index()
    return {
        "oracle": "concierge",
        "ready": index.ready,
        "chunks": len(index.chunks),
        "model": get_settings().openrouter_model_fast,
    }
