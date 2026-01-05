// Copyright (c) 2024-2026 Mesh Logic Pty Ltd
// Licensed under the Apache License, Version 2.0

package meshlogic

import "time"

// EventType represents the type of event.
type EventType string

const (
	EventTypeProcess EventType = "process"
	EventTypeFile    EventType = "file"
	EventTypeNetwork EventType = "network"
)

// EventAction represents the action that triggered the event.
type EventAction string

const (
	// Process actions
	ActionExec EventAction = "exec"
	ActionExit EventAction = "exit"
	ActionFork EventAction = "fork"

	// File actions
	ActionOpen   EventAction = "open"
	ActionWrite  EventAction = "write"
	ActionDelete EventAction = "delete"
	ActionRename EventAction = "rename"

	// Network actions
	ActionConnect EventAction = "connect"
	ActionAccept  EventAction = "accept"
	ActionSend    EventAction = "send"
	ActionReceive EventAction = "receive"
)

// Event represents a behavioral event.
type Event struct {
	ID         string          `json:"id"`
	Type       EventType       `json:"type"`
	Action     EventAction     `json:"action"`
	Timestamp  time.Time       `json:"timestamp"`
	DeviceID   string          `json:"device_id"`
	CustomerID string          `json:"customer_id"`
	Raw        json.RawMessage `json:"raw,omitempty"`

	// Process fields
	PID            int    `json:"pid,omitempty"`
	PPID           int    `json:"ppid,omitempty"`
	ProcessName    string `json:"process_name,omitempty"`
	ExecutablePath string `json:"executable_path,omitempty"`
	CommandLine    string `json:"command_line,omitempty"`
	User           string `json:"user,omitempty"`
	ExitCode       *int   `json:"exit_code,omitempty"`

	// File fields
	Path       string `json:"path,omitempty"`
	TargetPath string `json:"target_path,omitempty"`

	// Network fields
	LocalAddress  string `json:"local_address,omitempty"`
	LocalPort     int    `json:"local_port,omitempty"`
	RemoteAddress string `json:"remote_address,omitempty"`
	RemotePort    int    `json:"remote_port,omitempty"`
	Protocol      string `json:"protocol,omitempty"`
}

// Device represents a monitored device.
type Device struct {
	ID           string    `json:"id"`
	Hostname     string    `json:"hostname"`
	Platform     string    `json:"platform"`
	OSVersion    string    `json:"os_version"`
	AgentVersion string    `json:"agent_version"`
	LastSeen     time.Time `json:"last_seen"`
	Status       string    `json:"status"`
	CustomerID   string    `json:"customer_id"`
}

// Pattern represents a detection pattern.
type Pattern struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Category    string `json:"category"`
	Description string `json:"description"`
	Severity    string `json:"severity"`
	Enabled     bool   `json:"enabled"`
}

// PatternMatch represents a pattern match result.
type PatternMatch struct {
	ID          string                 `json:"id"`
	PatternID   string                 `json:"pattern_id"`
	PatternName string                 `json:"pattern_name"`
	EventID     string                 `json:"event_id"`
	DeviceID    string                 `json:"device_id"`
	Timestamp   time.Time              `json:"timestamp"`
	Severity    string                 `json:"severity"`
	Details     map[string]interface{} `json:"details,omitempty"`
}

// DeviceStatus represents fleet status summary.
type DeviceStatus struct {
	Total    int `json:"total"`
	Online   int `json:"online"`
	Offline  int `json:"offline"`
	Degraded int `json:"degraded"`
}
