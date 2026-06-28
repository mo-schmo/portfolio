"""Tiny in-memory vector index over the portfolio corpus.

We use ``sentence-transformers`` (defaults to ``BAAI/bge-small-en-v1.5``) and
normalised embeddings so cosine similarity collapses to a dot product. The
corpus is small (<200 chunks), so storing the embedding matrix in numpy is
both fast and dependency-light.

The embedding model is loaded lazily on first build and reused across
queries. Encoding is offloaded to a worker thread so the FastAPI event loop
stays unblocked.
"""

from __future__ import annotations

import asyncio
import logging
import threading
from dataclasses import dataclass

import numpy as np

from .corpus import Chunk, build_corpus

log = logging.getLogger(__name__)

_model = None
_model_lock = threading.Lock()


def _get_model(name: str):
    """Lazy singleton sentence-transformer model."""
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer

                log.info("Loading embedding model: %s", name)
                _model = SentenceTransformer(name)
    return _model


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float


class VectorIndex:
    """Cosine-similarity index over portfolio chunks.

    Embeddings are stored as a float32 matrix of shape ``(N, D)`` with
    L2-normalised rows. ``search`` returns the top ``k`` rows by dot product.
    """

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.chunks: list[Chunk] = []
        self.embeddings: np.ndarray | None = None
        self._build_lock = asyncio.Lock()

    @property
    def ready(self) -> bool:
        return self.embeddings is not None and len(self.chunks) > 0

    async def build(self, backend_url: str) -> int:
        """Pull corpus from the backend and (re)compute the embedding matrix."""
        async with self._build_lock:
            chunks = await build_corpus(backend_url)
            if not chunks:
                log.warning("Corpus is empty; concierge will run ungrounded")
                self.chunks = []
                self.embeddings = None
                return 0

            texts = [c.text for c in chunks]
            embeddings = await asyncio.to_thread(self._encode, texts)
            self.chunks = chunks
            self.embeddings = embeddings.astype(np.float32, copy=False)
            log.info(
                "Index ready: %d chunks, %d-dim embeddings",
                len(self.chunks),
                self.embeddings.shape[1],
            )
            return len(self.chunks)

    async def search(self, query: str, *, k: int = 5) -> list[RetrievedChunk]:
        if not self.ready or self.embeddings is None:
            return []
        q = await asyncio.to_thread(self._encode, [query])
        scores = (self.embeddings @ q[0]).astype(float)
        top = np.argsort(-scores)[: max(k, 0)]
        return [
            RetrievedChunk(chunk=self.chunks[i], score=float(scores[i]))
            for i in top
        ]

    def _encode(self, texts: list[str]) -> np.ndarray:
        model = _get_model(self.model_name)
        return model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )


_index: VectorIndex | None = None


def get_index() -> VectorIndex:
    """Return the process-wide vector index, constructing it on first use."""
    global _index
    if _index is None:
        from ..settings import get_settings

        _index = VectorIndex(get_settings().embedding_model)
    return _index
