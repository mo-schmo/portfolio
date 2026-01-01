# Cyberpunk Portfolio Website

A modern cyberpunk-styled portfolio website built with SvelteKit frontend and Golang backend, showcasing software engineering skills and projects.

## Tech Stack

### Frontend
- **SvelteKit** - Modern web framework
- **TailwindCSS** - Utility-first CSS with custom cyberpunk theme
- **TypeScript** - Type-safe development
- **Cyberpunk Design** - Neon colors, glitch effects, futuristic UI

### Backend
- **Golang** - High-performance backend API
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Gorilla WebSocket** - Real-time WebSocket support
- **Gorilla Mux** - HTTP router
- **Clean Architecture** - Separation of concerns with domain, repository, service, and API layers

## Features

- **Resume Display** - Beautiful presentation of experience, education, and skills
- **Blog System** - Full CRUD API for blog posts with real-time updates
- **Project Gallery** - Dynamic project showcase with filtering
- **Contact Form** - User-friendly contact interface
- **Real-time Updates** - WebSocket integration for live notifications
- **Cyberpunk Aesthetic** - Neon colors, animations, and futuristic design

## Project Structure

```
portfolio/
├── frontend/                 # SvelteKit application
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/   # Reusable UI components
│   │   │   ├── stores/       # Mock data stores
│   │   ├── routes/           # SvelteKit routes
│   │   └── app.css          # Cyberpunk theme styles
│   └── package.json
├── backend/                  # Golang API
│   ├── cmd/server/          # Application entry point
│   ├── internal/
│   │   ├── api/             # HTTP handlers
│   │   ├── domain/          # Domain models
│   │   ├── repository/      # Data access layer
│   │   ├── service/         # Business logic
│   │   ├── middleware/      # HTTP middleware
│   │   └── db/              # Database migrations
│   └── pkg/websocket/       # WebSocket implementation
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Go 1.21+ (for backend)

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

### Environment Variables (Backend)

- `PORT` - Server port (default: 8080)
- `DB_PATH` - Database file path (default: portfolio.db)

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

## Design Elements

The portfolio features a cyberpunk aesthetic with:

- **Color Palette**: Neon cyan (#00FFFF), hot pink (#FF00FF), electric blue (#0080FF) on dark backgrounds
- **Typography**: Futuristic fonts (Orbitron, Rajdhani) with neon text effects
- **Animations**: Glow effects, scanline overlays, hover transitions
- **UI Components**: Glassmorphism cards, neon borders, animated gradients

## Go Skills Showcased

The backend demonstrates:

- RESTful API design with proper HTTP methods
- WebSocket implementation with hub pattern for real-time communication
- Database operations with SQLite (CRUD with transactions)
- Concurrent programming (goroutines for WebSocket message handling)
- Clean architecture with separation of concerns (domain, repository, service, API layers)
- Middleware pattern (CORS, logging)
- Error handling best practices
- Structured logging

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
