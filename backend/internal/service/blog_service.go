package service

import (
	"fmt"
	"portfolio-backend/internal/domain"
	"portfolio-backend/internal/repository"
	"portfolio-backend/pkg/websocket"
	"strings"
	"time"
)

type BlogService struct {
	repo *repository.BlogRepository
	hub  *websocket.Hub
}

func NewBlogService(repo *repository.BlogRepository, hub *websocket.Hub) *BlogService {
	return &BlogService{repo: repo, hub: hub}
}

func (s *BlogService) GetAll() ([]domain.BlogPost, error) {
	return s.repo.GetAll()
}

func (s *BlogService) GetByID(id int) (*domain.BlogPost, error) {
	return s.repo.GetByID(id)
}

func (s *BlogService) GetBySlug(slug string) (*domain.BlogPost, error) {
	return s.repo.GetBySlug(slug)
}

func (s *BlogService) Create(req domain.CreateBlogPostRequest) (*domain.BlogPost, error) {
	slug := generateSlug(req.Title)

	// Ensure slug is unique
	existing, _ := s.repo.GetBySlug(slug)
	counter := 1
	originalSlug := slug
	for existing != nil {
		slug = fmt.Sprintf("%s-%d", originalSlug, counter)
		existing, _ = s.repo.GetBySlug(slug)
		counter++
		if counter > 1000 { // Safety limit
			break
		}
	}

	post := &domain.BlogPost{
		Title:       req.Title,
		Slug:        slug,
		Excerpt:     req.Excerpt,
		Content:     req.Content,
		PublishedAt: time.Now(),
	}

	err := s.repo.Create(post)
	if err != nil {
		return nil, err
	}

	// Broadcast creation
	s.hub.Broadcast(websocket.Message{
		Type:    "blog_created",
		Payload: post,
	})

	return post, nil
}

func (s *BlogService) Update(id int, req domain.UpdateBlogPostRequest) (*domain.BlogPost, error) {
	post, err := s.repo.GetByID(id)
	if err != nil {
		return nil, err
	}
	if post == nil {
		return nil, nil
	}

	post.Title = req.Title
	post.Excerpt = req.Excerpt
	post.Content = req.Content
	post.Slug = generateSlug(req.Title)

	err = s.repo.Update(post)
	if err != nil {
		return nil, err
	}

	// Broadcast update
	s.hub.Broadcast(websocket.Message{
		Type:    "blog_updated",
		Payload: post,
	})

	return post, nil
}

func (s *BlogService) Delete(id int) error {
	err := s.repo.Delete(id)
	if err == nil {
		// Broadcast deletion
		s.hub.Broadcast(websocket.Message{
			Type: "blog_deleted",
			Payload: map[string]int{
				"id": id,
			},
		})
	}
	return err
}

func generateSlug(title string) string {
	slug := strings.ToLower(title)
	slug = strings.ReplaceAll(slug, " ", "-")
	slug = strings.ReplaceAll(slug, "'", "")
	slug = strings.ReplaceAll(slug, "\"", "")
	// Add more replacements as needed
	return slug
}
