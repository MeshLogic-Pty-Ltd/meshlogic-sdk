// Copyright (c) 2024-2026 Mesh Logic Pty Ltd
// Licensed under the Apache License, Version 2.0

package meshlogic

import "fmt"

// Error represents an API error.
type Error struct {
	Code       string `json:"code"`
	Message    string `json:"message"`
	StatusCode int    `json:"-"`
}

func (e *Error) Error() string {
	if e.Code != "" {
		return fmt.Sprintf("[%s] %s", e.Code, e.Message)
	}
	return e.Message
}

// AuthenticationError is returned when authentication fails.
type AuthenticationError struct {
	Error
}

// NotFoundError is returned when a resource is not found.
type NotFoundError struct {
	Error
}

// RateLimitError is returned when rate limit is exceeded.
type RateLimitError struct {
	Error
	RetryAfter int // seconds until retry is allowed
}

func (e *RateLimitError) Error() string {
	return fmt.Sprintf("%s. Retry after %d seconds.", e.Message, e.RetryAfter)
}

// ValidationError is returned when request validation fails.
type ValidationError struct {
	Error
	Field string `json:"field,omitempty"`
}

func (e *ValidationError) Error() string {
	if e.Field != "" {
		return fmt.Sprintf("Validation error on field '%s': %s", e.Field, e.Message)
	}
	return fmt.Sprintf("Validation error: %s", e.Message)
}
