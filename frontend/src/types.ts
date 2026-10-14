export type AvailabilityState =
  | "LIVE"
  | "PERIODIC_LIVE"
  | "LATEST_VALID"
  | "EOD_CONFIRMED"
  | "STALE"
  | "GAP_RECOVERING"
  | "DELAYED"
  | "ENTITLEMENT_BLOCKED"
  | "UNAVAILABLE"
  | "UNKNOWN";

export interface Rights {
  read: "VERIFIED" | "BLOCKED" | "UNKNOWN";
  redisplay: "VERIFIED" | "BLOCKED" | "UNKNOWN";
  retained_use: "VERIFIED" | "BLOCKED" | "UNKNOWN";
  evidence_ref: string | null;
  verified_until: string | null;
}

export interface QuotePayload {
  kind: "quote";
  last_price: number | null;
  reference_price: number | null;
  ceiling_price: number | null;
  floor_price: number | null;
  cumulative_volume: number | null;
  cumulative_turnover: number | null;
}

export interface BarsItem {
  start_at: string;
  end_at: string | null;
  update_at: string | null;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number | null;
  turnover: number | null;
  provisional: boolean | null;
  revision: number;
}

export interface BarsGap {
  from: string;
  to: string;
  reason: string;
  capability: "BARS" | "TICKS" | "QUOTE" | "INDEX";
}

export interface BarsPayload {
  kind: "bars";
  timeframe: "1D";
  from: string;
  to: string;
  items: BarsItem[];
  gaps: BarsGap[];
}

export interface IndexSummaryPayload {
  kind: "index_summary";
  value: number | null;
  change_value: number | null;
  change_percent: number | null;
  up_count: number | null;
  down_count: number | null;
  unchanged_count: number | null;
  volume: number | null;
  turnover: number | null;
}

export type MarketPayload = QuotePayload | BarsPayload | IndexSummaryPayload | null;

export interface MarketObservation {
  profile: "INVESTOR" | "ISOLATED_TEST";
  instrument_id: string | null;
  symbol: string | null;
  instrument_type: "STOCK" | "INDEX" | "UNKNOWN";
  venue: "HOSE" | "HNX" | "UPCOM" | "UNKNOWN";
  board_id: string | null;
  record_id: string | null;
  revision: number | null;
  source_id: string | null;
  origin_provider: string | null;
  source_revision: string | null;
  retrieval_channel:
    | "WEBSOCKET"
    | "HISTORICAL_API"
    | "LOCAL_STORE"
    | "TEST_FIXTURE"
    | "UNAVAILABLE";
  event_at: string | null;
  as_of: string | null;
  received_at: string | null;
  first_available_at: string | null;
  data_mode:
    | "VERIFIED_PROVIDER"
    | "PROVIDER_NATIVE_UNVERIFIED"
    | "UNAVAILABLE"
    | "SYNTHETIC";
  freshness_state: AvailabilityState;
  quality: "VALID" | "PARTIAL" | "INVALID" | "UNKNOWN";
  mapping_state: "VERIFIED" | "UNKNOWN" | "BLOCKED";
  completeness: "COMPLETE" | "PARTIAL" | "UNKNOWN";
  price_basis: "RAW" | "ADJUSTED" | "UNKNOWN" | "NOT_APPLICABLE";
  price_unit: "VND_PER_SHARE" | "INDEX_POINTS" | "UNKNOWN" | "NOT_APPLICABLE";
  volume_unit: "SHARES" | "UNKNOWN" | "NOT_APPLICABLE";
  turnover_unit: "VND" | "UNKNOWN" | "NOT_APPLICABLE";
  adjustment_version: string | null;
  calendar_version: string | null;
  session: string | null;
  freshness_policy_version: string | null;
  rights: Rights;
  selection_audit_id: string;
  selection_reason: string;
  missing_fields: string[];
  payload: MarketPayload;
}

export interface MarketDataEnvelope {
  contract_version: "market-data-v0.4-candidate";
  request_id: string;
  generated_at: string;
  data: MarketObservation;
}

export interface Instrument {
  instrument_id: string;
  symbol: string;
  instrument_type: "STOCK" | "INDEX" | "UNKNOWN";
  venue: "HOSE" | "HNX" | "UPCOM" | "UNKNOWN";
  board_id: string | null;
}

export interface InstrumentSearchResult {
  items: Instrument[];
  universe_source: string | null;
  universe_revision: string | null;
  coverage: "COMPLETE" | "PARTIAL" | "UNKNOWN";
  cursor: string | null;
}

export interface StockResult {
  instrument: Instrument;
  quote: MarketDataEnvelope;
}

export interface ProcessHealth {
  contract_version: "market-data-v0.4-candidate";
  status: "OK" | "UNHEALTHY";
  provider_enabled: boolean;
}

export interface SourceHealth {
  capability: "QUOTE" | "BARS" | "INDEX";
  readiness: "UNKNOWN" | "UNAVAILABLE";
  state: "UNKNOWN" | "UNAVAILABLE";
  gap_state: "UNKNOWN";
  rights_state: "UNKNOWN";
  verified_until: string | null;
  reason: "NOT_INTEGRATED";
}

export interface WatchlistPreference {
  version: number;
  items: string[];
  updated_at: string | null;
}
