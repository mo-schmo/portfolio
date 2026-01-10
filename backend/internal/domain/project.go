package domain

import "time"

type Project struct {
	ID           int       `json:"id" db:"id"`
	Title        string    `json:"title" db:"title"`
	Slug         string    `json:"slug" db:"slug"`
	Description  string    `json:"description" db:"description"`
	Content      string    `json:"content" db:"content"`
	ImageURL     *string   `json:"imageUrl,omitempty" db:"image_url"`
	GithubURL    *string   `json:"githubUrl,omitempty" db:"github_url"`
	LiveURL      *string   `json:"liveUrl,omitempty" db:"live_url"`
	Technologies string    `json:"technologies" db:"technologies"` // JSON array stored as string
	Featured     bool      `json:"featured" db:"featured"`
	CreatedAt    time.Time `json:"createdAt" db:"created_at"`
	UpdatedAt    time.Time `json:"updatedAt" db:"updated_at"`
}

type CreateProjectRequest struct {
	Title        string   `json:"title"`
	Slug         string   `json:"slug"`
	Description  string   `json:"description"`
	Content      string   `json:"content"`
	ImageURL     *string  `json:"imageUrl,omitempty"`
	GithubURL    *string  `json:"githubUrl,omitempty"`
	LiveURL      *string  `json:"liveUrl,omitempty"`
	Technologies []string `json:"technologies"`
	Featured     bool     `json:"featured"`
}

type UpdateProjectRequest struct {
	Title        string   `json:"title"`
	Slug         string   `json:"slug"`
	Description  string   `json:"description"`
	Content      string   `json:"content"`
	ImageURL     *string  `json:"imageUrl,omitempty"`
	GithubURL    *string  `json:"githubUrl,omitempty"`
	LiveURL      *string  `json:"liveUrl,omitempty"`
	Technologies []string `json:"technologies"`
	Featured     bool     `json:"featured"`
}
