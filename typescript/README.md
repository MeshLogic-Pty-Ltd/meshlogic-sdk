# MeshLogic TypeScript/JavaScript SDK

Official TypeScript/JavaScript client library for the MeshLogic API.

## Installation

```bash
npm install @meshlogic/sdk
# or
yarn add @meshlogic/sdk
# or
pnpm add @meshlogic/sdk
```

## Quick Start

```typescript
import { MeshLogicClient } from '@meshlogic/sdk';

// Initialize client
const client = new MeshLogicClient({
  apiKey: 'your-api-key',
  region: 'ap-southeast-2',
});

// Query recent process events
const { events } = await client.events.list({
  eventType: 'process',
  limit: 100,
  since: '1h',
});

for (const event of events) {
  console.log(`${event.timestamp}: ${event.processName} (${event.pid})`);
}
```

## Authentication

Set your API key via environment variable (recommended):

```bash
export MESHLOGIC_API_KEY="your-api-key"
```

Or pass directly to the client:

```typescript
const client = new MeshLogicClient({ apiKey: 'your-api-key' });
```

## Usage Examples

### List Events

```typescript
// Get process events from the last hour
const { events } = await client.events.list({
  eventType: 'process',
  since: '1h',
  limit: 100,
});

// Get file events for a specific device
const { events } = await client.events.list({
  eventType: 'file',
  deviceId: 'device-123',
  since: '24h',
});
```

### List Devices

```typescript
// Get all online devices
const { devices } = await client.devices.list({ status: 'online' });

for (const device of devices) {
  console.log(`${device.hostname} (${device.platform}) - ${device.agentVersion}`);
}

// Get fleet status
const status = await client.devices.status();
console.log(`Online: ${status.online}, Offline: ${status.offline}`);
```

### Pattern Matches

```typescript
// Get recent pattern matches
const { matches } = await client.patterns.matches({
  since: '24h',
  limit: 50,
});

for (const match of matches) {
  console.log(`[${match.severity}] ${match.patternName} on ${match.deviceId}`);
}
```

## Error Handling

```typescript
import {
  MeshLogicClient,
  MeshLogicError,
  RateLimitError,
  AuthenticationError,
} from '@meshlogic/sdk';

try {
  const { events } = await client.events.list({ limit: 1000 });
} catch (error) {
  if (error instanceof RateLimitError) {
    console.log(`Rate limited. Retry after ${error.retryAfter} seconds`);
  } else if (error instanceof AuthenticationError) {
    console.log('Invalid API key');
  } else if (error instanceof MeshLogicError) {
    console.log(`API error: ${error.message}`);
  }
}
```

## TypeScript Support

This SDK is written in TypeScript and provides full type definitions out of the box.

```typescript
import type { Event, ProcessEvent, Device, Pattern } from '@meshlogic/sdk';

// Type-safe event handling
function handleEvent(event: Event) {
  if (event.type === 'process') {
    const processEvent = event as ProcessEvent;
    console.log(processEvent.processName);
  }
}
```

## License

Apache License 2.0
