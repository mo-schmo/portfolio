package websocket

import (
	"log"
)

type Hub struct {
	clients    map[*Client]bool
	broadcast  chan Message
	register   chan *Client
	unregister chan *Client
}

func NewHub() *Hub {
	return &Hub{
		clients:    make(map[*Client]bool),
		broadcast:  make(chan Message),
		register:   make(chan *Client),
		unregister: make(chan *Client),
	}
}

func (h *Hub) Run() {
	for {
		select {
		case client := <-h.register:
			h.clients[client] = true
			log.Printf("Client connected. Total clients: %d", len(h.clients))
			h.broadcastCount()

		case client := <-h.unregister:
			if _, ok := h.clients[client]; ok {
				delete(h.clients, client)
				close(client.send)
				log.Printf("Client disconnected. Total clients: %d", len(h.clients))
				h.broadcastCount()
			}

		case message := <-h.broadcast:
			for client := range h.clients {
				select {
				case client.send <- message:
				default:
					close(client.send)
					delete(h.clients, client)
				}
			}
		}
	}
}

func (h *Hub) Register(client *Client) {
	h.register <- client
}

func (h *Hub) Broadcast(message Message) {
	h.broadcast <- message
}

func (h *Hub) broadcastCount() {
	count := len(h.clients)
	msg := Message{
		Type:    "census_update",
		Payload: map[string]int{"count": count},
	}
	// Send message asynchronously to avoid blocking the main loop
	go func() {
		h.broadcast <- msg
	}()
}
