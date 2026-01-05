"""
MeshLogic API Client.

Copyright (c) 2024-2026 Mesh Logic Pty Ltd
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

import os
from typing import Iterator, Optional
from dataclasses import dataclass

import httpx

from .exceptions import (
    MeshLogicError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
)
from .types import Event, Device, Pattern, PatternMatch
from .resources import EventsResource, DevicesResource, PatternsResource


# Default API endpoints by region
ENDPOINTS = {
    "ap-southeast-2": "https://api.meshlogic.ai",
    "us-east-1": "https://api.us.meshlogic.ai",
    "eu-west-1": "https://api.eu.meshlogic.ai",
}


@dataclass
class ClientConfig:
    """Configuration for MeshLogic client."""

    api_key: str
    region: str = "ap-southeast-2"
    base_url: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3


class MeshLogicClient:
    """
    MeshLogic API client.

    Example:
        >>> client = MeshLogicClient(api_key="your-api-key")
        >>> events = client.events.list(event_type="process", limit=100)
        >>> for event in events:
        ...     print(event.process_name)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        region: str = "ap-southeast-2",
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """
        Initialize the MeshLogic client.

        Args:
            api_key: API key for authentication. If not provided, reads from
                     MESHLOGIC_API_KEY environment variable.
            region: AWS region for the API endpoint. Default: ap-southeast-2
            base_url: Override the API base URL. Optional.
            timeout: Request timeout in seconds. Default: 30.0
            max_retries: Maximum number of retry attempts. Default: 3

        Raises:
            AuthenticationError: If no API key is provided or found.
        """
        self._api_key = api_key or os.environ.get("MESHLOGIC_API_KEY")
        if not self._api_key:
            raise AuthenticationError(
                "API key required. Provide via api_key parameter or "
                "MESHLOGIC_API_KEY environment variable."
            )

        self._region = region
        self._base_url = base_url or ENDPOINTS.get(region, ENDPOINTS["ap-southeast-2"])
        self._timeout = timeout
        self._max_retries = max_retries

        # Initialize HTTP client
        self._http = httpx.Client(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"meshlogic-python/0.1.0",
            },
            timeout=timeout,
        )

        # Initialize resource handlers
        self.events = EventsResource(self)
        self.devices = DevicesResource(self)
        self.patterns = PatternsResource(self)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        """
        Make an API request.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            params: Query parameters
            json: JSON body

        Returns:
            Response JSON as dictionary

        Raises:
            MeshLogicError: On API error
            RateLimitError: When rate limited
            NotFoundError: When resource not found
        """
        response = self._http.request(
            method=method,
            url=path,
            params=params,
            json=json,
        )

        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired API key")
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {path}")
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=retry_after,
            )
        elif response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise MeshLogicError(
                message=error_data.get("message", "Unknown error"),
                code=error_data.get("code", "UNKNOWN"),
                status_code=response.status_code,
            )

        return response.json() if response.content else {}

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()

    def __enter__(self) -> MeshLogicClient:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
