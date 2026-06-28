"""Tool registry for the Project Tour Guide.

The Tour Guide is a tool-using agent: rather than retrieving context up
front (like the Concierge), it decides *during* generation which records to
pull from the Go backend and calls these tools to fetch them.

Each tool exposes:
- an OpenAI/OpenRouter ``tools`` JSON Schema (see :data:`TOOL_SPECS`), and
- an async ``run`` coroutine that performs the HTTP call and returns a
  ``(result_payload, summary)`` tuple. ``result_payload`` is fed back to the
  model as the tool message; ``summary`` is a short human string streamed to
  the UI's tool trace.

Tools are intentionally read-only GETs against the public backend API.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

log = logging.getLogger(__name__)

# Maximum characters of project ``content`` we feed back to the model, so a
# very long case study doesn't blow the context budget on a single tool call.
_MAX_CONTENT_CHARS = 4000


def _parse_technologies(raw: Any) -> list[str]:
    """Backend stores technologies as a JSON-encoded string array; tolerate
    both a real list and (possibly double-encoded) JSON strings.
    """
    if isinstance(raw, list):
        return [str(t) for t in raw]
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, str):
                parsed = json.loads(parsed)
            if isinstance(parsed, list):
                return [str(t) for t in parsed]
        except (json.JSONDecodeError, TypeError):
            return [raw] if raw else []
    return []


async def get_project(backend_url: str, slug: str) -> tuple[dict[str, Any], str]:
    """Fetch a single project by slug from ``GET /api/projects/slug/{slug}``."""
    slug = (slug or "").strip()
    if not slug:
        return {"error": "A non-empty 'slug' is required."}, "Missing slug."

    async with httpx.AsyncClient(base_url=backend_url, timeout=10.0) as http:
        resp = await http.get(f"/api/projects/slug/{slug}")
        if resp.status_code == 404:
            return (
                {"error": f"No project found with slug '{slug}'."},
                f"No project found for '{slug}'.",
            )
        resp.raise_for_status()
        project = resp.json()

    content = (project.get("content") or "").strip()
    truncated = len(content) > _MAX_CONTENT_CHARS
    payload = {
        "slug": project.get("slug"),
        "title": project.get("title"),
        "description": project.get("description"),
        "technologies": _parse_technologies(project.get("technologies")),
        "content": content[:_MAX_CONTENT_CHARS],
        "content_truncated": truncated,
        "githubUrl": project.get("githubUrl") or project.get("github_url"),
        "liveUrl": project.get("liveUrl") or project.get("live_url"),
        "href": f"/projects/{project.get('slug')}",
    }
    title = payload["title"] or payload["slug"] or slug
    return payload, f"Retrieved project '{title}'."


async def list_related_blog(
    backend_url: str, query: str
) -> tuple[dict[str, Any], str]:
    """List blog posts related to ``query`` via simple keyword scoring.

    Pulls the full list from ``GET /api/blog`` and ranks by how many query
    terms appear in each post's title/excerpt/tags. Returns the top matches.
    """
    query = (query or "").strip()
    async with httpx.AsyncClient(base_url=backend_url, timeout=10.0) as http:
        resp = await http.get("/api/blog")
        resp.raise_for_status()
        posts = resp.json() or []

    terms = [t for t in query.lower().split() if len(t) > 2]

    scored: list[tuple[int, dict[str, Any]]] = []
    for post in posts:
        haystack = " ".join(
            str(post.get(field) or "")
            for field in ("title", "excerpt", "tags", "content")
        ).lower()
        score = sum(haystack.count(term) for term in terms) if terms else 0
        scored.append((score, post))

    # When no query terms match anything, fall back to returning recent posts
    # so the guide still has something to point at.
    scored.sort(key=lambda pair: pair[0], reverse=True)
    if terms and all(score == 0 for score, _ in scored):
        ranked = scored
    else:
        ranked = [pair for pair in scored if pair[0] > 0] or scored

    results = [
        {
            "slug": post.get("slug"),
            "title": post.get("title"),
            "excerpt": (post.get("excerpt") or "").strip()[:300],
            "href": f"/blog/{post.get('slug')}",
        }
        for _, post in ranked[:4]
    ]
    return (
        {"query": query, "results": results},
        f"Found {len(results)} related writing(s) for '{query}'."
        if query
        else f"Listed {len(results)} recent writing(s).",
    )


# OpenAI/OpenRouter tool specifications advertised to the model.
TOOL_SPECS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_project",
            "description": (
                "Fetch the full record for one portfolio project by its slug, "
                "including description, technologies, and case-study content. "
                "Use this whenever the visitor asks about a specific project."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "slug": {
                        "type": "string",
                        "description": "The project slug, e.g. 'portfolio' or 'churn-predictor'.",
                    }
                },
                "required": ["slug"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_related_blog",
            "description": (
                "Find blog posts/writings related to a topic or project by "
                "keyword. Use this to point the visitor at relevant writing."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Topic or keywords to search writings for.",
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]


async def dispatch(
    name: str, args: dict[str, Any], *, backend_url: str
) -> tuple[dict[str, Any], str]:
    """Route a tool call to its implementation.

    Returns ``(result_payload, summary)``. Errors are caught and returned as a
    structured payload so the model can recover gracefully rather than the
    whole stream dying.
    """
    try:
        if name == "get_project":
            return await get_project(backend_url, str(args.get("slug", "")))
        if name == "list_related_blog":
            return await list_related_blog(backend_url, str(args.get("query", "")))
        return {"error": f"Unknown tool '{name}'."}, f"Unknown tool '{name}'."
    except httpx.HTTPError as exc:
        log.exception("Tool %s failed", name)
        return (
            {"error": f"Backend request failed: {exc}"},
            f"Tool '{name}' failed to reach the backend.",
        )
