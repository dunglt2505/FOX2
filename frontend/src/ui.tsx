import type { ReactNode } from "react";
import type { MarketObservation } from "./types";

export type IconName =
  | "overview"
  | "watchlist"
  | "stock"
  | "sources"
  | "search"
  | "refresh"
  | "shield"
  | "database"
  | "chevron"
  | "plus"
  | "close";

export function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  const paths: Record<IconName, ReactNode> = {
    overview: <><path d="M4 4h6v6H4z"/><path d="M14 4h6v10h-6z"/><path d="M4 14h6v6H4z"/><path d="M14 18h6v2h-6z"/></>,
    watchlist: <><path d="M6 4h12"/><path d="M6 10h12"/><path d="M6 16h8"/><path d="M4 4h.01"/><path d="M4 10h.01"/><path d="M4 16h.01"/></>,
    stock: <><path d="M4 18V6"/><path d="M9 18V10"/><path d="M14 18V4"/><path d="M19 18v-7"/></>,
    sources: <><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></>,
    search: <><circle cx="11" cy="11" r="6"/><path d="m16 16 4 4"/></>,
    refresh: <><path d="M20 7v5h-5"/><path d="M4 17v-5h5"/><path d="M6.1 8a7 7 0 0 1 11.4-2L20 8"/><path d="M17.9 16a7 7 0 0 1-11.4 2L4 16"/></>,
    shield: <><path d="M12 3 5 6v5c0 4.5 2.7 7.8 7 10 4.3-2.2 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/></>,
    database: <><ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v7c0 1.7 3.1 3 7 3s7-1.3 7-3V5"/><path d="M5 12v7c0 1.7 3.1 3 7 3s7-1.3 7-3v-7"/></>,
    chevron: <path d="m9 6 6 6-6 6"/>,
    plus: <><path d="M12 5v14"/><path d="M5 12h14"/></>,
    close: <><path d="m7 7 10 10"/><path d="M17 7 7 17"/></>
  };

  return (
    <svg
      aria-hidden="true"
      className="icon"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {paths[name]}
    </svg>
  );
}

export function Panel({
  children,
  className = ""
}: {
  children: ReactNode;
  className?: string;
}) {
  return <section className={"panel " + className}>{children}</section>;
}

export function StateBadge({ state }: { state: string | null | undefined }) {
  const label = state || "UNKNOWN";
  const normalized = label.toLowerCase().replaceAll("_", "-");
  return <span className={"state-badge state-" + normalized}>{label.replaceAll("_", " ")}</span>;
}

export function SourceBadge({ observation }: { observation: MarketObservation | null | undefined }) {
  if (!observation) return <StateBadge state="UNAVAILABLE" />;
  return (
    <span className="source-badge">
      <span className="source-badge__dot" />
      <span>{observation.freshness_state.replaceAll("_", " ")}</span>
      <span className="source-badge__divider">·</span>
      <span>{observation.retrieval_channel.replaceAll("_", " ")}</span>
    </span>
  );
}

export function Metric({
  label,
  value,
  hint,
  strong = false
}: {
  label: string;
  value: ReactNode;
  hint?: ReactNode;
  strong?: boolean;
}) {
  return (
    <div className={"metric " + (strong ? "metric--strong" : "")}>
      <span className="metric__label">{label}</span>
      <span className="metric__value">{value}</span>
      {hint ? <span className="metric__hint">{hint}</span> : null}
    </div>
  );
}

export function EmptyState({
  title,
  body,
  icon = "shield"
}: {
  title: string;
  body: string;
  icon?: IconName;
}) {
  return (
    <div className="empty-state">
      <div className="empty-state__icon"><Icon name={icon} size={22} /></div>
      <strong>{title}</strong>
      <p>{body}</p>
    </div>
  );
}

export function Skeleton({ lines = 3 }: { lines?: number }) {
  return (
    <div className="skeleton" aria-label="Loading">
      {Array.from({ length: lines }, (_, index) => (
        <span key={index} style={{ width: (92 - index * 11) + "%" }} />
      ))}
    </div>
  );
}

export function SectionHeading({
  eyebrow,
  title,
  description,
  action
}: {
  eyebrow: string;
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <header className="section-heading">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        {description ? <p>{description}</p> : null}
      </div>
      {action ? <div className="section-heading__action">{action}</div> : null}
    </header>
  );
}

export function RefreshButton({
  onClick,
  disabled = false
}: {
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button className="button button--ghost" onClick={onClick} disabled={disabled} type="button">
      <Icon name="refresh" />
      Refresh
    </button>
  );
}

export function formatNumber(value: number | null | undefined, maximumFractionDigits = 2) {
  if (value === null || value === undefined || Number.isNaN(value)) return "Unavailable";
  return new Intl.NumberFormat("en-US", { maximumFractionDigits }).format(value);
}

export function formatDate(value: string | null | undefined) {
  if (!value) return "Unknown";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return "Unknown";
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(parsed);
}
