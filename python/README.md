# MeshLogic Python SDK

Official Python client library for the MeshLogic API.

## Installation

```bash
pip install meshlogic
```

## Quick Start

```python
from meshlogic import MeshLogicClient

# Initialize client
client = MeshLogicClient(api_key="your-api-key")

# Query recent process events
events = client.events.list(
    event_type="process",
    limit=100,
    since="1h"
)

for event in events:
    print(f"{event.timestamp}: {event.process_name} ({event.pid})")
```

## Authentication

Set your API key via environment variable (recommended):

```bash
export MESHLOGIC_API_KEY="your-api-key"
```

Or pass directly to the client:

```python
client = MeshLogicClient(api_key="your-api-key")
```

## Usage Examples

### List Events

```python
# Get process events from the last hour
events = client.events.list(
    event_type="process",
    since="1h",
    limit=100
)

# Get file events for a specific device
events = client.events.list(
    event_type="file",
    device_id="device-123",
    since="24h"
)
```

### Stream Events in Real-time

```python
for event in client.events.stream(event_types=["process", "network"]):
    print(f"[{event.type}] {event.timestamp}: {event.process_name}")
```

### List Devices

```python
# Get all online devices
devices = client.devices.list(status="online")

for device in devices:
    print(f"{device.hostname} ({device.platform}) - {device.agent_version}")
```

### Pattern Matches

```python
# Get recent pattern matches
matches = client.patterns.matches(since="24h", limit=50)

for match in matches:
    print(f"[{match.severity}] {match.pattern_name} on {match.device_id}")
```

## Error Handling

```python
from meshlogic import MeshLogicClient, MeshLogicError, RateLimitError

try:
    events = client.events.list(limit=1000)
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except MeshLogicError as e:
    print(f"API error: {e.message}")
```

## License

Apache License 2.0
