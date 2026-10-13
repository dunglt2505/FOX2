# FOX2 — M1-P2-03 DSM Source Selection | Source & Design Lock

**Date:** 2026-10-14  
**WP:** `FOX2-M1-P2-03`  
**Status:** `SOURCE_DESIGN_LOCKED / OWNER_DEV_AUTHORIZED / STOP_AT_PUSHED_UNREVIEWED`  
**Owner instruction:** `triển khai FOX2-M1-P2-03`  
**Upstream accepted P2-02:** `f70f0237356c4f27afb0e6760b01870228ba3739`

## 1. Source authority

Use exactly the source present at the accepted P2-02 SHA unless a newer released source is explicitly proven material:

- Policy V1.8.5 RELEASED_EFFECTIVE
- Routing Index V1.2.6 EFFECTIVE_DERIVATIVE
- M1 Technical Spec v0.1
- P2 WP Plan v0.1
- BRD-06 v0.5 RELEASED_EFFECTIVE
- BRD-08 v0.5 RELEASED_EFFECTIVE
- Market Data Contract/schema v0.4
- Acceptance Matrix v0.4
- Accepted P2-01 frozen ports/DTO/validators
- Accepted P2-02 store implementation at `f70f0237356c4f27afb0e6760b01870228ba3739`

Frozen upstream interfaces include:

- `DSMSelectPort.select(capability, instrument_id, use_context) -> SelectionDecision`
- `StoreReadPort.get_observation(instrument_id, capability, at_or_before) -> ObservationOrUnavailable`
- `SelectionDecision(capability, selection_audit_id, observation)`
- `CapabilityContext` + `MarketValidator.validate_semantics`
- `SourceHealth` published health DTO

Do not modify frozen P2-01/P2-02 interfaces to make P2-03 easier.

## 2. Exact write scope

Allowed code:
- `backend/src/fox2/dsm/**`
- `tests/p2_03/**`

Allowed result:
- `reports/FOX2-M1-P2-03/report.md`
- `reports/FOX2-M1-P2-03/evidence_manifest.json`
- `reports/FOX2-M1-P2-03/evidence/**`

Everything else is read-only, including:
- `backend/src/fox2/contracts/**`
- `backend/src/fox2/ports/**`
- `backend/src/fox2/validation/**`
- `backend/src/fox2/store/**`
- `backend/pyproject.toml`
- provider/API/frontend/Bridge/governance/docs/.github canonical files.

No provider package, network client, scheduler, background refresher, websocket, REST call, broker/account path, secret handling or package install.

## 3. DSM behavioral lock

P2-03 is **offline M1-A source selection only**.

### 3.1 Per-use selection

Every call to `select(...)` must create a fresh sanitized `selection_audit_id` and reevaluate the current request. Do not cache a positive selection across calls.

DSM must distinguish typed `QUOTE`, `BARS`, `INDEX`. Never satisfy `QUOTE` from historical `BARS`, or otherwise cross capability.

For the selected local-store candidate, reevaluate at the current trusted UTC clock:

- requested capability and instrument identity;
- applicable rights and expiry;
- use context;
- provenance/data mode/retrieval channel;
- mapping state and units/basis;
- semantic validator result;
- freshness/freshness-policy evidence;
- calendar/session evidence where applicable;
- relevant gaps/completeness.

If any required fact is missing/blocked/expired/stale/ambiguous, return typed `Unavailable` with the safest existing reason. Do not fabricate a positive observation.

### 3.2 Rights

Minimum rights at selection time:

- `READ`: read
- `DISPLAY`: read + redisplay
- `ANALYSIS`: read + redisplay
- `RETAINED_USE`: read + retained_use

A local-store observation also remains subject to P2-02 retained-use protection. Expired/revoked/unknown rights must not silently fall back to another source or stale cache.

### 3.3 Freshness and capability evidence

Do not invent provider-specific stale thresholds.

Implement a DSM-owned injected offline capability policy/evidence object or equivalent immutable input. A positive selection requires explicit policy evidence for the requested capability. Missing freshness budget/mapping/calendar/gap evidence returns unavailable/unknown, not PASS.

`LIVE` / `PERIODIC_LIVE` cannot be positively selected in P2-03 unless transport/subscription evidence is explicitly supplied. In the normal P2-03 offline/provider-disabled configuration those facts are false, so such candidates are diagnostic-only/unavailable.

`PROVIDER_NATIVE_UNVERIFIED` remains diagnostic-only and must never be selected for `ANALYSIS`.

For `BARS`, relevant gaps, unknown calendar/session mapping, unknown basis/adjustment evidence or incomplete coverage block a positive selection where the semantic contract requires those facts.

No-trade versus outage must not be inferred solely from event age; use explicit injected session/calendar/gap evidence or return unknown/unavailable.

### 3.4 Provider-disabled boundary

Default runtime for this WP is `provider_enabled=false`.

When disabled:
- do not import/construct provider transports;
- no startup/manual refresh/retry/backfill/scheduler network path exists;
- tests must prove socket/DNS attempts are zero;
- no synthetic/test fixture may appear in INVESTOR selection;
- no automatic fallback to synthetic data.

If `provider_enabled=true` is passed before provider integration exists, return truthful NOT_INTEGRATED/UNAVAILABLE diagnostics and still do not construct network transport.

### 3.5 Diagnostics and audit

Keep canonical DTOs unchanged.

Provide DSM-owned immutable audit records via an injected audit sink/callback or equivalent request-local mechanism. Every selection attempt records at least:

- `selection_audit_id`
- requested capability/instrument/use_context
- selected source/record id when present
- accepted/rejected result
- sanitized reason code(s)
- evaluation time

No private data, credentials, raw provider payloads, or secret-like values.

Positive returned observations should carry the fresh selection audit identity/reason by immutable copy only; never mutate persisted store rows.

For source diagnostics, use the frozen `SourceHealth` contract truthfully. P2-03 offline diagnostics may only report `UNKNOWN/UNAVAILABLE` with `reason=NOT_INTEGRATED`; never claim READY/LIVE provider capability.

## 4. Acceptance subset

P2-03 may prove only offline/backend subcases for the existing IDs:

- `FOX2-06-T02` stale/disconnect state semantics
- `FOX2-06-T03` no-trade is not automatically outage
- `FOX2-06-T04` missing values remain missing, not zero
- `FOX2-06-T07` old local snapshot does not become LIVE
- `FOX2-06-T08` bars gap/revision issues block unsafe positive selection
- `FOX2-06-T09` entitlement expired/missing credentials => unavailable
- `FOX2-06-T15` source-selection diagnostics
- `FOX2-06-T16` no private/account/order/provider secret path
- `FOX2-06-T18` unavailable/semantic guards
- `FOX2-N1-T01` no observation => no invented timestamps
- `FOX2-N1-T02` LIVE with unknown rights/units/calendar rejected
- `FOX2-N1-T07` revoked retained-use blocks cache fallback
- `FOX2-N1-T09` no-trade age distinct from transport/session evidence

Canonical/provider/UI scenarios remain `NOT_RUN/PARTIAL`.

## 5. Mandatory tests

At minimum cover:

1. typed capability mismatch never falls back across capability;
2. no observation => typed unavailable;
3. provider disabled => zero provider construction and zero socket/DNS attempts;
4. provider-enabled-without-integration => NOT_INTEGRATED, still zero network;
5. INVESTOR test fixture/synthetic candidate rejected;
6. READ/DISPLAY/ANALYSIS/RETAINED_USE rights matrix;
7. rights expiry checked on every call; a previously positive selection becomes blocked after clock advance;
8. store revocation blocks later selection without fallback;
9. missing/unknown mapping/unit/basis blocks unsafe positive selection;
10. LIVE/PERIODIC_LIVE without transport/subscription evidence rejected;
11. stale quote/index under explicit budget rejected;
12. historical BARS never satisfy QUOTE;
13. BARS gap/calendar/coverage/adjustment evidence negatives;
14. no-trade explicit session evidence is not treated as outage solely by age;
15. PROVIDER_NATIVE_UNVERIFIED diagnostic-only; ANALYSIS rejected;
16. fresh selection audit ID each call;
17. audit sink contains only sanitized decision metadata;
18. returned positive observation gets fresh selection audit identity without mutating persisted object;
19. SourceHealth stays UNKNOWN/UNAVAILABLE, never fake READY;
20. P2-02 regression subset proving store unchanged;
21. import/dependency boundary: DSM may depend on contracts/ports/validation, but provider/api/frontend/Bridge must not be imported;
22. secret scan and changed-path allowlist.

## 6. Writer, branch and stop boundary

Task branch: `work/FOX2-M1-P2-03-dsm-codex`  
Preferred worktree: `C:\Projects\FOX2-worktrees\FOX2-M1-P2-03-CODEX`  
Single writer: CODEX via FOX2 Bridge.

Immediate execution may proceed under the Owner's explicit task authorization after the Bridge verifies exact branch/base/worktree and single-use dispatch.

Final boundary:
`PUSHED_UNREVIEWED`

No PR, merge, main, deployment, DNSE Production, broker write or LIVE.

## 7. Gate snapshot

```text
P2_02_OFFLINE_STORE=ACCEPTED
P2_03_OWNER_DEV_AUTHORIZATION=YES
P2_03_SOURCE_DESIGN=LOCKED
P2_03_CODE_ALLOWED=YES_TASK_ONLY
P2_03_GIT_CODE_PUSH=YES_OWN_TASK_BRANCH_ONLY
PR_CREATE=NO
MERGE_ALLOWED=NO
DNSE_PRODUCTION=NO
BROKER_WRITE=NO
LIVE=NO
```
