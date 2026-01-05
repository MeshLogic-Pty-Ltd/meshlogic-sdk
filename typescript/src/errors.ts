/**
 * MeshLogic SDK errors.
 *
 * Copyright (c) 2024-2026 Mesh Logic Pty Ltd
 * Licensed under the Apache License, Version 2.0
 */

/** Base error class for MeshLogic SDK errors */
export class MeshLogicError extends Error {
  constructor(
    message: string,
    public code?: string,
    public statusCode?: number
  ) {
    super(message);
    this.name = 'MeshLogicError';
  }

  toString(): string {
    if (this.code) {
      return `[${this.code}] ${this.message}`;
    }
    return this.message;
  }
}

/** Raised when authentication fails */
export class AuthenticationError extends MeshLogicError {
  constructor(message = 'Authentication failed') {
    super(message, 'AUTH_ERROR', 401);
    this.name = 'AuthenticationError';
  }
}

/** Raised when rate limit is exceeded */
export class RateLimitError extends MeshLogicError {
  constructor(
    message = 'Rate limit exceeded',
    public retryAfter = 60
  ) {
    super(message, 'RATE_LIMIT', 429);
    this.name = 'RateLimitError';
  }

  toString(): string {
    return `${this.message}. Retry after ${this.retryAfter} seconds.`;
  }
}

/** Raised when a resource is not found */
export class NotFoundError extends MeshLogicError {
  constructor(message = 'Resource not found') {
    super(message, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}

/** Raised when request validation fails */
export class ValidationError extends MeshLogicError {
  constructor(
    message: string,
    public field?: string
  ) {
    super(message, 'VALIDATION_ERROR', 400);
    this.name = 'ValidationError';
  }

  toString(): string {
    if (this.field) {
      return `Validation error on field '${this.field}': ${this.message}`;
    }
    return `Validation error: ${this.message}`;
  }
}
