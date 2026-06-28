# Portfolio Oracles

Python FastAPI sidecar that powers the four agentic bots on the portfolio.

## Run locally

```bash
cd agents
python -m venv .venv
.venv/Scripts/activate     # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env       # then edit and set OPENROUTER_API_KEY
uvicorn app.main:app --reload --port 8001
```

Health check: <http://localhost:8001/health>

## Routes

| Oracle           | Path                          | Notes                                |
| ---------------- | ----------------------------- | ------------------------------------ |
| Concierge        | `POST /agents/concierge/chat` | RAG over resume + projects + blog    |
| Patent Bench     | `POST /agents/patent/run`     | LangGraph multi-agent (drafter -> reviewer -> revisor) |
| Tour Guide       | `POST /agents/tour/chat`      | Tool-using agent with backend tools  |
| Clause Explainer | `POST /agents/clause/explain` | Single-shot structured output        |

All chat endpoints stream Server-Sent Events; the Clause Explainer returns plain JSON.

## Architecture

```
SvelteKit  ->  FastAPI  ->  OpenRouter (LLM)
              FastAPI  ->  Go backend (project/blog/resume)
              FastAPI  ---  in-memory vector store (sentence-transformers)
```

Embeddings are computed locally with `sentence-transformers/BAAI/bge-small-en-v1.5`
(downloaded once at container build time). The model can be swapped via the
`EMBEDDING_MODEL` env var.
