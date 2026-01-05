# MeshLogic SDK

Official client libraries for the MeshLogic API.

## Overview

The MeshLogic SDK provides programmatic access to behavioral monitoring data collected by MeshLogic agents. Use these libraries to:

- Query process, file, and network events
- Stream real-time events via WebSocket
- Export data for SIEM/SOAR integration
- Build custom dashboards and reports

## Available SDKs

| Language | Package | Status |
|----------|---------|--------|
| Python | `meshlogic` | Stable |
| Go | `github.com/MeshLogic-Pty-Ltd/meshlogic-sdk/go/meshlogic` | Stable |
| TypeScript | `@meshlogic/sdk` | Stable |

## Installation

### Python

```bash
pip install meshlogic
```

### Go

```bash
go get github.com/MeshLogic-Pty-Ltd/meshlogic-sdk/go/meshlogic
```

### TypeScript/JavaScript

```bash
npm install @meshlogic/sdk
# or
yarn add @meshlogic/sdk
```

## Quick Start

### Python

```python
from meshlogic import MeshLogicClient

client = MeshLogicClient(
    api_key="your-api-key",
    region="ap-southeast-2"
)

# Query recent process events
events = client.events.list(
    event_type="process",
    limit=100,
    since="1h"
)

for event in events:
    print(f"{event.timestamp}: {event.process_name} ({event.pid})")
```

### Go

```go
package main

import (
    "context"
    "fmt"
    "github.com/MeshLogic-Pty-Ltd/meshlogic-sdk/go/meshlogic"
)

func main() {
    client := meshlogic.NewClient(
        meshlogic.WithAPIKey("your-api-key"),
        meshlogic.WithRegion("ap-southeast-2"),
    )

    events, err := client.Events.List(context.Background(), &meshlogic.EventsListParams{
        EventType: "process",
        Limit:     100,
        Since:     "1h",
    })
    if err != nil {
        panic(err)
    }

    for _, event := range events {
        fmt.Printf("%s: %s (%d)\n", event.Timestamp, event.ProcessName, event.PID)
    }
}
```

### TypeScript

```typescript
import { MeshLogicClient } from '@meshlogic/sdk';

const client = new MeshLogicClient({
  apiKey: 'your-api-key',
  region: 'ap-southeast-2',
});

const events = await client.events.list({
  eventType: 'process',
  limit: 100,
  since: '1h',
});

for (const event of events) {
  console.log(`${event.timestamp}: ${event.processName} (${event.pid})`);
}
```

## Authentication

All API requests require authentication via API key:

1. Log in to the MeshLogic dashboard
2. Navigate to Settings → API Keys
3. Create a new API key with appropriate scopes
4. Store securely (environment variable recommended)

```bash
export MESHLOGIC_API_KEY="your-api-key"
```

## API Reference

### Events

| Method | Description |
|--------|-------------|
| `events.list()` | List events with filtering |
| `events.get(id)` | Get a specific event |
| `events.stream()` | Real-time event stream (WebSocket) |
| `events.export()` | Export events to file |

### Devices

| Method | Description |
|--------|-------------|
| `devices.list()` | List monitored devices |
| `devices.get(id)` | Get device details |
| `devices.status()` | Get device health status |

### Patterns

| Method | Description |
|--------|-------------|
| `patterns.list()` | List detection patterns |
| `patterns.matches()` | Get pattern match history |

## Real-time Streaming

```python
from meshlogic import MeshLogicClient

client = MeshLogicClient(api_key="your-api-key")

# Stream events in real-time
for event in client.events.stream(event_types=["process", "network"]):
    print(f"[{event.type}] {event.summary}")
```

## Error Handling

```python
from meshlogic import MeshLogicClient, MeshLogicError, RateLimitError

client = MeshLogicClient(api_key="your-api-key")

try:
    events = client.events.list(limit=1000)
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except MeshLogicError as e:
    print(f"API error: {e.message} (code: {e.code})")
```

## Rate Limits

| Tier | Requests/minute | WebSocket connections |
|------|-----------------|----------------------|
| Free | 60 | 1 |
| Pro | 600 | 5 |
| Enterprise | Unlimited | Unlimited |

## Support

- Documentation: https://meshlogic.ai/docs/sdk
- Issues: https://github.com/MeshLogic-Pty-Ltd/meshlogic-sdk/issues
- Email: support@meshlogic.ai

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
