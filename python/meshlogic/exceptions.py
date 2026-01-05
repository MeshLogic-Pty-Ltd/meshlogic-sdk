"""
MeshLogic SDK exceptions.

Copyright (c) 2024-2026 Mesh Logic Pty Ltd
Licensed under the Apache License, Version 2.0
"""

from typing import Optional


class MeshLogicError(Exception):
    """Base exception for MeshLogic SDK errors."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class AuthenticationError(MeshLogicError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="AUTH_ERROR", status_code=401)


class RateLimitError(MeshLogicError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60):
        super().__init__(message, code="RATE_LIMIT", status_code=429)
        self.retry_after = retry_after

    def __str__(self) -> str:
        return f"{self.message}. Retry after {self.retry_after} seconds."


class NotFoundError(MeshLogicError):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="NOT_FOUND", status_code=404)


class ValidationError(MeshLogicError):
    """Raised when request validation fails."""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, code="VALIDATION_ERROR", status_code=400)
        self.field = field

    def __str__(self) -> str:
        if self.field:
            return f"Validation error on field '{self.field}': {self.message}"
        return f"Validation error: {self.message}"
