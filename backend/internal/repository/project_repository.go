package repository

import (
	"database/sql"
	"portfolio-backend/internal/domain"
	"time"
)

type ProjectRepository struct {
	db *sql.DB
}

func NewProjectRepository(db *sql.DB) *ProjectRepository {
	return &ProjectRepository{db: db}
}

func (r *ProjectRepository) GetAll() ([]domain.Project, error) {
	rows, err := r.db.Query(`
		SELECT id, title, slug, description, content, image_url, github_url, live_url, technologies, featured, created_at, updated_at
		FROM projects
		ORDER BY created_at DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var projects []domain.Project
	for rows.Next() {
		var project domain.Project
		var technologiesStr string
		err := rows.Scan(
			&project.ID, &project.Title, &project.Slug, &project.Description, &project.Content,
			&project.ImageURL, &project.GithubURL, &project.LiveURL,
			&technologiesStr, &project.Featured, &project.CreatedAt, &project.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}
		project.Technologies = technologiesStr
		projects = append(projects, project)
	}

	return projects, rows.Err()
}

func (r *ProjectRepository) GetByID(id int) (*domain.Project, error) {
	var project domain.Project
	var technologiesStr string
	err := r.db.QueryRow(`
		SELECT id, title, slug, description, content, image_url, github_url, live_url, technologies, featured, created_at, updated_at
		FROM projects
		WHERE id = ?
	`, id).Scan(
		&project.ID, &project.Title, &project.Slug, &project.Description, &project.Content,
		&project.ImageURL, &project.GithubURL, &project.LiveURL,
		&technologiesStr, &project.Featured, &project.CreatedAt, &project.UpdatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	project.Technologies = technologiesStr
	return &project, nil
}

func (r *ProjectRepository) GetBySlug(slug string) (*domain.Project, error) {
	var project domain.Project
	var technologiesStr string
	err := r.db.QueryRow(`
		SELECT id, title, slug, description, content, image_url, github_url, live_url, technologies, featured, created_at, updated_at
		FROM projects
		WHERE slug = ?
	`, slug).Scan(
		&project.ID, &project.Title, &project.Slug, &project.Description, &project.Content,
		&project.ImageURL, &project.GithubURL, &project.LiveURL,
		&technologiesStr, &project.Featured, &project.CreatedAt, &project.UpdatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	project.Technologies = technologiesStr
	return &project, nil
}

func (r *ProjectRepository) Create(project *domain.Project) error {
	now := time.Now()
	project.CreatedAt = now
	project.UpdatedAt = now

	result, err := r.db.Exec(`
		INSERT INTO projects (title, slug, description, content, image_url, github_url, live_url, technologies, featured, created_at, updated_at)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`, project.Title, project.Slug, project.Description, project.Content, project.ImageURL, project.GithubURL,
		project.LiveURL, project.Technologies, project.Featured, project.CreatedAt, project.UpdatedAt)
	if err != nil {
		return err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return err
	}
	project.ID = int(id)
	return nil
}

func (r *ProjectRepository) Update(project *domain.Project) error {
	project.UpdatedAt = time.Now()

	_, err := r.db.Exec(`
		UPDATE projects
		SET title = ?, slug = ?, description = ?, content = ?, image_url = ?, github_url = ?, live_url = ?, technologies = ?, featured = ?, updated_at = ?
		WHERE id = ?
	`, project.Title, project.Slug, project.Description, project.Content, project.ImageURL, project.GithubURL,
		project.LiveURL, project.Technologies, project.Featured, project.UpdatedAt, project.ID)
	return err
}

func (r *ProjectRepository) Delete(id int) error {
	_, err := r.db.Exec(`DELETE FROM projects WHERE id = ?`, id)
	return err
}
