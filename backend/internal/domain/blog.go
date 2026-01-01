package domain

import "time"

type BlogPost struct {
	ID          int       `json:"id" db:"id"`
	Title       string    `json:"title" db:"title"`
	Slug        string    `json:"slug" db:"slug"`
	Excerpt     string    `json:"excerpt" db:"excerpt"`
	Content     string    `json:"content" db:"content"`
	PublishedAt time.Time `json:"publishedAt" db:"published_at"`
	CreatedAt   time.Time `json:"createdAt" db:"created_at"`
	UpdatedAt   time.Time `json:"updatedAt" db:"updated_at"`
}

type CreateBlogPostRequest struct {
	Title   string `json:"title"`
	Excerpt string `json:"excerpt"`
	Content string `json:"content"`
}

type UpdateBlogPostRequest struct {
	Title   string `json:"title"`
	Excerpt string `json:"excerpt"`
	Content string `json:"content"`
}
