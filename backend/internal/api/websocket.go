package api

import (
	"log"
	"net/http"
	ws "portfolio-backend/pkg/websocket"

	"github.com/gorilla/websocket"
)

type WebSocketHub struct {
	hub *ws.Hub
}

func NewWebSocketHub() *WebSocketHub {
	return &WebSocketHub{
		hub: ws.NewHub(),
	}
}

func (h *WebSocketHub) HandleWebSocket(w http.ResponseWriter, r *http.Request) {
	var upgrader = websocket.Upgrader{
		CheckOrigin: func(r *http.Request) bool {
			return true // Allow all origins in development
		},
	}

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("WebSocket upgrade error: %v", err)
		return
	}

	client := ws.NewClient(h.hub, conn)
	h.hub.Register(client)

	go client.WritePump()
	go client.ReadPump()
}

func (h *WebSocketHub) Broadcast(message ws.Message) {
	h.hub.Broadcast(message)
}

func (h *WebSocketHub) Run() {
	h.hub.Run()
}

func (h *WebSocketHub) GetHub() *ws.Hub {
	return h.hub
}
