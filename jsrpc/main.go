package main

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

type Session struct {
	peer   Peer
	active bool

	mu sync.Mutex
}

func (s *Session) Handle(msg []byte) ([]byte, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if !s.active {
		return nil, fmt.Errorf("session: %s is inactive", s.peer.Id())
	}

	err := s.peer.Send(msg)
	if err != nil {
		s.active = false
		return nil, err
	}

	res, err := s.peer.Recv()
	if err != nil {
		s.active = false
		return nil, err
	}
	return res, nil
}

func (s *Session) IsActive() bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.active
}

func (s *Session) Close() {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.peer.Close()
	s.active = false
}

type SessionManager struct {
	sessions map[string]*Session
	mu       sync.RWMutex
}

func NewSessionManager() *SessionManager {
	return &SessionManager{
		sessions: make(map[string]*Session),
	}
}

func (sm *SessionManager) AddSession(peer Peer) {
	sm.mu.Lock()
	defer sm.mu.Unlock()

	if s, ok := sm.sessions[peer.Id()]; ok {
		s.Close()
	}
	sm.sessions[peer.Id()] = &Session{
		peer:   peer,
		active: true,
	}
}

func (sm *SessionManager) removeInactiveSession(id string) {
	sm.mu.Lock()
	defer sm.mu.Unlock()

	s, ok := sm.sessions[id]
	if ok {
		if !s.IsActive() {
			s.Close()
			delete(sm.sessions, id)
		}
	}
}

func (sm *SessionManager) Handle(id string, msg []byte) ([]byte, error) {
	sm.mu.RLock()
	session, ok := sm.sessions[id]
	sm.mu.RUnlock()
	if !ok {
		return nil, fmt.Errorf("session: %s not found", id)
	}

	res, err := session.Handle(msg)
	if err != nil {
		sm.removeInactiveSession(id)
		return nil, err
	}
	return res, nil
}

type onPerr func(Peer)

type Peer interface {
	Id() string
	Addr() net.Addr
	Send(msg []byte) error
	Recv() ([]byte, error)
	Close() error
}

type wsPeer struct {
	conn *websocket.Conn
	id   string
}

func newWsPeer(conn *websocket.Conn, id string) Peer {
	return &wsPeer{
		conn: conn,
		id:   id,
	}
}

func (p *wsPeer) Id() string {
	return p.id
}

func (p *wsPeer) Addr() net.Addr {
	return p.conn.RemoteAddr()
}

func (p *wsPeer) Send(msg []byte) error {
	return p.conn.WriteMessage(websocket.TextMessage, msg)
}

func (p *wsPeer) Recv() ([]byte, error) {
	_, msg, err := p.conn.ReadMessage()
	if err != nil {
		return nil, err
	}
	return msg, nil
}

func (p *wsPeer) Close() error {
	return p.conn.Close()
}

func wsHandler(onPeer onPerr) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Println("Upgrade error:", err)
			return
		}

		peer := newWsPeer(conn, r.URL.Query().Get("id"))
		onPeer(peer)
	}
}

func echoHandler(sm *SessionManager) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		msg := r.URL.Query().Get("msg")
		res, err := sm.Handle("echo", []byte(msg))
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Write(res)
	}
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // 允许跨域（仅示例用，生产环境请严格限制）
	},
}

func main() {
	var sm = NewSessionManager()

	http.HandleFunc("/echo", echoHandler(sm))
	http.HandleFunc("/ws", wsHandler(sm.AddSession))
	log.Println("Server started at :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
