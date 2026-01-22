package service

import (
	"encoding/json"
	"portfolio-backend/internal/domain"
	"portfolio-backend/internal/repository"
	"portfolio-backend/pkg/websocket"
)

type ProjectService struct {
	repo *repository.ProjectRepository
	hub  *websocket.Hub
}

func NewProjectService(repo *repository.ProjectRepository, hub *websocket.Hub) *ProjectService {
	return &ProjectService{repo: repo, hub: hub}
}

func (s *ProjectService) GetAll() ([]domain.Project, error) {
	return s.repo.GetAll()
}

func (s *ProjectService) GetAllAdmin() ([]domain.Project, error) {
	return s.repo.GetAllAdmin()
}

func (s *ProjectService) GetByID(id int) (*domain.Project, error) {
	return s.repo.GetByID(id)
}

func (s *ProjectService) GetByIDAdmin(id int) (*domain.Project, error) {
	return s.repo.GetByIDAdmin(id)
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
		IsDraft:      req.IsDraft,
	}

	err = s.repo.Create(project)
	if err != nil {
		return nil, err
	}

	// Broadcast creation event
	s.hub.Broadcast(websocket.Message{
		Type:    "project_created",
		Payload: project,
	})

	return project, nil
}

func (s *ProjectService) Update(id int, req domain.UpdateProjectRequest) (*domain.Project, error) {
	// For update, we use GetByIDAdmin to handle drafts
	project, err := s.repo.GetByIDAdmin(id)
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
	project.IsDraft = req.IsDraft

	err = s.repo.Update(project)
	if err != nil {
		return nil, err
	}

	// Broadcast update event
	s.hub.Broadcast(websocket.Message{
		Type:    "project_updated",
		Payload: project,
	})

	return project, nil
}

func (s *ProjectService) Delete(id int) error {
	err := s.repo.Delete(id)

	if err == nil {
		// Broadcast deletion
		s.hub.Broadcast(websocket.Message{
			Type: "project_deleted",
			Payload: map[string]int{
				"id": id,
			},
		})
	}

	return err
}
