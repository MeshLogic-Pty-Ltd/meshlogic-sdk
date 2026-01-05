// Copyright (c) 2024-2026 Mesh Logic Pty Ltd
// Licensed under the Apache License, Version 2.0

package meshlogic

import (
	"context"
	"encoding/json"
	"net/url"
	"strconv"
)

// PatternsService handles pattern-related API calls.
type PatternsService struct {
	client *Client
}

// PatternsListParams contains parameters for listing patterns.
type PatternsListParams struct {
	Category string // Filter by category
	Enabled  *bool  // Filter by enabled status
}

// PatternsListResponse is the response from listing patterns.
type PatternsListResponse struct {
	Patterns   []Pattern `json:"patterns"`
	TotalCount int       `json:"total_count"`
}

// List retrieves detection patterns.
func (s *PatternsService) List(ctx context.Context, params *PatternsListParams) (*PatternsListResponse, error) {
	if params == nil {
		params = &PatternsListParams{}
	}

	v := url.Values{}
	if params.Category != "" {
		v.Set("category", params.Category)
	}
	if params.Enabled != nil {
		v.Set("enabled", strconv.FormatBool(*params.Enabled))
	}

	body, err := s.client.request(ctx, "GET", "/v1/patterns", v, nil)
	if err != nil {
		return nil, err
	}

	var resp PatternsListResponse
	if err := json.Unmarshal(body, &resp); err != nil {
		return nil, err
	}

	return &resp, nil
}

// MatchesParams contains parameters for listing pattern matches.
type MatchesParams struct {
	PatternID string // Filter by pattern ID
	DeviceID  string // Filter by device ID
	Since     string // Start time
	Limit     int    // Maximum matches to return
}

// MatchesResponse is the response from listing pattern matches.
type MatchesResponse struct {
	Matches    []PatternMatch `json:"matches"`
	TotalCount int            `json:"total_count"`
	HasMore    bool           `json:"has_more"`
}

// Matches retrieves pattern match history.
func (s *PatternsService) Matches(ctx context.Context, params *MatchesParams) (*MatchesResponse, error) {
	if params == nil {
		params = &MatchesParams{}
	}

	v := url.Values{}
	if params.PatternID != "" {
		v.Set("pattern_id", params.PatternID)
	}
	if params.DeviceID != "" {
		v.Set("device_id", params.DeviceID)
	}
	if params.Since != "" {
		v.Set("since", params.Since)
	}
	if params.Limit > 0 {
		v.Set("limit", strconv.Itoa(params.Limit))
	} else {
		v.Set("limit", "100")
	}

	body, err := s.client.request(ctx, "GET", "/v1/patterns/matches", v, nil)
	if err != nil {
		return nil, err
	}

	var resp MatchesResponse
	if err := json.Unmarshal(body, &resp); err != nil {
		return nil, err
	}

	return &resp, nil
}
