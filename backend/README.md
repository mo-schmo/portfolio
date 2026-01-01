# Portfolio Backend API

Golang REST API server with WebSocket support for the portfolio website.

## Features

- RESTful API for blog posts (CRUD operations)
- RESTful API for projects (CRUD operations)
- WebSocket server for real-time updates
- SQLite database (easily switchable to PostgreSQL)

## Getting Started

### Prerequisites

- Go 1.21 or higher (for local development)
- Docker and Docker Compose (for containerized deployment)

### Running with Docker (Recommended)

```bash
# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Running Locally

```bash
# Install dependencies
go mod download

# Run the server
go run cmd/server/main.go
```

### Building Docker Image

```bash
docker build -t portfolio-backend .
docker run -p 8080:8080 portfolio-backend
```

The server will start on port 8080 by default. Set the `PORT` environment variable to change it.

### Environment Variables

- `PORT` - Server port (default: 8080)
- `DB_PATH` - Database file path (default: portfolio.db, or /data/portfolio.db in Docker)

## API Endpoints

### Blog Posts

- `GET /api/blog` - List all blog posts
- `GET /api/blog/{id}` - Get blog post by ID
- `GET /api/blog/slug/{slug}` - Get blog post by slug
- `POST /api/blog` - Create blog post
- `PUT /api/blog/{id}` - Update blog post
- `DELETE /api/blog/{id}` - Delete blog post

### Projects

- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project by ID
- `POST /api/projects` - Create project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### WebSocket

- `WS /ws` - WebSocket endpoint for real-time updates

### Health Check

- `GET /health` - Server health check

## Architecture

The backend follows a clean architecture pattern:

- `cmd/server` - Application entry point
- `internal/api` - HTTP handlers
- `internal/domain` - Domain models
- `internal/repository` - Data access layer
- `internal/service` - Business logic
- `internal/middleware` - HTTP middleware
- `pkg/websocket` - WebSocket hub and client implementation

## Docker

The backend is containerized using a multi-stage Docker build:

- **Builder stage**: Compiles the Go application with CGO enabled (required for SQLite)
- **Runtime stage**: Uses lightweight Alpine Linux with only runtime dependencies

The Docker setup includes:
- Volume mounting for persistent database storage
- Environment variable configuration
- Port mapping for API access
