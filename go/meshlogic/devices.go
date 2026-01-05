// Copyright (c) 2024-2026 Mesh Logic Pty Ltd
// Licensed under the Apache License, Version 2.0

package meshlogic

import (
	"context"
	"encoding/json"
	"net/url"
	"strconv"
)

// DevicesService handles device-related API calls.
type DevicesService struct {
	client *Client
}

// DevicesListParams contains parameters for listing devices.
type DevicesListParams struct {
	Status   string // Filter by status (online, offline, degraded)
	Platform string // Filter by platform (linux, macos, windows)
	Limit    int    // Maximum devices to return
	Offset   int    // Pagination offset
}

// DevicesListResponse is the response from listing devices.
type DevicesListResponse struct {
	Devices    []Device `json:"devices"`
	TotalCount int      `json:"total_count"`
	HasMore    bool     `json:"has_more"`
}

// List retrieves devices with optional filtering.
func (s *DevicesService) List(ctx context.Context, params *DevicesListParams) (*DevicesListResponse, error) {
	if params == nil {
		params = &DevicesListParams{}
	}

	v := url.Values{}
	if params.Status != "" {
		v.Set("status", params.Status)
	}
	if params.Platform != "" {
		v.Set("platform", params.Platform)
	}
	if params.Limit > 0 {
		v.Set("limit", strconv.Itoa(params.Limit))
	} else {
		v.Set("limit", "100")
	}
	if params.Offset > 0 {
		v.Set("offset", strconv.Itoa(params.Offset))
	}

	body, err := s.client.request(ctx, "GET", "/v1/devices", v, nil)
	if err != nil {
		return nil, err
	}

	var resp DevicesListResponse
	if err := json.Unmarshal(body, &resp); err != nil {
		return nil, err
	}

	return &resp, nil
}

// Get retrieves a specific device by ID.
func (s *DevicesService) Get(ctx context.Context, deviceID string) (*Device, error) {
	body, err := s.client.request(ctx, "GET", "/v1/devices/"+deviceID, nil, nil)
	if err != nil {
		return nil, err
	}

	var device Device
	if err := json.Unmarshal(body, &device); err != nil {
		return nil, err
	}

	return &device, nil
}

// Status retrieves the overall device fleet status.
func (s *DevicesService) Status(ctx context.Context) (*DeviceStatus, error) {
	body, err := s.client.request(ctx, "GET", "/v1/devices/status", nil, nil)
	if err != nil {
		return nil, err
	}

	var status DeviceStatus
	if err := json.Unmarshal(body, &status); err != nil {
		return nil, err
	}

	return &status, nil
}
