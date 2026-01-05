/**
 * MeshLogic SDK type definitions.
 *
 * Copyright (c) 2024-2026 Mesh Logic Pty Ltd
 * Licensed under the Apache License, Version 2.0
 */

/** Event type enumeration */
export type EventType = 'process' | 'file' | 'network';

/** Event action enumeration */
export type EventAction =
  // Process actions
  | 'exec'
  | 'exit'
  | 'fork'
  // File actions
  | 'open'
  | 'write'
  | 'delete'
  | 'rename'
  // Network actions
  | 'connect'
  | 'accept'
  | 'send'
  | 'receive';

/** Base event interface */
export interface Event {
  id: string;
  type: EventType;
  action: EventAction;
  timestamp: string;
  deviceId: string;
  customerId: string;
}

/** Process event */
export interface ProcessEvent extends Event {
  type: 'process';
  pid: number;
  ppid: number;
  processName: string;
  executablePath: string;
  commandLine: string;
  user: string;
  exitCode?: number;
}

/** File event */
export interface FileEvent extends Event {
  type: 'file';
  path: string;
  targetPath?: string;
  pid: number;
  processName: string;
}

/** Network event */
export interface NetworkEvent extends Event {
  type: 'network';
  pid: number;
  processName: string;
  localAddress: string;
  localPort: number;
  remoteAddress: string;
  remotePort: number;
  protocol: 'tcp' | 'udp';
}

/** Monitored device */
export interface Device {
  id: string;
  hostname: string;
  platform: 'linux' | 'macos' | 'windows';
  osVersion: string;
  agentVersion: string;
  lastSeen: string;
  status: 'online' | 'offline' | 'degraded';
  customerId: string;
}

/** Detection pattern */
export interface Pattern {
  id: string;
  name: string;
  category: string;
  description: string;
  severity: 'info' | 'low' | 'medium' | 'high' | 'critical';
  enabled: boolean;
}

/** Pattern match result */
export interface PatternMatch {
  id: string;
  patternId: string;
  patternName: string;
  eventId: string;
  deviceId: string;
  timestamp: string;
  severity: string;
  details: Record<string, unknown>;
}

/** Device fleet status */
export interface DeviceStatus {
  total: number;
  online: number;
  offline: number;
  degraded: number;
}

/** Parameters for listing events */
export interface EventsListParams {
  eventType?: EventType;
  deviceId?: string;
  since?: string;
  until?: string;
  limit?: number;
  offset?: number;
}

/** Response from listing events */
export interface EventsListResponse {
  events: Event[];
  totalCount: number;
  hasMore: boolean;
}

/** Parameters for listing devices */
export interface DevicesListParams {
  status?: 'online' | 'offline' | 'degraded';
  platform?: 'linux' | 'macos' | 'windows';
  limit?: number;
  offset?: number;
}

/** Response from listing devices */
export interface DevicesListResponse {
  devices: Device[];
  totalCount: number;
  hasMore: boolean;
}

/** Parameters for listing patterns */
export interface PatternsListParams {
  category?: string;
  enabled?: boolean;
}

/** Response from listing patterns */
export interface PatternsListResponse {
  patterns: Pattern[];
  totalCount: number;
}

/** Parameters for listing pattern matches */
export interface MatchesParams {
  patternId?: string;
  deviceId?: string;
  since?: string;
  limit?: number;
}

/** Response from listing pattern matches */
export interface MatchesResponse {
  matches: PatternMatch[];
  totalCount: number;
  hasMore: boolean;
}
