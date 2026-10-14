import { FormEvent, useEffect, useMemo, useState } from "react";
import { api, ApiError } from "./api";
import type {
  BarsPayload,
  Instrument,
  MarketDataEnvelope,
  ProcessHealth,
  SourceHealth,
  StockResult,
  WatchlistPreference
} from "./types";
import {
  EmptyState,
  formatDate,
  formatNumber,
  Icon,
  Metric,
  Panel,
  RefreshButton,
  SectionHeading,
  Skeleton,
  SourceBadge,
  StateBadge
} from "./ui";

type RouteKey = "overview" | "watchlist" | "stock" | "sources";

interface RouteState {
  key: RouteKey;
  symbol?: string;
}

function parseRoute(pathname: string): RouteState {
  if (pathname.startsWith("/watchlist")) return { key: "watchlist" };
  if (pathname.startsWith("/settings/data-sources")) return { key: "sources" };
  if (pathname.startsWith("/stocks/")) {
    const symbol = decodeURIComponent(pathname.slice("/stocks/".length)).trim();
    return { key: "stock", symbol: symbol || undefined };
  }
  if (pathname === "/stocks") return { key: "stock" };
  return { key: "overview" };
}

function usePath() {
  const [pathname, setPathname] = useState(() => window.location.pathname);

  useEffect(() => {
    const onPopState = () => setPathname(window.location.pathname);
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  const navigate = (path: string) => {
    if (window.location.pathname === path) return;
    window.history.pushState({}, "", path);
    setPathname(path);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return { pathname, navigate };
}

function useResource<T>(key: string, loader: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let live = true;
    setLoading(true);
    setError(null);
    loader()
      .then((value) => {
        if (live) setData(value);
      })
      .catch((reason: unknown) => {
        if (live) setError(reason instanceof Error ? reason : new Error("Request failed"));
      })
      .finally(() => {
        if (live) setLoading(false);
      });
    return () => {
      live = false;
    };
  }, [key]);

  return { data, loading, error };
}

function NavItem({
  href,
  icon,
  label,
  active,
  onNavigate
}: {
  href: string;
  icon: "overview" | "watchlist" | "stock" | "sources";
  label: string;
  active: boolean;
  onNavigate: (path: string) => void;
}) {
  return (
    <a
      href={href}
      className={"nav-item " + (active ? "nav-item--active" : "")}
      onClick={(event) => {
        event.preventDefault();
        onNavigate(href);
      }}
    >
      <Icon name={icon} />
      <span>{label}</span>
    </a>
  );
}

function AppShell({
  route,
  onNavigate,
  children
}: {
  route: RouteState;
  onNavigate: (path: string) => void;
  children: React.ReactNode;
}) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button className="brand" type="button" onClick={() => onNavigate("/overview")}>
          <span className="brand__mark">F2</span>
          <span className="brand__copy">
            <strong>FOX2</strong>
            <small>Local market workspace</small>
          </span>
        </button>

        <nav className="sidebar__nav" aria-label="Primary navigation">
          <NavItem href="/overview" icon="overview" label="Overview" active={route.key === "overview"} onNavigate={onNavigate} />
          <NavItem href="/watchlist" icon="watchlist" label="Watchlist" active={route.key === "watchlist"} onNavigate={onNavigate} />
          <NavItem href="/stocks" icon="stock" label="Stock360" active={route.key === "stock"} onNavigate={onNavigate} />
          <NavItem href="/settings/data-sources" icon="sources" label="Data Sources" active={route.key === "sources"} onNavigate={onNavigate} />
        </nav>

        <div className="sidebar__footer">
          <div className="safety-card">
            <Icon name="shield" />
            <div>
              <strong>Offline-safe M1-A</strong>
              <span>No order or broker-write capability</span>
            </div>
          </div>
          <span className="build-label">Presentation slice · v0.1</span>
        </div>
      </aside>

      <div className="workspace">
        <header className="topbar">
          <div className="topbar__context">
            <span className="topbar__pulse" />
            <span>localhost</span>
            <span className="topbar__separator">/</span>
            <span>Investor view</span>
          </div>
          <div className="topbar__safety">
            <Icon name="shield" size={16} />
            <span>Verified data only · no synthetic fallback</span>
          </div>
        </header>
        <main className="content">{children}</main>
      </div>

      <nav className="mobile-nav" aria-label="Mobile navigation">
        <NavItem href="/overview" icon="overview" label="Overview" active={route.key === "overview"} onNavigate={onNavigate} />
        <NavItem href="/watchlist" icon="watchlist" label="Watchlist" active={route.key === "watchlist"} onNavigate={onNavigate} />
        <NavItem href="/stocks" icon="stock" label="Stock360" active={route.key === "stock"} onNavigate={onNavigate} />
        <NavItem href="/settings/data-sources" icon="sources" label="Sources" active={route.key === "sources"} onNavigate={onNavigate} />
      </nav>
    </div>
  );
}

function ErrorNotice({ error }: { error: Error }) {
  const status = error instanceof ApiError ? "HTTP " + error.status : "LOCAL API";
  return (
    <div className="notice notice--error" role="status">
      <div>
        <strong>{status} unavailable</strong>
        <p>{error.message || "FOX2 backend did not return an accepted response."}</p>
      </div>
      <StateBadge state="UNAVAILABLE" />
    </div>
  );
}

function MarketCard({ envelope, onOpen }: { envelope: MarketDataEnvelope; onOpen: (symbol: string) => void }) {
  const observation = envelope.data;
  const payload = observation.payload?.kind === "index_summary" ? observation.payload : null;
  const symbol = observation.symbol || "Unknown index";
  const change = payload?.change_percent ?? null;
  const changeClass = change === null ? "" : change > 0 ? "positive" : change < 0 ? "negative" : "neutral";

  return (
    <Panel className="market-card">
      <div className="market-card__header">
        <div>
          <span className="market-card__venue">{observation.venue}</span>
          <h2>{symbol}</h2>
        </div>
        <SourceBadge observation={observation} />
      </div>

      <div className="market-card__value-row">
        <span className="market-card__value">{formatNumber(payload?.value)}</span>
        <span className={"market-card__change " + changeClass}>
          {change === null ? "Change unavailable" : (change > 0 ? "+" : "") + formatNumber(change) + "%"}
        </span>
      </div>

      <div className="market-card__metrics">
        <Metric label="Advancing" value={formatNumber(payload?.up_count, 0)} />
        <Metric label="Declining" value={formatNumber(payload?.down_count, 0)} />
        <Metric label="Turnover" value={formatNumber(payload?.turnover, 0)} hint={observation.turnover_unit.replaceAll("_", " ")} />
      </div>

      <div className="market-card__footer">
        <span>As of {formatDate(observation.as_of)}</span>
        {observation.instrument_type === "STOCK" && observation.symbol ? (
          <button type="button" className="text-link" onClick={() => onOpen(observation.symbol!)}>
            Open Stock360 <Icon name="chevron" size={14} />
          </button>
        ) : null}
      </div>
    </Panel>
  );
}

function OverviewPage({ onNavigate }: { onNavigate: (path: string) => void }) {
  const [revision, setRevision] = useState(0);
  const overview = useResource("overview-" + revision, api.overview);
  const health = useResource("health-" + revision, api.health);
  const sources = useResource("sources-" + revision, api.sourceHealth);

  const refreshedAt = useMemo(() => new Date().toISOString(), [revision]);

  return (
    <div className="page">
      <SectionHeading
        eyebrow="M1-A · Market workspace"
        title="Market Overview"
        description="A truthful localhost view. Missing market evidence stays missing — FOX2 never substitutes a synthetic price, trend or score."
        action={<RefreshButton onClick={() => setRevision((value) => value + 1)} disabled={overview.loading} />}
      />

      <div className="truth-strip">
        <div>
          <span className="truth-strip__label">Runtime</span>
          {health.loading ? <span className="muted">Checking…</span> :
            health.error ? <StateBadge state="UNAVAILABLE" /> :
            <StateBadge state={health.data?.status === "OK" ? "LIVE" : "UNAVAILABLE"} />}
        </div>
        <div>
          <span className="truth-strip__label">Provider mode</span>
          <span>{health.data?.provider_enabled ? "Enabled" : "Disabled / offline-safe"}</span>
        </div>
        <div>
          <span className="truth-strip__label">Last UI refresh</span>
          <span>{formatDate(refreshedAt)}</span>
        </div>
        <button className="text-link" type="button" onClick={() => onNavigate("/settings/data-sources")}>
          Inspect sources <Icon name="chevron" size={14} />
        </button>
      </div>

      {overview.error ? <ErrorNotice error={overview.error} /> : null}

      <div className="market-grid">
        {overview.loading ? (
          <>
            <Panel><Skeleton lines={5} /></Panel>
            <Panel><Skeleton lines={5} /></Panel>
          </>
        ) : overview.data && overview.data.length > 0 ? (
          overview.data.map((item) => (
            <MarketCard
              key={item.request_id}
              envelope={item}
              onOpen={(symbol) => onNavigate("/stocks/" + encodeURIComponent(symbol))}
            />
          ))
        ) : (
          <Panel className="span-2">
            <EmptyState
              icon="database"
              title="Market overview unavailable"
              body="The backend returned no accepted index observations. FOX2 will not fabricate index values or breadth."
            />
          </Panel>
        )}
      </div>

      <div className="two-column">
        <Panel>
          <div className="panel-heading">
            <div>
              <span className="eyebrow">Source readiness</span>
              <h2>Market data capabilities</h2>
            </div>
            <Icon name="database" />
          </div>

          {sources.loading ? <Skeleton lines={4} /> :
            sources.error ? <ErrorNotice error={sources.error} /> :
            sources.data?.map((source) => (
              <div className="source-row" key={source.capability}>
                <div>
                  <strong>{source.capability}</strong>
                  <span>{source.reason.replaceAll("_", " ")}</span>
                </div>
                <StateBadge state={source.state} />
              </div>
            ))
          }
        </Panel>

        <Panel className="guardrail-panel">
          <div className="guardrail-panel__icon"><Icon name="shield" size={24} /></div>
          <span className="eyebrow">Investor safety boundary</span>
          <h2>Presentation, not execution</h2>
          <p>
            M1-A exposes read-only market evidence and local preferences only. No order, margin,
            broker account or private portfolio action is available in this interface.
          </p>
          <div className="guardrail-list">
            <span>✓ No BUY / SELL controls</span>
            <span>✓ No provider call from browser</span>
            <span>✓ No synthetic investor fallback</span>
          </div>
        </Panel>
      </div>
    </div>
  );
}

function WatchlistPage({ onNavigate }: { onNavigate: (path: string) => void }) {
  const [revision, setRevision] = useState(0);
  const watchlist = useResource("watchlist-" + revision, api.watchlist);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Instrument[]>([]);
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState<Error | null>(null);
  const [mutationError, setMutationError] = useState<Error | null>(null);
  const [saving, setSaving] = useState(false);

  const runSearch = async (event: FormEvent) => {
    event.preventDefault();
    setSearching(true);
    setSearchError(null);
    try {
      const response = await api.searchStocks(query);
      setResults(response.items);
    } catch (error) {
      setSearchError(error instanceof Error ? error : new Error("Search unavailable"));
      setResults([]);
    } finally {
      setSearching(false);
    }
  };

  const mutate = async (items: string[]) => {
    if (!watchlist.data) return;
    setSaving(true);
    setMutationError(null);
    try {
      await api.replaceWatchlist(watchlist.data.version, items);
      setRevision((value) => value + 1);
    } catch (error) {
      setMutationError(error instanceof Error ? error : new Error("Watchlist update failed"));
    } finally {
      setSaving(false);
    }
  };

  const addInstrument = (instrument: Instrument) => {
    if (!watchlist.data || watchlist.data.items.includes(instrument.instrument_id)) return;
    void mutate([...watchlist.data.items, instrument.instrument_id]);
  };

  const removeInstrument = (instrumentId: string) => {
    if (!watchlist.data) return;
    void mutate(watchlist.data.items.filter((item) => item !== instrumentId));
  };

  return (
    <div className="page">
      <SectionHeading
        eyebrow="Local preference"
        title="Watchlist"
        description="Single-user localhost preference only. Items are not holdings, positions or broker state."
        action={<RefreshButton onClick={() => setRevision((value) => value + 1)} disabled={watchlist.loading || saving} />}
      />

      {watchlist.error ? <ErrorNotice error={watchlist.error} /> : null}
      {mutationError ? (
        <div className="notice notice--warning">
          <div>
            <strong>Watchlist update not applied</strong>
            <p>{mutationError.message}. Refresh before retrying if the version changed.</p>
          </div>
          <StateBadge state="UNKNOWN" />
        </div>
      ) : null}

      <div className="watchlist-layout">
        <Panel className="watchlist-panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">Saved instruments</span>
              <h2>{watchlist.data ? watchlist.data.items.length + " / 100" : "Watchlist"}</h2>
            </div>
            {watchlist.data ? <span className="version-chip">v{watchlist.data.version}</span> : null}
          </div>

          {watchlist.loading ? <Skeleton lines={6} /> :
            watchlist.data && watchlist.data.items.length > 0 ? (
              <div className="watchlist-items">
                {watchlist.data.items.map((instrumentId) => (
                  <div className="watchlist-item" key={instrumentId}>
                    <div className="watchlist-item__main">
                      <span className="symbol-avatar">{instrumentId.slice(0, 2).toUpperCase()}</span>
                      <span>
                        <strong>{instrumentId}</strong>
                        <small>Verified instrument ID · not assumed to be a market symbol</small>
                      </span>
                    </div>
                    <button
                      type="button"
                      className="icon-button"
                      aria-label={"Remove " + instrumentId}
                      onClick={() => removeInstrument(instrumentId)}
                      disabled={saving}
                    >
                      <Icon name="close" />
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                icon="watchlist"
                title="Watchlist is empty"
                body="Search the verified instrument universe and add an instrument. FOX2 will not insert example tickers automatically."
              />
            )
          }

          {watchlist.data ? (
            <div className="panel-footer-note">Updated {formatDate(watchlist.data.updated_at)}</div>
          ) : null}
        </Panel>

        <Panel>
          <div className="panel-heading">
            <div>
              <span className="eyebrow">Verified universe</span>
              <h2>Find a stock</h2>
            </div>
            <Icon name="search" />
          </div>

          <form className="search-box" onSubmit={runSearch}>
            <Icon name="search" />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Symbol or instrument"
              aria-label="Search verified stocks"
            />
            <button className="button button--primary" type="submit" disabled={searching}>
              {searching ? "Searching…" : "Search"}
            </button>
          </form>

          {searchError ? <ErrorNotice error={searchError} /> : null}

          <div className="search-results">
            {results.map((instrument) => {
              const added = watchlist.data?.items.includes(instrument.instrument_id) ?? false;
              return (
                <div className="search-result" key={instrument.instrument_id}>
                  <button
                    type="button"
                    className="search-result__main"
                    onClick={() => onNavigate("/stocks/" + encodeURIComponent(instrument.symbol))}
                  >
                    <span className="symbol-avatar">{instrument.symbol.slice(0, 2)}</span>
                    <span>
                      <strong>{instrument.symbol}</strong>
                      <small>{instrument.venue} · {instrument.instrument_type}</small>
                    </span>
                  </button>
                  <button
                    type="button"
                    className={"button " + (added ? "button--quiet" : "button--ghost")}
                    disabled={added || saving || !watchlist.data || watchlist.data.items.length >= 100}
                    onClick={() => addInstrument(instrument)}
                  >
                    {added ? "Added" : <><Icon name="plus" size={15} /> Add</>}
                  </button>
                </div>
              );
            })}
          </div>

          {!searching && results.length === 0 && query ? (
            <p className="inline-help">No verified result is currently displayed. Unknown instruments are not silently added.</p>
          ) : null}
        </Panel>
      </div>
    </div>
  );
}

function BarsChart({ bars }: { bars: BarsPayload }) {
  if (bars.items.length < 2) {
    return (
      <EmptyState
        icon="stock"
        title="History unavailable"
        body="There are not enough accepted daily bars to draw a price path."
      />
    );
  }

  const closes = bars.items.map((item) => item.close);
  const min = Math.min(...closes);
  const max = Math.max(...closes);
  const spread = max - min || 1;
  const points = bars.items
    .map((item, index) => {
      const x = (index / (bars.items.length - 1)) * 100;
      const y = 88 - ((item.close - min) / spread) * 72;
      return x.toFixed(2) + "," + y.toFixed(2);
    })
    .join(" ");

  return (
    <div className="chart-wrap">
      <svg className="price-chart" viewBox="0 0 100 100" preserveAspectRatio="none" role="img" aria-label="Accepted historical close path">
        <defs>
          <linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="currentColor" stopOpacity="0.22" />
            <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
          </linearGradient>
        </defs>
        <polygon points={"0,100 " + points + " 100,100"} fill="url(#chartFill)" stroke="none" />
        <polyline points={points} fill="none" vectorEffect="non-scaling-stroke" />
      </svg>
      <div className="chart-caption">
        <span>{bars.timeframe} · RAW basis</span>
        <span>{bars.items.length} accepted bars</span>
        <span className={bars.gaps.length > 0 ? "warning-text" : ""}>
          {bars.gaps.length > 0 ? bars.gaps.length + " explicit gap(s)" : "No reported gaps"}
        </span>
      </div>
    </div>
  );
}

function StockSearch({ onNavigate }: { onNavigate: (path: string) => void }) {
  const [symbol, setSymbol] = useState("");
  const submit = (event: FormEvent) => {
    event.preventDefault();
    const clean = symbol.trim().toUpperCase();
    if (clean) onNavigate("/stocks/" + encodeURIComponent(clean));
  };
  return (
    <Panel className="stock-search-card">
      <span className="eyebrow">Stock360</span>
      <h2>Open a verified stock</h2>
      <p>Enter a symbol. FOX2 will request the accepted localhost backend and will not invent a quote if the source is unavailable.</p>
      <form className="search-box" onSubmit={submit}>
        <Icon name="search" />
        <input value={symbol} onChange={(event) => setSymbol(event.target.value)} placeholder="e.g. verified symbol" aria-label="Stock symbol" />
        <button className="button button--primary" type="submit">Open</button>
      </form>
    </Panel>
  );
}

function Stock360Page({ symbol, onNavigate }: { symbol?: string; onNavigate: (path: string) => void }) {
  const [revision, setRevision] = useState(0);
  const stock = useResource("stock-" + (symbol || "none") + "-" + revision, () => symbol ? api.stock(symbol) : Promise.resolve(null as unknown as StockResult));
  const bars = useResource("bars-" + (symbol || "none") + "-" + revision, () => symbol ? api.bars(symbol) : Promise.resolve(null as unknown as MarketDataEnvelope));

  if (!symbol) {
    return (
      <div className="page">
        <SectionHeading
          eyebrow="Evidence-led stock review"
          title="Stock360"
          description="Quote, history and provenance remain distinct. A history close is never presented as a current trade."
        />
        <StockSearch onNavigate={onNavigate} />
      </div>
    );
  }

  const observation = stock.data?.quote.data;
  const quote = observation?.payload?.kind === "quote" ? observation.payload : null;
  const barsPayload = bars.data?.data.payload?.kind === "bars" ? bars.data.data.payload : null;

  return (
    <div className="page">
      <SectionHeading
        eyebrow="Stock360 · read-only evidence"
        title={stock.data?.instrument.symbol || symbol.toUpperCase()}
        description={stock.data ? stock.data.instrument.venue + " · " + stock.data.instrument.instrument_type : "Loading verified instrument metadata"}
        action={<RefreshButton onClick={() => setRevision((value) => value + 1)} disabled={stock.loading || bars.loading} />}
      />

      {stock.error ? <ErrorNotice error={stock.error} /> : null}

      <div className="stock-hero">
        <Panel className="stock-price-card">
          {stock.loading ? <Skeleton lines={5} /> : (
            <>
              <div className="stock-price-card__top">
                <SourceBadge observation={observation} />
                <span className="muted">As of {formatDate(observation?.as_of)}</span>
              </div>
              <div className="stock-price-card__price">
                <span>{formatNumber(quote?.last_price)}</span>
                <small>{observation?.price_unit?.replaceAll("_", " ") || "UNKNOWN UNIT"}</small>
              </div>
              <div className="metric-grid metric-grid--four">
                <Metric label="Reference" value={formatNumber(quote?.reference_price)} />
                <Metric label="Ceiling" value={formatNumber(quote?.ceiling_price)} />
                <Metric label="Floor" value={formatNumber(quote?.floor_price)} />
                <Metric label="Volume" value={formatNumber(quote?.cumulative_volume, 0)} hint={observation?.volume_unit?.replaceAll("_", " ")} />
              </div>
            </>
          )}
        </Panel>

        <Panel className="provenance-card">
          <span className="eyebrow">Data provenance</span>
          <h2>What this view actually knows</h2>
          <div className="provenance-list">
            <div><span>Data mode</span><strong>{observation?.data_mode?.replaceAll("_", " ") || "Unknown"}</strong></div>
            <div><span>Freshness</span><StateBadge state={observation?.freshness_state} /></div>
            <div><span>Quality</span><strong>{observation?.quality || "Unknown"}</strong></div>
            <div><span>Price basis</span><strong>{observation?.price_basis?.replaceAll("_", " ") || "Unknown"}</strong></div>
            <div><span>Source</span><strong>{observation?.source_id || observation?.retrieval_channel?.replaceAll("_", " ") || "Unknown"}</strong></div>
            <div><span>Revision</span><strong>{observation?.revision ?? "Unknown"}</strong></div>
          </div>
        </Panel>
      </div>

      <Panel>
        <div className="panel-heading">
          <div>
            <span className="eyebrow">Price history</span>
            <h2>90-day accepted daily bars</h2>
          </div>
          {bars.data ? <SourceBadge observation={bars.data.data} /> : null}
        </div>

        {bars.loading ? <Skeleton lines={6} /> :
          bars.error ? <ErrorNotice error={bars.error} /> :
          barsPayload ? <BarsChart bars={barsPayload} /> :
          <EmptyState icon="stock" title="History unavailable" body="The backend did not return an accepted bars payload. No fallback chart is generated." />
        }
      </Panel>

      {barsPayload && barsPayload.gaps.length > 0 ? (
        <Panel className="gap-panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">Explicit data gaps</span>
              <h2>History continuity warnings</h2>
            </div>
            <StateBadge state="GAP_RECOVERING" />
          </div>
          {barsPayload.gaps.map((gap, index) => (
            <div className="gap-row" key={gap.from + "-" + gap.to + "-" + index}>
              <span>{formatDate(gap.from)} → {formatDate(gap.to)}</span>
              <strong>{gap.reason}</strong>
            </div>
          ))}
        </Panel>
      ) : null}

      <Panel className="disclaimer-panel">
        <Icon name="shield" />
        <div>
          <strong>No investment action is generated in the browser</strong>
          <p>Stock360 presents accepted evidence only. BUY/SELL, NAV, private account facts and synthetic scores are outside M1-A.</p>
        </div>
      </Panel>
    </div>
  );
}

function DataSourcesPage() {
  const [revision, setRevision] = useState(0);
  const health = useResource("health-detail-" + revision, api.health);
  const sources = useResource("source-detail-" + revision, api.sourceHealth);

  return (
    <div className="page">
      <SectionHeading
        eyebrow="Read-only diagnostics"
        title="Data Sources"
        description="Capability state without secrets, credentials or private entitlement details."
        action={<RefreshButton onClick={() => setRevision((value) => value + 1)} disabled={health.loading || sources.loading} />}
      />

      <div className="source-summary">
        <Panel>
          <span className="eyebrow">Process</span>
          <div className="summary-stat">
            <strong>{health.loading ? "Checking…" : health.data?.status || "Unavailable"}</strong>
            <StateBadge state={health.data?.status === "OK" ? "LIVE" : "UNAVAILABLE"} />
          </div>
          <p>{health.data?.provider_enabled ? "Provider mode enabled." : "Provider integration disabled; localhost remains usable with explicit unavailable states."}</p>
        </Panel>
        <Panel>
          <span className="eyebrow">Contract</span>
          <div className="summary-stat"><strong>{health.data?.contract_version || "Unknown"}</strong></div>
          <p>Diagnostics expose only the accepted market-data contract identity returned by FOX2 backend.</p>
        </Panel>
      </div>

      {health.error ? <ErrorNotice error={health.error} /> : null}
      {sources.error ? <ErrorNotice error={sources.error} /> : null}

      <div className="source-card-grid">
        {sources.loading ? (
          <><Panel><Skeleton lines={6} /></Panel><Panel><Skeleton lines={6} /></Panel><Panel><Skeleton lines={6} /></Panel></>
        ) : sources.data?.map((source: SourceHealth) => (
          <Panel className="source-detail-card" key={source.capability}>
            <div className="source-detail-card__head">
              <span className="source-icon"><Icon name="database" /></span>
              <div>
                <span className="eyebrow">Capability</span>
                <h2>{source.capability}</h2>
              </div>
              <StateBadge state={source.state} />
            </div>
            <div className="provenance-list">
              <div><span>Readiness</span><strong>{source.readiness}</strong></div>
              <div><span>Gap state</span><strong>{source.gap_state}</strong></div>
              <div><span>Rights state</span><strong>{source.rights_state}</strong></div>
              <div><span>Verified until</span><strong>{formatDate(source.verified_until)}</strong></div>
              <div><span>Reason</span><strong>{source.reason.replaceAll("_", " ")}</strong></div>
            </div>
          </Panel>
        ))}

        {!sources.loading && (!sources.data || sources.data.length === 0) ? (
          <Panel className="span-3">
            <EmptyState icon="database" title="No source diagnostics returned" body="FOX2 cannot infer provider readiness from an empty response." />
          </Panel>
        ) : null}
      </div>

      <div className="notice notice--info">
        <Icon name="shield" />
        <div>
          <strong>Secret-safe diagnostic boundary</strong>
          <p>This screen is read-only. It never shows API keys, provider credentials, account information or raw private entitlement payloads.</p>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const { pathname, navigate } = usePath();
  const route = parseRoute(pathname);

  return (
    <AppShell route={route} onNavigate={navigate}>
      {route.key === "overview" ? <OverviewPage onNavigate={navigate} /> : null}
      {route.key === "watchlist" ? <WatchlistPage onNavigate={navigate} /> : null}
      {route.key === "stock" ? <Stock360Page symbol={route.symbol} onNavigate={navigate} /> : null}
      {route.key === "sources" ? <DataSourcesPage /> : null}
    </AppShell>
  );
}
