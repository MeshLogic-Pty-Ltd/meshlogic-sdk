/**
 * MeshLogic API Client.
 *
 * Copyright (c) 2024-2026 Mesh Logic Pty Ltd
 * Licensed under the Apache License, Version 2.0
 */

import {
  MeshLogicError,
  AuthenticationError,
  RateLimitError,
  NotFoundError,
} from './errors';
import {
  Event,
  Device,
  Pattern,
  PatternMatch,
  DeviceStatus,
  EventsListParams,
  EventsListResponse,
  DevicesListParams,
  DevicesListResponse,
  PatternsListParams,
  PatternsListResponse,
  MatchesParams,
  MatchesResponse,
} from './types';

/** Default API endpoints by region */
const ENDPOINTS: Record<string, string> = {
  'ap-southeast-2': 'https://api.meshlogic.ai',
  'us-east-1': 'https://api.us.meshlogic.ai',
  'eu-west-1': 'https://api.eu.meshlogic.ai',
};

/** Client configuration options */
export interface ClientConfig {
  /** API key for authentication */
  apiKey?: string;
  /** AWS region for API endpoint (default: ap-southeast-2) */
  region?: string;
  /** Override the API base URL */
  baseUrl?: string;
  /** Request timeout in milliseconds (default: 30000) */
  timeout?: number;
}

/**
 * MeshLogic API client.
 *
 * @example
 * ```typescript
 * const client = new MeshLogicClient({ apiKey: 'your-api-key' });
 * const events = await client.events.list({ eventType: 'process', limit: 100 });
 * ```
 */
export class MeshLogicClient {
  private apiKey: string;
  private baseUrl: string;
  private timeout: number;

  /** Events API resource */
  public events: EventsResource;
  /** Devices API resource */
  public devices: DevicesResource;
  /** Patterns API resource */
  public patterns: PatternsResource;

  constructor(config: ClientConfig = {}) {
    this.apiKey = config.apiKey || process.env.MESHLOGIC_API_KEY || '';
    if (!this.apiKey) {
      throw new AuthenticationError(
        'API key required. Provide via apiKey option or MESHLOGIC_API_KEY environment variable.'
      );
    }

    const region = config.region || 'ap-southeast-2';
    this.baseUrl = config.baseUrl || ENDPOINTS[region] || ENDPOINTS['ap-southeast-2'];
    this.timeout = config.timeout || 30000;

    // Initialize resources
    this.events = new EventsResource(this);
    this.devices = new DevicesResource(this);
    this.patterns = new PatternsResource(this);
  }

  /** Make an API request */
  async request<T>(
    method: string,
    path: string,
    params?: Record<string, string | number | boolean | undefined>,
    body?: unknown
  ): Promise<T> {
    const url = new URL(path, this.baseUrl);

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          url.searchParams.set(key, String(value));
        }
      });
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url.toString(), {
        method,
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
          'User-Agent': 'meshlogic-typescript/0.1.0',
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        switch (response.status) {
          case 401:
            throw new AuthenticationError(errorData.message || 'Invalid or expired API key');
          case 404:
            throw new NotFoundError(errorData.message || `Resource not found: ${path}`);
          case 429:
            const retryAfter = parseInt(response.headers.get('Retry-After') || '60', 10);
            throw new RateLimitError(errorData.message || 'Rate limit exceeded', retryAfter);
          default:
            throw new MeshLogicError(
              errorData.message || 'Unknown error',
              errorData.code || 'UNKNOWN',
              response.status
            );
        }
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof MeshLogicError) {
        throw error;
      }
      if (error instanceof Error && error.name === 'AbortError') {
        throw new MeshLogicError('Request timeout', 'TIMEOUT');
      }
      throw new MeshLogicError(String(error), 'NETWORK_ERROR');
    }
  }
}

/** Events API resource */
class EventsResource {
  constructor(private client: MeshLogicClient) {}

  /** List events with optional filtering */
  async list(params: EventsListParams = {}): Promise<EventsListResponse> {
    return this.client.request<EventsListResponse>('GET', '/v1/events', {
      type: params.eventType,
      device_id: params.deviceId,
      since: params.since,
      until: params.until,
      limit: params.limit || 100,
      offset: params.offset || 0,
    });
  }

  /** Get a specific event by ID */
  async get(eventId: string): Promise<Event> {
    return this.client.request<Event>('GET', `/v1/events/${eventId}`);
  }

  /** Export events to file */
  async export(params: {
    format?: 'json' | 'csv' | 'parquet';
    eventType?: string;
    since?: string;
    until?: string;
  } = {}): Promise<Blob> {
    const url = new URL('/v1/events/export', this.client['baseUrl']);
    if (params.format) url.searchParams.set('format', params.format);
    if (params.eventType) url.searchParams.set('type', params.eventType);
    if (params.since) url.searchParams.set('since', params.since);
    if (params.until) url.searchParams.set('until', params.until);

    const response = await fetch(url.toString(), {
      headers: {
        Authorization: `Bearer ${this.client['apiKey']}`,
      },
    });

    if (!response.ok) {
      throw new MeshLogicError('Export failed', 'EXPORT_ERROR', response.status);
    }

    return response.blob();
  }
}

/** Devices API resource */
class DevicesResource {
  constructor(private client: MeshLogicClient) {}

  /** List monitored devices */
  async list(params: DevicesListParams = {}): Promise<DevicesListResponse> {
    return this.client.request<DevicesListResponse>('GET', '/v1/devices', {
      status: params.status,
      platform: params.platform,
      limit: params.limit || 100,
      offset: params.offset || 0,
    });
  }

  /** Get a specific device by ID */
  async get(deviceId: string): Promise<Device> {
    return this.client.request<Device>('GET', `/v1/devices/${deviceId}`);
  }

  /** Get overall device fleet status */
  async status(): Promise<DeviceStatus> {
    return this.client.request<DeviceStatus>('GET', '/v1/devices/status');
  }
}

/** Patterns API resource */
class PatternsResource {
  constructor(private client: MeshLogicClient) {}

  /** List detection patterns */
  async list(params: PatternsListParams = {}): Promise<PatternsListResponse> {
    return this.client.request<PatternsListResponse>('GET', '/v1/patterns', {
      category: params.category,
      enabled: params.enabled,
    });
  }

  /** Get pattern match history */
  async matches(params: MatchesParams = {}): Promise<MatchesResponse> {
    return this.client.request<MatchesResponse>('GET', '/v1/patterns/matches', {
      pattern_id: params.patternId,
      device_id: params.deviceId,
      since: params.since,
      limit: params.limit || 100,
    });
  }
}
