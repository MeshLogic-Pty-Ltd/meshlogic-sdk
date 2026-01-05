// Copyright (c) 2024-2026 Mesh Logic Pty Ltd
// Licensed under the Apache License, Version 2.0

package meshlogic

import (
	"context"
	"encoding/json"
	"net/url"
	"strconv"
)

// EventsService handles event-related API calls.
type EventsService struct {
	client *Client
}

// EventsListParams contains parameters for listing events.
type EventsListParams struct {
	EventType string // Filter by event type (process, file, network)
	DeviceID  string // Filter by device ID
	Since     string // Start time (ISO format or relative like "1h", "24h")
	Until     string // End time
	Limit     int    // Maximum events to return (default: 100, max: 1000)
	Offset    int    // Pagination offset
}

// EventsListResponse is the response from listing events.
type EventsListResponse struct {
	Events     []Event `json:"events"`
	TotalCount int     `json:"total_count"`
	HasMore    bool    `json:"has_more"`
}

// List retrieves events with optional filtering.
func (s *EventsService) List(ctx context.Context, params *EventsListParams) (*EventsListResponse, error) {
	if params == nil {
		params = &EventsListParams{}
	}

	v := url.Values{}
	if params.EventType != "" {
		v.Set("type", params.EventType)
	}
	if params.DeviceID != "" {
		v.Set("device_id", params.DeviceID)
	}
	if params.Since != "" {
		v.Set("since", params.Since)
	}
	if params.Until != "" {
		v.Set("until", params.Until)
	}
	if params.Limit > 0 {
		v.Set("limit", strconv.Itoa(params.Limit))
	} else {
		v.Set("limit", "100")
	}
	if params.Offset > 0 {
		v.Set("offset", strconv.Itoa(params.Offset))
	}

	body, err := s.client.request(ctx, "GET", "/v1/events", v, nil)
	if err != nil {
		return nil, err
	}

	var resp EventsListResponse
	if err := json.Unmarshal(body, &resp); err != nil {
		return nil, err
	}

	return &resp, nil
}

// Get retrieves a specific event by ID.
func (s *EventsService) Get(ctx context.Context, eventID string) (*Event, error) {
	body, err := s.client.request(ctx, "GET", "/v1/events/"+eventID, nil, nil)
	if err != nil {
		return nil, err
	}

	var event Event
	if err := json.Unmarshal(body, &event); err != nil {
		return nil, err
	}

	return &event, nil
}

// ExportParams contains parameters for exporting events.
type ExportParams struct {
	Format    string // Export format (json, csv, parquet)
	EventType string // Filter by event type
	Since     string // Start time
	Until     string // End time
}

// Export exports events to the specified format.
func (s *EventsService) Export(ctx context.Context, params *ExportParams) ([]byte, error) {
	if params == nil {
		params = &ExportParams{Format: "json"}
	}

	v := url.Values{}
	v.Set("format", params.Format)
	if params.EventType != "" {
		v.Set("type", params.EventType)
	}
	if params.Since != "" {
		v.Set("since", params.Since)
	}
	if params.Until != "" {
		v.Set("until", params.Until)
	}

	return s.client.request(ctx, "GET", "/v1/events/export", v, nil)
}
