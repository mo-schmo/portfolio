# Hamza & Co. - Software Engineering Portfolio

A prestigious, classical-styled portfolio website inspired by traditional legal archives and academic aesthetics. Built with a SvelteKit frontend, a Golang backend, and a Python FastAPI sidecar that hosts a series of agentic bots ("The Oracles") to showcase applied AI engineering.

## Tech Stack

### Frontend
- **SvelteKit** - Modern web framework
- **TailwindCSS** - Custom design system for the Legacy Folio aesthetic
- **TypeScript** - Type-safe development
- **Classical Design** - Mahogany, Parchment, and Brass color palette with elegant serif typography
- **Motion** - Subtle page-enter, ink-bloom hover, brass nav underlines, and typewriter cursor for streamed agent output (all respecting `prefers-reduced-motion`)

### Backend (Go)
- **Golang** - High-performance backend API
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Gorilla WebSocket** - Real-time WebSocket support
- **Gorilla Mux** - HTTP router
- **Clean Architecture** - Separation of concerns with domain, repository, service, and API layers

### Agents (Python)
- **FastAPI + uvicorn** - HTTP service for the agentic bots
- **OpenRouter** - Provider-agnostic LLM gateway (OpenAI-compatible)
- **sentence-transformers** - Local embeddings for the Concierge RAG index
- **LangGraph** - Multi-agent orchestration for the Patent Compliance Bench
- **Pydantic** - Structured-output schemas
- **SSE (sse-starlette)** - Streaming tokens, tool calls, and agent state to the browser

## Features

- **Admin CMS** - Full management system for projects and blogs with secure authentication
- **Archival Gallery** - Dynamic project showcase with a refined, tactile presentation
- **Legacy Blog** - A sophisticated journal system for technical thoughts and updates
- **Resume Portfolio** - Elegant display of experience, education, and skills using classical layout principles
- **The Oracles** - A `/oracles` chamber that introduces four agentic bots demonstrating retrieval, multi-agent deliberation, tool use, and structured output (UI scaffolded; bot logic in progress)
- **Real-time Notifications** - WebSocket integration for live system updates
- **Tactile UI** - Paper textures, ink-stamped elements, illuminated brass accents, and smooth classical transitions
- **Responsive Terminal** - Fully responsive dashboard for mobile and desktop management

## Project Structure

```
portfolio/
├── frontend/                       # SvelteKit application
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api/                # Backend + agents API clients
│   │   │   ├── components/         # Reusable UI components
│   │   │   │   └── oracle/         # OracleChat + ToolCallTrace (agent UI)
│   │   │   ├── content/resume.ts   # Typed resume (single source of truth)
│   │   │   └── stores/             # Auth, websocket, mock data
│   │   ├── routes/                 # SvelteKit routes
│   │   │   ├── admin/              # Admin CMS routes
│   │   │   └── oracles/            # The Oracles chamber
│   │   └── app.css                 # Legacy Folio theme + Oracle utilities
│   └── package.json
├── backend/                        # Golang API
│   ├── cmd/server/                 # Application entry point
│   ├── data/resume.json            # Resume served to the agents sidecar
│   ├── internal/
│   │   ├── api/                    # HTTP handlers (includes /api/resume)
│   │   ├── domain/                 # Domain models
│   │   ├── repository/             # Data access layer
│   │   ├── service/                # Business logic
│   │   ├── middleware/             # Auth, CORS, and logging middleware
│   │   └── db/                     # Database migrations
│   └── pkg/websocket/              # WebSocket implementation
├── agents/                         # Python FastAPI sidecar (The Oracles)
│   ├── app/
│   │   ├── main.py                 # FastAPI app, CORS, rate limiting
│   │   ├── llm.py                  # OpenRouter client + streaming helpers
│   │   ├── sessions.py             # In-memory session store
│   │   ├── sse.py                  # SSE event helpers
│   │   ├── rate_limit.py           # Per-IP sliding-window limiter
│   │   ├── settings.py             # Typed env-driven settings
│   │   └── routes/                 # Per-Oracle routers
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── docker-compose.yml              # backend + agents
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Go 1.21+ (for backend)
- Python 3.11+ (for the `agents/` sidecar; optional unless you're running the Oracles)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` (default SvelteKit port).

### Backend Setup

#### Option 1: Run with Docker (Recommended)

```bash
# From project root
docker-compose up --build

# Or from backend directory
cd backend
docker-compose up --build
```

#### Option 2: Run locally

```bash
cd backend
go mod download
go run cmd/server/main.go
```

The backend API will be available at `http://localhost:8080` by default.

### Agents Sidecar Setup

```bash
cd agents
python -m venv .venv
.venv\Scripts\Activate.ps1            # PowerShell on Windows
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
cp .env.example .env                   # then edit and set OPENROUTER_API_KEY
uvicorn app.main:app --reload --port 8001
```

Health check: <http://localhost:8001/health>. See [agents/README.md](agents/README.md) for route details.

### Environment Variables (Backend)

- `PORT` - Server port (default: 8080)
- `DB_PATH` - Database file path (default: portfolio.db)
- `RESUME_PATH` - Path to `resume.json` (default: `data/resume.json`)
- `ADMIN_USERNAME` - Admin login username (default: admin)
- `ADMIN_PASSWORD` - Admin login password (default: password)
- `JWT_SECRET` - Secret key for JWT signing

### Environment Variables (Agents)

- `OPENROUTER_API_KEY` - OpenRouter API key (required)
- `OPENROUTER_MODEL_FAST` - Fast model id (default: `openai/gpt-4o-mini`)
- `OPENROUTER_MODEL_SMART` - Smart model id (default: `anthropic/claude-3.5-sonnet`)
- `BACKEND_URL` - Where to reach the Go backend (default: `http://localhost:8080`)
- `ALLOWED_ORIGINS` - Comma-separated CORS origins
- `RATE_LIMIT_PER_MINUTE` - Per-IP rate limit (default: 20)
- `SESSION_TTL_SECONDS` - Idle session TTL (default: 3600)
- `EMBEDDING_MODEL` - sentence-transformers model id (default: `BAAI/bge-small-en-v1.5`)

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login to admin panel
- `POST /api/auth/logout` - Logout from admin panel
- `GET /api/auth/check` - Check current authentication status (Protected)

### Blog Posts
- `GET /api/blog` - List all blog posts
- `GET /api/blog/{id}` - Get blog post by ID
- `GET /api/blog/slug/{slug}` - Get blog post by slug
- `POST /api/blog` - Create blog post (Protected)
- `PUT /api/blog/{id}` - Update blog post (Protected)
- `DELETE /api/blog/{id}` - Delete blog post (Protected)

### Projects
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project by ID
- `GET /api/projects/slug/{slug}` - Get project by slug
- `POST /api/projects` - Create project (Protected)
- `PUT /api/projects/{id}` - Update project (Protected)
- `DELETE /api/projects/{id}` - Delete project (Protected)

### Resume
- `GET /api/resume` - Canonical resume JSON (used by both frontend and the agents sidecar)

### WebSocket
- `WS /ws` - WebSocket endpoint for real-time updates

### Health Check
- `GET /health` - Server health check

## Agents (Oracles) Endpoints

Hosted by the Python sidecar at port 8001. UI scaffolded; full bot implementations are landing next.

- `POST /agents/concierge/chat` - SSE stream, RAG over the portfolio
- `POST /agents/patent/run` - SSE stream, multi-agent compliance bench
- `POST /agents/tour/chat` - SSE stream, tool-using project tour guide
- `POST /agents/clause/explain` - JSON, structured clause explanation
- `GET /health` - Service health check

## Design Elements

The portfolio features a refined, classical aesthetic with:

- **Color Palette**: Rich Mahogany (#2d1b1b), aged Parchment (#fbf9f1), and warm Brass (#947a46)
- **Typography**: Elegant serifs (Playfair Display, PT Serif) with sophisticated tracking
- **Textural Detail**: Natural paper textures, ink-stamp effects, and subtle parchment gradients
- **UI Components**: "Legal folio" cards, tactile borders, and smooth academic transitions

## Go Skills Showcased

The backend demonstrates:

- RESTful API design with proper HTTP methods
- WebSocket implementation with hub pattern for real-time communication
- Database operations with SQLite (CRUD with transactions)
- Concurrent programming (goroutines for WebSocket message handling)
- Clean architecture with separation of concerns (domain, repository, service, API layers)
- Middleware pattern (CORS, logging, and JWT/Session authentication)
- Error handling best practices
- Structured logging

## AI / Agentic Skills Showcased

The agents sidecar will demonstrate (UI is in place, bot logic is the next milestone):

- Streaming token + tool-call SSE protocols designed for live agent UIs
- Provider-agnostic LLM access via OpenRouter (OpenAI-compatible)
- Local sentence-transformers embeddings paired with grounded generation
- LangGraph multi-agent orchestration with critique loops
- Pydantic-validated structured outputs for downstream UI rendering
- Per-IP rate limiting, typed settings, and in-memory session management

## Development

### Frontend Development

```bash
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Development

```bash
cd backend
go run cmd/server/main.go    # Run server
go test ./...                # Run tests
```

## License

This project is a personal portfolio website.
