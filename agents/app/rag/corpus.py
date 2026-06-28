"""Build the searchable corpus from the Go backend.

The corpus is a list of ``Chunk`` records. Each chunk is small enough to
embed cheaply but long enough to carry context. Citations rendered in the
chat UI link back to ``href`` and display ``title``.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

import httpx

log = logging.getLogger(__name__)


@dataclass
class Chunk:
    id: str
    text: str
    title: str
    href: str
    source_type: str  # "resume" | "project" | "blog"


def _strip(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _chunk_text(text: str, max_chars: int = 1100) -> list[str]:
    """Split long text on paragraph boundaries; fall back to char windows."""
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    buf = ""
    for p in paragraphs:
        if not buf:
            buf = p
        elif len(buf) + 2 + len(p) <= max_chars:
            buf = f"{buf}\n\n{p}"
        else:
            chunks.append(buf)
            buf = p
    if buf:
        chunks.append(buf)

    # Hard-split any chunk still over the limit (e.g. a single very long para).
    final: list[str] = []
    for c in chunks:
        if len(c) <= max_chars:
            final.append(c)
            continue
        for i in range(0, len(c), max_chars):
            final.append(c[i : i + max_chars])
    return final


def _resume_chunks(resume: dict[str, Any]) -> list[Chunk]:
    chunks: list[Chunk] = []

    name = resume.get("name", "Mohammed Hamza")
    tagline = _strip(resume.get("tagline", ""))
    if tagline:
        chunks.append(
            Chunk(
                id="resume:tagline",
                text=f"{name} - {resume.get('title', '')}. {tagline}",
                title="Profile Summary",
                href="/",
                source_type="resume",
            )
        )

    statement = resume.get("statement") or []
    if statement:
        body = "\n\n".join(_strip(p) for p in statement)
        chunks.append(
            Chunk(
                id="resume:statement",
                text=f"Statement of Intent.\n\n{body}",
                title="Statement of Intent",
                href="/",
                source_type="resume",
            )
        )

    for i, exp in enumerate(resume.get("experience") or []):
        title = _strip(exp.get("title", ""))
        company = _strip(exp.get("company", ""))
        period = _strip(exp.get("period", ""))
        achievements = exp.get("achievements") or []
        body = "\n".join(f"- {_strip(a)}" for a in achievements)
        text = (
            f"Role: {title} at {company} ({period}).\n"
            f"Highlights:\n{body}"
        )
        chunks.append(
            Chunk(
                id=f"resume:experience:{i}",
                text=text,
                title=f"{title} - {company}",
                href="/",
                source_type="resume",
            )
        )

    for i, edu in enumerate(resume.get("education") or []):
        text = (
            f"{_strip(edu.get('degree', ''))} - {_strip(edu.get('institution', ''))} "
            f"({_strip(edu.get('period', ''))}). "
            f"{_strip(edu.get('concentration', ''))}. "
            f"{_strip(edu.get('location', ''))}."
        )
        chunks.append(
            Chunk(
                id=f"resume:education:{i}",
                text=text,
                title=_strip(edu.get("institution", "Education")),
                href="/",
                source_type="resume",
            )
        )

    skills = resume.get("skills") or {}
    if skills:
        body = "\n".join(
            f"{cat}: {', '.join(items)}" for cat, items in skills.items()
        )
        chunks.append(
            Chunk(
                id="resume:skills",
                text=f"Technical competencies.\n{body}",
                title="Technical Competencies",
                href="/",
                source_type="resume",
            )
        )

    return chunks


def _project_chunks(project: dict[str, Any]) -> list[Chunk]:
    slug = project.get("slug", "")
    title = _strip(project.get("title", "")) or slug
    description = _strip(project.get("description", ""))
    technologies = project.get("technologies")
    tech_str = ""
    if isinstance(technologies, str):
        # Backend stores tech as a JSON string array; tolerate both.
        try:
            import json

            parsed = json.loads(technologies)
            if isinstance(parsed, str):
                parsed = json.loads(parsed)
            if isinstance(parsed, list):
                tech_str = ", ".join(parsed)
        except Exception:
            tech_str = technologies
    elif isinstance(technologies, list):
        tech_str = ", ".join(str(t) for t in technologies)

    chunks: list[Chunk] = []
    overview = (
        f"Project: {title}.\n"
        f"Description: {description}\n"
        f"Technologies: {tech_str}"
    )
    chunks.append(
        Chunk(
            id=f"project:{slug}:overview",
            text=overview,
            title=title,
            href=f"/projects/{slug}",
            source_type="project",
        )
    )

    content_chunks = _chunk_text(project.get("content") or "")
    for i, c in enumerate(content_chunks):
        chunks.append(
            Chunk(
                id=f"project:{slug}:{i}",
                text=f"Project: {title} - case detail.\n{c}",
                title=title,
                href=f"/projects/{slug}",
                source_type="project",
            )
        )
    return chunks


def _blog_chunks(post: dict[str, Any]) -> list[Chunk]:
    slug = post.get("slug", "")
    title = _strip(post.get("title", "")) or slug
    excerpt = _strip(post.get("excerpt", ""))

    chunks: list[Chunk] = []
    chunks.append(
        Chunk(
            id=f"blog:{slug}:excerpt",
            text=f"Blog: {title}.\n{excerpt}",
            title=title,
            href=f"/blog/{slug}",
            source_type="blog",
        )
    )
    for i, c in enumerate(_chunk_text(post.get("content") or "")):
        chunks.append(
            Chunk(
                id=f"blog:{slug}:{i}",
                text=f"Blog: {title}.\n{c}",
                title=title,
                href=f"/blog/{slug}",
                source_type="blog",
            )
        )
    return chunks


async def build_corpus(backend_url: str) -> list[Chunk]:
    """Pull resume, projects, and blog posts from the Go backend.

    Failures on any one source are logged and skipped so the Concierge can
    serve from a partial corpus rather than refusing to start.
    """
    chunks: list[Chunk] = []
    async with httpx.AsyncClient(base_url=backend_url, timeout=10.0) as http:
        try:
            r = await http.get("/api/resume")
            r.raise_for_status()
            chunks.extend(_resume_chunks(r.json()))
        except Exception:
            log.exception("Failed to fetch resume from %s", backend_url)

        try:
            r = await http.get("/api/projects")
            r.raise_for_status()
            for project in r.json() or []:
                chunks.extend(_project_chunks(project))
        except Exception:
            log.exception("Failed to fetch projects from %s", backend_url)

        try:
            r = await http.get("/api/blog")
            r.raise_for_status()
            for post in r.json() or []:
                chunks.extend(_blog_chunks(post))
        except Exception:
            log.exception("Failed to fetch blog posts from %s", backend_url)

    log.info("Built corpus with %d chunks", len(chunks))
    return chunks
