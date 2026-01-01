package repository

import (
	"database/sql"
	"encoding/json"
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
		SELECT id, title, description, image_url, github_url, live_url, technologies, featured, created_at, updated_at
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
			&project.ID, &project.Title, &project.Description,
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
		SELECT id, title, description, image_url, github_url, live_url, technologies, featured, created_at, updated_at
		FROM projects
		WHERE id = ?
	`, id).Scan(
		&project.ID, &project.Title, &project.Description,
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

	technologiesJSON, err := json.Marshal(project.Technologies)
	if err != nil {
		return err
	}

	result, err := r.db.Exec(`
		INSERT INTO projects (title, description, image_url, github_url, live_url, technologies, featured, created_at, updated_at)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
	`, project.Title, project.Description, project.ImageURL, project.GithubURL,
		project.LiveURL, string(technologiesJSON), project.Featured, project.CreatedAt, project.UpdatedAt)
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

	technologiesJSON, err := json.Marshal(project.Technologies)
	if err != nil {
		return err
	}

	_, err = r.db.Exec(`
		UPDATE projects
		SET title = ?, description = ?, image_url = ?, github_url = ?, live_url = ?, technologies = ?, featured = ?, updated_at = ?
		WHERE id = ?
	`, project.Title, project.Description, project.ImageURL, project.GithubURL,
		project.LiveURL, string(technologiesJSON), project.Featured, project.UpdatedAt, project.ID)
	return err
}

func (r *ProjectRepository) Delete(id int) error {
	_, err := r.db.Exec(`DELETE FROM projects WHERE id = ?`, id)
	return err
}
