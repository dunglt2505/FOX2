# FOX2 SQLite store

`SQLiteStore` implements the accepted `StoreReadPort`, `StoreWritePort` and
`PreferenceRepositoryPort` without changing them. It adds no application wiring.
Python stdlib SQLite is the only persistence dependency.

Instantiate with an explicit absolute root outside every Git worktree. Its final
directory name must start with `fox2`. Legacy `Data/Fox` ancestry, symlinks and
Windows junctions are refused. Databases, rollback journals and test DBs stay out
of Git. A fresh store records its `INVESTOR` or `ISOLATED_TEST` profile permanently;
an isolated fixture store cannot be reopened as an investor store.

Supply a trusted local `instrument_registry(id) -> bool` and, for promotion, a
trusted `evidence(observation) -> PromotionEvidence | None`. The latter is called
per independently decomposed bar, before acquiring a write lock. Its capability
context must use the injected clock's current UTC evaluation time and
`RETAINED_USE`. A lifecycle claim or provider revision label in the observation
does not substitute for this adapter's verification. No provider adapter is part
of this package. With no evidence adapter, valid but unproved observations are
stored as quarantine and never become current.

The receipt argument is a trusted local `IngestAudit`. Receipts up to five seconds
before local verification are accepted; older or future receipts are refused.
Persisted `received_at` comes from that receipt and `first_available_at` comes
from the store clock at verification. New caller-supplied availability must be
absent or equal to verification time; duplicates may retain their known original
availability. Clock regression is refused. The original incoming DTO as
canonical JSON, source IDs, source revision label, immutable
market payload and evidence reference are retained separately from store IDs.
The frozen ingest port supplies a raw hash, not raw wire bytes; this package
does not claim to store wire bytes that the port never receives.

Verified ordering is an adapter-provided nonnegative integer, never a parsed
provider label. Same logical bar/event correction requires the current store
record as verified predecessor and a strictly increasing verified order.
Final-to-provisional regression is retained without promotion. A chronologically
newer daily bar in the same series can advance on verified lifecycle/calendar
evidence with nondecreasing source order (including a single batched receipt).
Different quote events require both chronologically newer event time and
increasing verified order. Same-time ticks remain distinct immutable records;
they do not use receipt order as precedence. Unprovable candidates leave current
unchanged and receive an audit/gap reason.

For a multi-bar receipt, the frozen singular `CommitResult.record_id/revision`
describe the first input item; `promoted` says whether any item advanced current.
Every item is linked in `receipt_records`, with its own immutable record,
revision, promotion audit and logical identity. The whole batch commits or rolls
back together. Canonical market fingerprints exclude receipt/local revision,
selection metadata and rights; a changed rights assertion alone is not a market
revision and cannot extend existing registry authorization.

Reads use immutable promotion history for the requested UTC availability cutoff.
Quarantine and out-of-order revisions are never chosen merely because they
arrived later. Current retained-use rights are checked in the same read snapshot,
independently of the historical cutoff. Expiry or explicit trusted
`revoke_rights(series_key, evidence_ref)` blocks reads. Polling cannot re-grant
rights. Multiple eligible source/basis series return `Unavailable(UNKNOWN)`;
an unauthorized series returns `Unavailable(RIGHTS_BLOCKED)` without falling
back to a different source. P2-03 will own source/use-context selection.

Each operation owns a separate connection. Writes use `BEGIN IMMEDIATE`, foreign
keys, `synchronous=FULL`, DELETE rollback journal and a bounded busy timeout
(default 250 ms; permitted 0–5000 ms). Busy/disk failures return existing sanitized
port outcomes; no retry loop or background thread is created. Readers use a
transaction snapshot. SQLite schema metadata and checksums are verified at
initialization; unknown, altered, future-version or non-FOX2 stores are refused,
never repaired. Version 1 is a transactional initial migration; future migrations
must extend the ordered checksummed chain rather than change released version 1.

`fault_hook(stage)` is an explicit testing dependency for transaction/crash tests,
not a production scheduler or network callback. Keep all supplied callbacks
local, synchronous and trusted. `integrity()` exposes SQLite integrity, FK,
durability and migration readback. `close()` is a no-op because operations close
their connections immediately. Watchlist CAS uses the same bounded atomic
transaction and trusted instrument registry, with restart persistence.
