// Package meshlogic provides the official Go SDK for the MeshLogic API.
//
// Copyright (c) 2024-2026 Mesh Logic Pty Ltd
// Licensed under the Apache License, Version 2.0
package meshlogic

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"time"
)

// Default API endpoints by region
var endpoints = map[string]string{
	"ap-southeast-2": "https://api.meshlogic.ai",
	"us-east-1":      "https://api.us.meshlogic.ai",
	"eu-west-1":      "https://api.eu.meshlogic.ai",
}

// Client is the MeshLogic API client.
type Client struct {
	apiKey     string
	baseURL    string
	httpClient *http.Client

	// Resource handlers
	Events   *EventsService
	Devices  *DevicesService
	Patterns *PatternsService
}

// ClientOption configures the Client.
type ClientOption func(*Client)

// WithAPIKey sets the API key.
func WithAPIKey(apiKey string) ClientOption {
	return func(c *Client) {
		c.apiKey = apiKey
	}
}

// WithRegion sets the API region.
func WithRegion(region string) ClientOption {
	return func(c *Client) {
		if endpoint, ok := endpoints[region]; ok {
			c.baseURL = endpoint
		}
	}
}

// WithBaseURL overrides the API base URL.
func WithBaseURL(baseURL string) ClientOption {
	return func(c *Client) {
		c.baseURL = baseURL
	}
}

// WithHTTPClient sets a custom HTTP client.
func WithHTTPClient(httpClient *http.Client) ClientOption {
	return func(c *Client) {
		c.httpClient = httpClient
	}
}

// WithTimeout sets the HTTP client timeout.
func WithTimeout(timeout time.Duration) ClientOption {
	return func(c *Client) {
		c.httpClient.Timeout = timeout
	}
}

// NewClient creates a new MeshLogic API client.
//
// Example:
//
//	client := meshlogic.NewClient(
//	    meshlogic.WithAPIKey("your-api-key"),
//	    meshlogic.WithRegion("ap-southeast-2"),
//	)
func NewClient(opts ...ClientOption) (*Client, error) {
	c := &Client{
		baseURL: endpoints["ap-southeast-2"],
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}

	for _, opt := range opts {
		opt(c)
	}

	// Check for API key in environment if not provided
	if c.apiKey == "" {
		c.apiKey = os.Getenv("MESHLOGIC_API_KEY")
	}

	if c.apiKey == "" {
		return nil, &Error{
			Code:    "AUTH_ERROR",
			Message: "API key required. Provide via WithAPIKey() or MESHLOGIC_API_KEY environment variable.",
		}
	}

	// Initialize services
	c.Events = &EventsService{client: c}
	c.Devices = &DevicesService{client: c}
	c.Patterns = &PatternsService{client: c}

	return c, nil
}

// request makes an API request.
func (c *Client) request(ctx context.Context, method, path string, params url.Values, body interface{}) ([]byte, error) {
	// Build URL
	u, err := url.Parse(c.baseURL + path)
	if err != nil {
		return nil, err
	}
	if params != nil {
		u.RawQuery = params.Encode()
	}

	// Build request body
	var bodyReader io.Reader
	if body != nil {
		jsonBody, err := json.Marshal(body)
		if err != nil {
			return nil, err
		}
		bodyReader = bytes.NewReader(jsonBody)
	}

	// Create request
	req, err := http.NewRequestWithContext(ctx, method, u.String(), bodyReader)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Authorization", "Bearer "+c.apiKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "meshlogic-go/0.1.0")

	// Execute request
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Read response body
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	// Handle errors
	if resp.StatusCode >= 400 {
		var apiErr Error
		if err := json.Unmarshal(respBody, &apiErr); err != nil {
			apiErr = Error{
				Code:       "UNKNOWN",
				Message:    string(respBody),
				StatusCode: resp.StatusCode,
			}
		}
		apiErr.StatusCode = resp.StatusCode

		switch resp.StatusCode {
		case 401:
			return nil, &AuthenticationError{Error: apiErr}
		case 404:
			return nil, &NotFoundError{Error: apiErr}
		case 429:
			retryAfter := 60
			if ra := resp.Header.Get("Retry-After"); ra != "" {
				fmt.Sscanf(ra, "%d", &retryAfter)
			}
			return nil, &RateLimitError{Error: apiErr, RetryAfter: retryAfter}
		default:
			return nil, &apiErr
		}
	}

	return respBody, nil
}
