"""
MeshLogic SDK - Python client for the MeshLogic API.

Copyright (c) 2024-2026 Mesh Logic Pty Ltd
Licensed under the Apache License, Version 2.0
"""

from .client import MeshLogicClient
from .exceptions import (
    MeshLogicError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)
from .types import (
    Event,
    ProcessEvent,
    FileEvent,
    NetworkEvent,
    Device,
    Pattern,
    PatternMatch,
)

__version__ = "0.1.0"
__author__ = "Mesh Logic Pty Ltd"
__email__ = "support@meshlogic.ai"

__all__ = [
    # Client
    "MeshLogicClient",
    # Exceptions
    "MeshLogicError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
    # Types
    "Event",
    "ProcessEvent",
    "FileEvent",
    "NetworkEvent",
    "Device",
    "Pattern",
    "PatternMatch",
]
