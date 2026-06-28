"""Thin OpenRouter client. OpenRouter is OpenAI-compatible, so we use the
official ``openai`` SDK with a custom ``base_url`` and the OpenRouter-specific
attribution headers.

This module exposes:
- ``get_client()``: returns a configured ``AsyncOpenAI`` instance.
- ``stream_chat(...)``: async generator yielding ``StreamEvent`` items
  (token deltas, tool calls, finish events).
- ``complete_json(...)``: helper that returns a parsed pydantic model using
  JSON-mode prompting (useful for the Clause Explainer and Patent Reviewer).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, AsyncIterator, Type, TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from .settings import get_settings

T = TypeVar("T", bound=BaseModel)

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    """Process-wide singleton OpenAI client pointed at OpenRouter."""
    global _client
    if _client is None:
        settings = get_settings()
        if not settings.openrouter_api_key:
            # Fail loudly here instead of letting OpenRouter return an opaque
            # 401 deep inside a streaming call. The most common cause is the
            # key not making it from `agents/.env.local` into the container
            # (check docker-compose `env_file`).
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. Populate it in agents/.env.local "
                "or export it in the shell before starting the agents service."
            )
        _client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
            default_headers={
                "HTTP-Referer": settings.openrouter_referer,
                "X-Title": settings.openrouter_app_title,
            },
        )
    return _client


@dataclass
class StreamEvent:
    """A single streamed event from the model.

    ``kind`` is one of:
        - ``"token"``: ``text`` carries the delta string.
        - ``"tool_call"``: ``tool_name`` and ``tool_args`` populated.
        - ``"finish"``: stream is over; ``finish_reason`` may be set.
    """

    kind: str
    text: str = ""
    tool_name: str | None = None
    tool_args: dict[str, Any] | None = None
    tool_call_id: str | None = None
    finish_reason: str | None = None


async def stream_chat(
    model: str,
    messages: list[dict[str, Any]],
    *,
    tools: list[dict[str, Any]] | None = None,
    temperature: float = 0.4,
    max_tokens: int | None = None,
) -> AsyncIterator[StreamEvent]:
    """Stream a chat completion, normalising deltas into ``StreamEvent``s.

    Tool calls arrive in chunks (name + args streamed separately) and are
    accumulated here so consumers see one complete ``tool_call`` event per call.
    """

    client = get_client()
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": temperature,
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    pending_tools: dict[int, dict[str, Any]] = {}

    stream = await client.chat.completions.create(**kwargs)
    async for chunk in stream:
        if not chunk.choices:
            continue
        choice = chunk.choices[0]
        delta = choice.delta

        if delta and delta.content:
            yield StreamEvent(kind="token", text=delta.content)

        if delta and getattr(delta, "tool_calls", None):
            for tc in delta.tool_calls:
                idx = tc.index if tc.index is not None else 0
                bucket = pending_tools.setdefault(
                    idx,
                    {"id": None, "name": "", "args": ""},
                )
                if tc.id:
                    bucket["id"] = tc.id
                if tc.function and tc.function.name:
                    bucket["name"] = tc.function.name
                if tc.function and tc.function.arguments:
                    bucket["args"] += tc.function.arguments

        if choice.finish_reason:
            for bucket in pending_tools.values():
                parsed: dict[str, Any]
                try:
                    parsed = json.loads(bucket["args"]) if bucket["args"] else {}
                except json.JSONDecodeError:
                    parsed = {"_raw": bucket["args"]}
                yield StreamEvent(
                    kind="tool_call",
                    tool_name=bucket["name"],
                    tool_args=parsed,
                    tool_call_id=bucket["id"],
                )
            pending_tools.clear()
            yield StreamEvent(kind="finish", finish_reason=choice.finish_reason)


async def complete_json(
    model: str,
    messages: list[dict[str, Any]],
    schema: Type[T],
    *,
    temperature: float = 0.2,
) -> T:
    """Single-shot completion that returns a parsed pydantic model.

    Uses OpenRouter's JSON-mode via ``response_format={"type": "json_object"}``.
    The caller's system prompt is responsible for describing the schema.
    """

    client = get_client()
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return schema.model_validate_json(content)
