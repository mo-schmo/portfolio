package db

import (
	"database/sql"
	"log"
)

func Migrate(db *sql.DB) error {
	// Create blog_posts table
	blogTable := `
	CREATE TABLE IF NOT EXISTS blog_posts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		slug TEXT NOT NULL UNIQUE,
		excerpt TEXT NOT NULL,
		content TEXT NOT NULL,
		published_at DATETIME NOT NULL,
		created_at DATETIME NOT NULL,
		updated_at DATETIME NOT NULL
	);
	`

	// Create projects table
	projectsTable := `
	CREATE TABLE IF NOT EXISTS projects (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		slug TEXT NOT NULL UNIQUE,
		description TEXT NOT NULL,
		content TEXT NOT NULL,
		image_url TEXT,
		github_url TEXT,
		live_url TEXT,
		technologies TEXT NOT NULL,
		featured BOOLEAN NOT NULL DEFAULT 0,
		created_at DATETIME NOT NULL,
		updated_at DATETIME NOT NULL
	);
	`

	if _, err := db.Exec(blogTable); err != nil {
		log.Printf("Error creating blog_posts table: %v", err)
		return err
	}

	if _, err := db.Exec(projectsTable); err != nil {
		log.Printf("Error creating projects table: %v", err)
		return err
	}

	// Ensure slug and content columns exist for existing tables
	_, _ = db.Exec("ALTER TABLE projects ADD COLUMN slug TEXT NOT NULL DEFAULT ''")
	_, _ = db.Exec("ALTER TABLE projects ADD COLUMN content TEXT NOT NULL DEFAULT ''")

	// Populate empty slugs for existing projects
	_, _ = db.Exec("UPDATE projects SET slug = lower(replace(title, ' ', '-')) WHERE slug = '' OR slug IS NULL")

	log.Println("Database migrations completed successfully")
	return nil
}
