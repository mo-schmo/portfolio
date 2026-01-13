package api

import (
	"encoding/json"
	"net/http"
	"portfolio-backend/internal/auth"
	"time"
)

type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func Login(w http.ResponseWriter, r *http.Request) {
	var req LoginRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if !auth.CheckCredentials(req.Username, req.Password) {
		http.Error(w, "Invalid username or password", http.StatusUnauthorized)
		return
	}

	token, err := auth.GenerateToken(req.Username)
	if err != nil {
		http.Error(w, "Failed to generate authentication token", http.StatusInternalServerError)
		return
	}

	// Set secure httpOnly cookie
	http.SetCookie(w, &http.Cookie{
		Name:     "auth_token",
		Value:    token,
		Path:     "/",
		HttpOnly: true,
		Secure:   true,                  // Required for SameSite: None
		SameSite: http.SameSiteNoneMode, // Required for cross-site cookies (Vercel -> Northflank)
		Expires:  time.Now().Add(time.Hour * 24),
	})

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"message": "Authentication successful",
	})
}

func Logout(w http.ResponseWriter, r *http.Request) {
	http.SetCookie(w, &http.Cookie{
		Name:     "auth_token",
		Value:    "",
		Path:     "/",
		HttpOnly: true,
		Secure:   true,
		SameSite: http.SameSiteNoneMode,
		MaxAge:   -1,
		Expires:  time.Unix(0, 0),
	})

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"message": "Logged out successfully",
	})
}

func CheckAuth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"authenticated": true,
	})
}
