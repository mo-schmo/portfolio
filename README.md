# Legacy Folio: Software Engineering Portfolio

A prestigious, classical-styled portfolio website inspired by traditional legal archives and academic aesthetics. Built with a SvelteKit frontend and Golang backend, it showcases professional engineering expertise through a refined, legacy-themed interface.

## Tech Stack

### Frontend
- **SvelteKit** - Modern web framework
- **TailwindCSS** - Custom design system for the Legacy Folio aesthetic
- **TypeScript** - Type-safe development
- **Classical Design** - Mahogany, Parchment, and Brass color palette with elegant serif typography

### Backend
- **Golang** - High-performance backend API
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Gorilla WebSocket** - Real-time WebSocket support
- **Gorilla Mux** - HTTP router
- **Clean Architecture** - Separation of concerns with domain, repository, service, and API layers

## Features

- **Admin CMS** - Full management system for projects and blogs with secure authentication
- **Archival Gallery** - Dynamic project showcase with a refined, tactile presentation
- **Legacy Blog** - A sophisticated journal system for technical thoughts and updates
- **Resume Portfolio** - Elegant display of experience, education, and skills using classical layout principles
- **Real-time Notifications** - WebSocket integration for live system updates
- **Tactile UI** - Paper textures, ink-stamped elements, and smooth classical transitions
- **Responsive Terminal** - Fully responsive dashboard for mobile and desktop management

## Project Structure

```
portfolio/
├── frontend/                 # SvelteKit application
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/   # Reusable UI components
│   │   │   ├── stores/       # Auth and data stores
│   │   ├── routes/           # SvelteKit routes
│   │   │   ├── admin/        # Admin CMS routes (Login, Dashboard, Editors)
│   │   └── app.css          # Cyberpunk theme styles
│   └── package.json
├── backend/                  # Golang API
│   ├── cmd/server/          # Application entry point
│   ├── internal/
│   │   ├── api/             # HTTP handlers
│   │   ├── domain/          # Domain models
│   │   ├── repository/      # Data access layer
│   │   ├── service/         # Business logic
│   │   ├── middleware/      # Auth, CORS, and logging middleware
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
- `ADMIN_USERNAME` - Admin login username (default: admin)
- `ADMIN_PASSWORD` - Admin login password (default: password)
- `JWT_SECRET` - Secret key for JWT signing

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

### WebSocket
- `WS /ws` - WebSocket endpoint for real-time updates

### Health Check
- `GET /health` - Server health check

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
