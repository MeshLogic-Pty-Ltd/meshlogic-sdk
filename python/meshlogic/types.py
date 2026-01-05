"""
MeshLogic SDK type definitions.

Copyright (c) 2024-2026 Mesh Logic Pty Ltd
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class EventType(str, Enum):
    """Event type enumeration."""

    PROCESS = "process"
    FILE = "file"
    NETWORK = "network"


class EventAction(str, Enum):
    """Event action enumeration."""

    # Process actions
    EXEC = "exec"
    EXIT = "exit"
    FORK = "fork"

    # File actions
    OPEN = "open"
    WRITE = "write"
    DELETE = "delete"
    RENAME = "rename"

    # Network actions
    CONNECT = "connect"
    ACCEPT = "accept"
    SEND = "send"
    RECEIVE = "receive"


@dataclass
class Event:
    """Base event class."""

    id: str
    type: EventType
    action: EventAction
    timestamp: datetime
    device_id: str
    customer_id: str
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Event:
        """Create an Event from a dictionary."""
        event_type = EventType(data.get("type", "process"))

        # Dispatch to specific event type
        if event_type == EventType.PROCESS:
            return ProcessEvent.from_dict(data)
        elif event_type == EventType.FILE:
            return FileEvent.from_dict(data)
        elif event_type == EventType.NETWORK:
            return NetworkEvent.from_dict(data)

        return cls(
            id=data["id"],
            type=event_type,
            action=EventAction(data.get("action", "exec")),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            device_id=data["device_id"],
            customer_id=data["customer_id"],
            raw=data,
        )


@dataclass
class ProcessEvent(Event):
    """Process event (exec, exit, fork)."""

    pid: int = 0
    ppid: int = 0
    process_name: str = ""
    executable_path: str = ""
    command_line: str = ""
    user: str = ""
    exit_code: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProcessEvent:
        """Create a ProcessEvent from a dictionary."""
        return cls(
            id=data["id"],
            type=EventType.PROCESS,
            action=EventAction(data.get("action", "exec")),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            device_id=data["device_id"],
            customer_id=data["customer_id"],
            raw=data,
            pid=data.get("pid", 0),
            ppid=data.get("ppid", 0),
            process_name=data.get("process_name", ""),
            executable_path=data.get("executable_path", ""),
            command_line=data.get("command_line", ""),
            user=data.get("user", ""),
            exit_code=data.get("exit_code"),
        )


@dataclass
class FileEvent(Event):
    """File event (open, write, delete, rename)."""

    path: str = ""
    target_path: Optional[str] = None  # For rename operations
    pid: int = 0
    process_name: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> FileEvent:
        """Create a FileEvent from a dictionary."""
        return cls(
            id=data["id"],
            type=EventType.FILE,
            action=EventAction(data.get("action", "open")),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            device_id=data["device_id"],
            customer_id=data["customer_id"],
            raw=data,
            path=data.get("path", ""),
            target_path=data.get("target_path"),
            pid=data.get("pid", 0),
            process_name=data.get("process_name", ""),
        )


@dataclass
class NetworkEvent(Event):
    """Network event (connect, accept, send, receive)."""

    pid: int = 0
    process_name: str = ""
    local_address: str = ""
    local_port: int = 0
    remote_address: str = ""
    remote_port: int = 0
    protocol: str = "tcp"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NetworkEvent:
        """Create a NetworkEvent from a dictionary."""
        return cls(
            id=data["id"],
            type=EventType.NETWORK,
            action=EventAction(data.get("action", "connect")),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            device_id=data["device_id"],
            customer_id=data["customer_id"],
            raw=data,
            pid=data.get("pid", 0),
            process_name=data.get("process_name", ""),
            local_address=data.get("local_address", ""),
            local_port=data.get("local_port", 0),
            remote_address=data.get("remote_address", ""),
            remote_port=data.get("remote_port", 0),
            protocol=data.get("protocol", "tcp"),
        )


@dataclass
class Device:
    """Monitored device."""

    id: str
    hostname: str
    platform: str  # linux, macos, windows
    os_version: str
    agent_version: str
    last_seen: datetime
    status: str  # online, offline, degraded
    customer_id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Device:
        """Create a Device from a dictionary."""
        return cls(
            id=data["id"],
            hostname=data["hostname"],
            platform=data["platform"],
            os_version=data["os_version"],
            agent_version=data["agent_version"],
            last_seen=datetime.fromisoformat(data["last_seen"]),
            status=data["status"],
            customer_id=data["customer_id"],
        )


@dataclass
class Pattern:
    """Detection pattern."""

    id: str
    name: str
    category: str
    description: str
    severity: str  # info, low, medium, high, critical
    enabled: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Pattern:
        """Create a Pattern from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            description=data["description"],
            severity=data["severity"],
            enabled=data.get("enabled", True),
        )


@dataclass
class PatternMatch:
    """Pattern match result."""

    id: str
    pattern_id: str
    pattern_name: str
    event_id: str
    device_id: str
    timestamp: datetime
    severity: str
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PatternMatch:
        """Create a PatternMatch from a dictionary."""
        return cls(
            id=data["id"],
            pattern_id=data["pattern_id"],
            pattern_name=data["pattern_name"],
            event_id=data["event_id"],
            device_id=data["device_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            severity=data["severity"],
            details=data.get("details", {}),
        )
