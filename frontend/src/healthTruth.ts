import type { ProcessHealth } from "./types";

/** Process health is not market LIVE availability, particularly offline. */
export function healthBadge(health: ProcessHealth | null | undefined) {
  if (health?.status === "OK") return "OK";
  if (health?.status === "UNHEALTHY") return "UNHEALTHY";
  return "UNAVAILABLE";
}

export function providerModeLabel(health: ProcessHealth | null | undefined) {
  if (!health) return "Unknown";
  return health.provider_enabled ? "Enabled" : "Disabled / offline-safe";
}
