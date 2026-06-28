package api

import (
	"net/http"
	"os"
	"path/filepath"
)

// ResumeHandler serves the canonical resume JSON used by both the
// frontend and the Python agents service for grounding.
type ResumeHandler struct {
	path string
}

func NewResumeHandler() *ResumeHandler {
	path := os.Getenv("RESUME_PATH")
	if path == "" {
		path = filepath.Join("data", "resume.json")
	}
	return &ResumeHandler{path: path}
}

func (h *ResumeHandler) Get(w http.ResponseWriter, r *http.Request) {
	data, err := os.ReadFile(h.path)
	if err != nil {
		http.Error(w, "Resume not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Cache-Control", "public, max-age=300")
	if _, err := w.Write(data); err != nil {
		return
	}
}
