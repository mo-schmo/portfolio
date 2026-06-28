"""SSE helpers for streaming agent events to the browser.

We send JSON-encoded events with a ``type`` field. Event types:
- ``token``    : {"type":"token","text":"..."}
- ``tool_call``: {"type":"tool_call","tool":"...","args":{...},"id":"..."}
- ``tool_result``: {"type":"tool_result","tool":"...","ok":true,"summary":"..."}
- ``state``    : {"type":"state","node":"reviewer","status":"running"}
- ``citation`` : {"type":"citation","id":"project:foo","title":"Foo","href":"..."}
- ``message``  : {"type":"message","role":"assistant","content":"..."}
- ``error``    : {"type":"error","message":"..."}
- ``done``     : {"type":"done"}
"""

from __future__ import annotations

import json
from typing import Any, AsyncIterator


def encode(event_type: str, **payload: Any) -> dict[str, str]:
    """Build an ``EventSourceResponse``-compatible event dict."""
    data = {"type": event_type, **payload}
    return {"event": "message", "data": json.dumps(data, ensure_ascii=False)}


async def merge(*iters: AsyncIterator[dict[str, str]]) -> AsyncIterator[dict[str, str]]:
    """Sequentially yield from each async iterator (helper for compositions)."""
    for it in iters:
        async for item in it:
            yield item
