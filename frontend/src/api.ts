import type {
  InstrumentSearchResult,
  MarketDataEnvelope,
  ProcessHealth,
  SourceHealth,
  StockResult,
  WatchlistPreference
} from "./types";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  headers.set("Accept", "application/json");
  if (init?.body) headers.set("Content-Type", "application/json");

  const response = await fetch(path, {
    ...init,
    headers
  });

  if (!response.ok) {
    let detail = "Request failed";
    try {
      const payload = (await response.json()) as { detail?: unknown };
      if (typeof payload.detail === "string") detail = payload.detail;
    } catch {
      // Keep the sanitized generic message.
    }
    throw new ApiError(response.status, detail);
  }

  return (await response.json()) as T;
}

export const api = {
  health: () => request<ProcessHealth>("/api/health"),
  sourceHealth: () => request<SourceHealth[]>("/api/data-sources/health"),
  overview: () => request<MarketDataEnvelope[]>("/api/market/overview"),
  watchlist: () => request<WatchlistPreference>("/api/watchlist"),
  replaceWatchlist: (expectedVersion: number, items: string[]) =>
    request<WatchlistPreference>("/api/watchlist", {
      method: "PUT",
      body: JSON.stringify({ expected_version: expectedVersion, items })
    }),
  searchStocks: (query: string) =>
    request<InstrumentSearchResult>(
      "/api/stocks?query=" + encodeURIComponent(query.trim()) + "&limit=20"
    ),
  stock: (symbol: string) =>
    request<StockResult>("/api/stocks/" + encodeURIComponent(symbol.trim().toUpperCase())),
  bars: (symbol: string) => {
    const to = new Date();
    const from = new Date(to.getTime() - 90 * 24 * 60 * 60 * 1000);
    const params = new URLSearchParams({
      from: from.toISOString(),
      to: to.toISOString(),
      timeframe: "1D",
      basis: "RAW"
    });
    return request<MarketDataEnvelope>(
      "/api/stocks/" + encodeURIComponent(symbol.trim().toUpperCase()) + "/bars?" + params
    );
  }
};
