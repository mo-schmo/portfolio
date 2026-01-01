package repository

import (
	"database/sql"
	"portfolio-backend/internal/domain"
	"time"
)

type BlogRepository struct {
	db *sql.DB
}

func NewBlogRepository(db *sql.DB) *BlogRepository {
	return &BlogRepository{db: db}
}

func (r *BlogRepository) GetAll() ([]domain.BlogPost, error) {
	rows, err := r.db.Query(`
		SELECT id, title, slug, excerpt, content, published_at, created_at, updated_at
		FROM blog_posts
		ORDER BY published_at DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var posts []domain.BlogPost
	for rows.Next() {
		var post domain.BlogPost
		err := rows.Scan(
			&post.ID, &post.Title, &post.Slug, &post.Excerpt,
			&post.Content, &post.PublishedAt, &post.CreatedAt, &post.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}
		posts = append(posts, post)
	}

	return posts, rows.Err()
}

func (r *BlogRepository) GetByID(id int) (*domain.BlogPost, error) {
	var post domain.BlogPost
	err := r.db.QueryRow(`
		SELECT id, title, slug, excerpt, content, published_at, created_at, updated_at
		FROM blog_posts
		WHERE id = ?
	`, id).Scan(
		&post.ID, &post.Title, &post.Slug, &post.Excerpt,
		&post.Content, &post.PublishedAt, &post.CreatedAt, &post.UpdatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &post, nil
}

func (r *BlogRepository) GetBySlug(slug string) (*domain.BlogPost, error) {
	var post domain.BlogPost
	err := r.db.QueryRow(`
		SELECT id, title, slug, excerpt, content, published_at, created_at, updated_at
		FROM blog_posts
		WHERE slug = ?
	`, slug).Scan(
		&post.ID, &post.Title, &post.Slug, &post.Excerpt,
		&post.Content, &post.PublishedAt, &post.CreatedAt, &post.UpdatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &post, nil
}

func (r *BlogRepository) Create(post *domain.BlogPost) error {
	now := time.Now()
	post.CreatedAt = now
	post.UpdatedAt = now
	if post.PublishedAt.IsZero() {
		post.PublishedAt = now
	}

	result, err := r.db.Exec(`
		INSERT INTO blog_posts (title, slug, excerpt, content, published_at, created_at, updated_at)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	`, post.Title, post.Slug, post.Excerpt, post.Content, post.PublishedAt, post.CreatedAt, post.UpdatedAt)
	if err != nil {
		return err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return err
	}
	post.ID = int(id)
	return nil
}

func (r *BlogRepository) Update(post *domain.BlogPost) error {
	post.UpdatedAt = time.Now()
	_, err := r.db.Exec(`
		UPDATE blog_posts
		SET title = ?, slug = ?, excerpt = ?, content = ?, published_at = ?, updated_at = ?
		WHERE id = ?
	`, post.Title, post.Slug, post.Excerpt, post.Content, post.PublishedAt, post.UpdatedAt, post.ID)
	return err
}

func (r *BlogRepository) Delete(id int) error {
	_, err := r.db.Exec(`DELETE FROM blog_posts WHERE id = ?`, id)
	return err
}
