# MeshLogic Go SDK

Official Go client library for the MeshLogic API.

## Installation

```bash
go get github.com/MeshLogic-Pty-Ltd/meshlogic-sdk/go/meshlogic
```

## Quick Start

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/MeshLogic-Pty-Ltd/meshlogic-sdk/go/meshlogic"
)

func main() {
    // Initialize client
    client, err := meshlogic.NewClient(
        meshlogic.WithAPIKey("your-api-key"),
        meshlogic.WithRegion("ap-southeast-2"),
    )
    if err != nil {
        log.Fatal(err)
    }

    // Query recent process events
    ctx := context.Background()
    resp, err := client.Events.List(ctx, &meshlogic.EventsListParams{
        EventType: "process",
        Limit:     100,
        Since:     "1h",
    })
    if err != nil {
        log.Fatal(err)
    }

    for _, event := range resp.Events {
        fmt.Printf("%s: %s (%d)\n", event.Timestamp, event.ProcessName, event.PID)
    }
}
```

## Authentication

Set your API key via environment variable (recommended):

```bash
export MESHLOGIC_API_KEY="your-api-key"
```

Or pass directly to the client:

```go
client, err := meshlogic.NewClient(
    meshlogic.WithAPIKey("your-api-key"),
)
```

## Usage Examples

### List Events

```go
// Get process events from the last hour
resp, err := client.Events.List(ctx, &meshlogic.EventsListParams{
    EventType: "process",
    Since:     "1h",
    Limit:     100,
})

// Get file events for a specific device
resp, err := client.Events.List(ctx, &meshlogic.EventsListParams{
    EventType: "file",
    DeviceID:  "device-123",
    Since:     "24h",
})
```

### List Devices

```go
// Get all online devices
resp, err := client.Devices.List(ctx, &meshlogic.DevicesListParams{
    Status: "online",
})

for _, device := range resp.Devices {
    fmt.Printf("%s (%s) - %s\n", device.Hostname, device.Platform, device.AgentVersion)
}

// Get fleet status
status, err := client.Devices.Status(ctx)
fmt.Printf("Online: %d, Offline: %d\n", status.Online, status.Offline)
```

### Pattern Matches

```go
// Get recent pattern matches
resp, err := client.Patterns.Matches(ctx, &meshlogic.MatchesParams{
    Since: "24h",
    Limit: 50,
})

for _, match := range resp.Matches {
    fmt.Printf("[%s] %s on %s\n", match.Severity, match.PatternName, match.DeviceID)
}
```

## Error Handling

```go
resp, err := client.Events.List(ctx, params)
if err != nil {
    switch e := err.(type) {
    case *meshlogic.RateLimitError:
        fmt.Printf("Rate limited. Retry after %d seconds\n", e.RetryAfter)
    case *meshlogic.AuthenticationError:
        fmt.Println("Invalid API key")
    case *meshlogic.NotFoundError:
        fmt.Println("Resource not found")
    default:
        fmt.Printf("API error: %v\n", err)
    }
}
```

## License

Apache License 2.0
