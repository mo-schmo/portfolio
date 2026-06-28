"""FastAPI entrypoint for the Portfolio Oracles service."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .rate_limit import get_limiter
from .routes import clause, concierge, patent, tour
from .settings import get_settings

log = logging.getLogger("oracles")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if not settings.openrouter_api_key:
        log.warning(
            "OPENROUTER_API_KEY is empty; the service will start but model calls will fail."
        )

    # Warm the concierge RAG index in the background so the first user
    # query is fast. Failures are non-fatal - the route handles them.
    try:
        await concierge.warm_index()
    except Exception:
        log.exception("Failed to warm concierge index")

    yield


app = FastAPI(title="Hamza & Co. Oracles", version="0.1.0", lifespan=lifespan)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.method == "OPTIONS" or request.url.path in {"/", "/health"}:
        return await call_next(request)

    ip = request.client.host if request.client else "anon"
    if not get_limiter().allow(ip):
        return JSONResponse(
            {"error": "rate_limited", "message": "Too many requests. Try again shortly."},
            status_code=429,
        )
    return await call_next(request)


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "oracles", "status": "ok"}


@app.get("/health")
async def health() -> Response:
    return Response("OK", media_type="text/plain")


app.include_router(concierge.router, prefix="/agents/concierge", tags=["concierge"])
app.include_router(patent.router, prefix="/agents/patent", tags=["patent"])
app.include_router(tour.router, prefix="/agents/tour", tags=["tour"])
app.include_router(clause.router, prefix="/agents/clause", tags=["clause"])
