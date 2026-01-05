"""
MeshLogic SDK API resources.

Copyright (c) 2024-2026 Mesh Logic Pty Ltd
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from typing import Iterator, List, Optional, TYPE_CHECKING

from .types import Event, Device, Pattern, PatternMatch

if TYPE_CHECKING:
    from .client import MeshLogicClient


class EventsResource:
    """Events API resource."""

    def __init__(self, client: MeshLogicClient):
        self._client = client

    def list(
        self,
        event_type: Optional[str] = None,
        device_id: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Event]:
        """
        List events with optional filtering.

        Args:
            event_type: Filter by event type (process, file, network)
            device_id: Filter by device ID
            since: Start time (ISO format or relative like "1h", "24h")
            until: End time (ISO format or relative)
            limit: Maximum number of events to return (default: 100, max: 1000)
            offset: Pagination offset

        Returns:
            List of Event objects
        """
        params = {"limit": limit, "offset": offset}
        if event_type:
            params["type"] = event_type
        if device_id:
            params["device_id"] = device_id
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        response = self._client._request("GET", "/v1/events", params=params)
        return [Event.from_dict(e) for e in response.get("events", [])]

    def get(self, event_id: str) -> Event:
        """
        Get a specific event by ID.

        Args:
            event_id: The event ID

        Returns:
            Event object
        """
        response = self._client._request("GET", f"/v1/events/{event_id}")
        return Event.from_dict(response)

    def stream(
        self,
        event_types: Optional[List[str]] = None,
        device_ids: Optional[List[str]] = None,
    ) -> Iterator[Event]:
        """
        Stream events in real-time via WebSocket.

        Args:
            event_types: Filter by event types
            device_ids: Filter by device IDs

        Yields:
            Event objects as they arrive

        Note:
            This is a blocking operation. Use in a separate thread if needed.
        """
        import websocket
        import json

        ws_url = self._client._base_url.replace("https://", "wss://")
        ws_url = f"{ws_url}/v1/events/stream"

        headers = {
            "Authorization": f"Bearer {self._client._api_key}",
        }

        ws = websocket.create_connection(ws_url, header=headers)

        try:
            # Send subscription message
            subscription = {}
            if event_types:
                subscription["event_types"] = event_types
            if device_ids:
                subscription["device_ids"] = device_ids

            ws.send(json.dumps({"type": "subscribe", **subscription}))

            while True:
                message = ws.recv()
                if message:
                    data = json.loads(message)
                    if data.get("type") == "event":
                        yield Event.from_dict(data["event"])
        finally:
            ws.close()

    def export(
        self,
        format: str = "json",
        event_type: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> bytes:
        """
        Export events to file.

        Args:
            format: Export format (json, csv, parquet)
            event_type: Filter by event type
            since: Start time
            until: End time

        Returns:
            File contents as bytes
        """
        params = {"format": format}
        if event_type:
            params["type"] = event_type
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        response = self._client._http.get("/v1/events/export", params=params)
        return response.content


class DevicesResource:
    """Devices API resource."""

    def __init__(self, client: MeshLogicClient):
        self._client = client

    def list(
        self,
        status: Optional[str] = None,
        platform: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Device]:
        """
        List monitored devices.

        Args:
            status: Filter by status (online, offline, degraded)
            platform: Filter by platform (linux, macos, windows)
            limit: Maximum number of devices to return
            offset: Pagination offset

        Returns:
            List of Device objects
        """
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        if platform:
            params["platform"] = platform

        response = self._client._request("GET", "/v1/devices", params=params)
        return [Device.from_dict(d) for d in response.get("devices", [])]

    def get(self, device_id: str) -> Device:
        """
        Get a specific device by ID.

        Args:
            device_id: The device ID

        Returns:
            Device object
        """
        response = self._client._request("GET", f"/v1/devices/{device_id}")
        return Device.from_dict(response)

    def status(self) -> dict:
        """
        Get overall device fleet status.

        Returns:
            Dictionary with status counts
        """
        return self._client._request("GET", "/v1/devices/status")


class PatternsResource:
    """Patterns API resource."""

    def __init__(self, client: MeshLogicClient):
        self._client = client

    def list(
        self,
        category: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> List[Pattern]:
        """
        List detection patterns.

        Args:
            category: Filter by category
            enabled: Filter by enabled status

        Returns:
            List of Pattern objects
        """
        params = {}
        if category:
            params["category"] = category
        if enabled is not None:
            params["enabled"] = str(enabled).lower()

        response = self._client._request("GET", "/v1/patterns", params=params)
        return [Pattern.from_dict(p) for p in response.get("patterns", [])]

    def matches(
        self,
        pattern_id: Optional[str] = None,
        device_id: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 100,
    ) -> List[PatternMatch]:
        """
        Get pattern match history.

        Args:
            pattern_id: Filter by pattern ID
            device_id: Filter by device ID
            since: Start time
            limit: Maximum number of matches to return

        Returns:
            List of PatternMatch objects
        """
        params = {"limit": limit}
        if pattern_id:
            params["pattern_id"] = pattern_id
        if device_id:
            params["device_id"] = device_id
        if since:
            params["since"] = since

        response = self._client._request("GET", "/v1/patterns/matches", params=params)
        return [PatternMatch.from_dict(m) for m in response.get("matches", [])]
