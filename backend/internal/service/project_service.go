package service

import (
	"encoding/json"
	"portfolio-backend/internal/domain"
	"portfolio-backend/internal/repository"
)

type ProjectService struct {
	repo *repository.ProjectRepository
}

func NewProjectService(repo *repository.ProjectRepository) *ProjectService {
	return &ProjectService{repo: repo}
}

func (s *ProjectService) GetAll() ([]domain.Project, error) {
	return s.repo.GetAll()
}

func (s *ProjectService) GetByID(id int) (*domain.Project, error) {
	return s.repo.GetByID(id)
}

func (s *ProjectService) GetBySlug(slug string) (*domain.Project, error) {
	return s.repo.GetBySlug(slug)
}

func (s *ProjectService) Create(req domain.CreateProjectRequest) (*domain.Project, error) {
	technologiesJSON, err := json.Marshal(req.Technologies)
	if err != nil {
		return nil, err
	}

	project := &domain.Project{
		Title:        req.Title,
		Slug:         req.Slug,
		Description:  req.Description,
		Content:      req.Content,
		ImageURL:     req.ImageURL,
		GithubURL:    req.GithubURL,
		LiveURL:      req.LiveURL,
		Technologies: string(technologiesJSON),
		Featured:     req.Featured,
	}

	err = s.repo.Create(project)
	if err != nil {
		return nil, err
	}

	return project, nil
}

func (s *ProjectService) Update(id int, req domain.UpdateProjectRequest) (*domain.Project, error) {
	project, err := s.repo.GetByID(id)
	if err != nil {
		return nil, err
	}
	if project == nil {
		return nil, nil
	}

	technologiesJSON, err := json.Marshal(req.Technologies)
	if err != nil {
		return nil, err
	}

	project.Title = req.Title
	project.Slug = req.Slug
	project.Description = req.Description
	project.Content = req.Content
	project.ImageURL = req.ImageURL
	project.GithubURL = req.GithubURL
	project.LiveURL = req.LiveURL
	project.Technologies = string(technologiesJSON)
	project.Featured = req.Featured

	err = s.repo.Update(project)
	if err != nil {
		return nil, err
	}

	return project, nil
}

func (s *ProjectService) Delete(id int) error {
	return s.repo.Delete(id)
}
