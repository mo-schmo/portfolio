package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"
	"portfolio-backend/internal/api"
	"portfolio-backend/internal/db"
	"portfolio-backend/internal/middleware"
	"portfolio-backend/internal/repository"
	"portfolio-backend/internal/service"

	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
)

func main() {
	// Initialize database
	databasePath := os.Getenv("DB_PATH")
	if databasePath == "" {
		databasePath = "portfolio.db"
	}

	sqliteDB, err := sql.Open("sqlite3", databasePath+"?_foreign_keys=1")
	if err != nil {
		log.Fatal("Failed to open database:", err)
	}
	defer sqliteDB.Close()

	// Run migrations
	if err := db.Migrate(sqliteDB); err != nil {
		log.Fatal("Failed to migrate database:", err)
	}

	// Initialize repositories
	blogRepo := repository.NewBlogRepository(sqliteDB)
	projectRepo := repository.NewProjectRepository(sqliteDB)

	// Initialize services
	blogService := service.NewBlogService(blogRepo)
	projectService := service.NewProjectService(projectRepo)

	// Initialize WebSocket hub
	wsHub := api.NewWebSocketHub()
	go wsHub.Run()

	// Initialize handlers
	blogHandler := api.NewBlogHandler(blogService, wsHub)
	projectHandler := api.NewProjectHandler(projectService, wsHub)

	// Setup router
	r := mux.NewRouter()

	// Apply middleware
	r.Use(middleware.Logging)
	r.Use(middleware.CORS)

	// API routes
	apiRouter := r.PathPrefix("/api").Subrouter()

	// Blog routes
	apiRouter.HandleFunc("/blog", blogHandler.GetAll).Methods("GET")
	apiRouter.HandleFunc("/blog/{id:[0-9]+}", blogHandler.GetByID).Methods("GET")
	apiRouter.HandleFunc("/blog/slug/{slug}", blogHandler.GetBySlug).Methods("GET")
	apiRouter.HandleFunc("/blog", blogHandler.Create).Methods("POST")
	apiRouter.HandleFunc("/blog/{id:[0-9]+}", blogHandler.Update).Methods("PUT")
	apiRouter.HandleFunc("/blog/{id:[0-9]+}", blogHandler.Delete).Methods("DELETE")

	// Project routes
	apiRouter.HandleFunc("/projects", projectHandler.GetAll).Methods("GET")
	apiRouter.HandleFunc("/projects/{id:[0-9]+}", projectHandler.GetByID).Methods("GET")
	apiRouter.HandleFunc("/projects/slug/{slug}", projectHandler.GetBySlug).Methods("GET")
	apiRouter.HandleFunc("/projects", projectHandler.Create).Methods("POST")
	apiRouter.HandleFunc("/projects/{id:[0-9]+}", projectHandler.Update).Methods("PUT")
	apiRouter.HandleFunc("/projects/{id:[0-9]+}", projectHandler.Delete).Methods("DELETE")

	// WebSocket route
	r.HandleFunc("/ws", wsHub.HandleWebSocket)

	// Health check
	r.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}).Methods("GET")

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}
