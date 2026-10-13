# FOX2 — CODEX EXECUTION HANDOFF — M1-P2-03 DSM SOURCE SELECTION

**Date:** 2026-10-14  
**WP:** `FOX2-M1-P2-03`  
**Status:** `EXECUTABLE / DEV_AUTHORIZED_TASK_BOUND / STOP_AT_PUSHED_UNREVIEWED`  
**Owner instruction:** `triển khai FOX2-M1-P2-03`

## 0. Assignment

- **Role:** CODEX implementation agent through FOX2 Bridge
- **Engine/Model:** current configured OpenAI Codex CLI model; GPT-6.1 Sol was observed on the immediately preceding Bridge canary
- **Thinking:** use current configured effort; Medium is preferred for source-selection semantics if the runtime exposes a selectable setting. Do not fabricate the actual level; report it.
- **Scope:** whole P2-03 DSM offline source-selection WP only
- **Writer:** one CODEX writer, one branch, one worktree
- **Stop boundary:** `PUSHED_UNREVIEWED`

This task is explicitly authorized by Owner. No additional Owner confirmation is required for internal P2-03 implementation/test checkpoints that remain inside this immutable scope.

## 1. Immutable base and source lock

Repository: `dunglt2505/FOX2`

Task branch: `work/FOX2-M1-P2-03-dsm-codex`

Accepted upstream P2-02:
`f70f0237356c4f27afb0e6760b01870228ba3739`

Normative P2-03 source/design lock:
- commit `97b68bd67ef84675dabcfdd656f95ffb7d78511e`
- path `docs/agent_handoff/M1/P2-03/FOX2_M1_P2_03_DSM_SOURCE_DESIGN_LOCK_20261014.md`
- blob `22745ab75b804697db5cb4907ba77c266814f42b`

Read that document completely before editing.

Preserve accepted P2-01 and P2-02 code unchanged.

## 2. Exact write allowlist

Implementation:
- `backend/src/fox2/dsm/**`
- `tests/p2_03/**`

Result:
- `reports/FOX2-M1-P2-03/report.md`
- `reports/FOX2-M1-P2-03/evidence_manifest.json`
- `reports/FOX2-M1-P2-03/evidence/**`

Everything else is read-only.

If implementation genuinely requires changing a frozen port, DTO, validator, store, pyproject, API, provider, frontend, Bridge, governance or canonical docs, STOP with `BLOCKED_INTERFACE_CONFLICT` or `BLOCKED_SCOPE`.

## 3. Preferred implementation shape

Use small deterministic modules under `fox2.dsm`. Exact filenames/classes are implementation-owned, but keep the public implementation centered on the frozen `DSMSelectPort`.

Recommended components:

- `DataSourceManager`: implements `select(capability, instrument_id, use_context)`
- immutable `CapabilityPolicy` / evaluation evidence input: current freshness budget and capability/session/gap/coverage facts supplied locally, never provider-fabricated
- immutable `SelectionAuditRecord`
- injected `audit_sink` callback; default safe no-op
- injected UTC clock and audit-id factory for deterministic tests
- `source_health(capability)` or equivalent truthful frozen-`SourceHealth` diagnostic

Do not add provider interfaces/transports in this WP.

## 4. Selection algorithm lock

For every call:

1. validate typed capability/instrument/use-context inputs;
2. allocate a fresh sanitized selection audit id;
3. read only the requested capability from `StoreReadPort`; no cross-capability fallback;
4. if store returns `Unavailable`, preserve safe typed unavailable semantics and emit audit;
5. if an observation exists, reject investor fixture/synthetic leakage;
6. reevaluate rights and expiry for the exact use context at the current clock;
7. build/use `CapabilityContext` from injected current evidence;
8. run semantic validation;
9. apply explicit freshness policy and gap/calendar/coverage/mapping/basis evidence;
10. select only if all required facts are positively evidenced;
11. return an immutable copy carrying the new `selection_audit_id` and sanitized `selection_reason`;
12. emit one immutable audit record; never mutate persisted store rows or cache a positive decision.

Safe unavailable mapping should use existing `Unavailable` reasons. Suggested mapping:
- explicit rights/expiry/revocation → `RIGHTS_BLOCKED`
- store unsafe → `UNSAFE_STORE`
- malformed/semantic-invalid positive candidate → `INVALID_CANDIDATE`
- absent item → `NOT_FOUND`
- missing/ambiguous freshness/mapping/calendar/gap/provider evidence → `UNKNOWN`

Do not invent a new canonical unavailable enum in this WP.

## 5. Rights/use-context matrix

At selection time:
- `READ` => require `rights.read=VERIFIED`
- `DISPLAY` => read + redisplay
- `ANALYSIS` => read + redisplay
- `RETAINED_USE` => read + retained_use

Always require valid evidence ref and unexpired `verified_until` when the semantic contract requires rights evidence.

A local store read is additionally subject to P2-02 retained-use protection.

No fallback after rights block/expiry.

## 6. Freshness / mapping / gap rules

Do not invent provider stale thresholds. Use an injected explicit policy/evidence object.

Positive current selection requires the evidence relevant to its state/capability. Missing policy/evidence => `UNKNOWN`.

- `LIVE/PERIODIC_LIVE`: require transport + subscription evidence, explicit positive freshness budget and current `as_of`; offline default must not pass.
- `PROVIDER_NATIVE_UNVERIFIED`: diagnostic-only; `ANALYSIS` forbidden.
- BARS: no unsafe selection with relevant gaps, unknown session/calendar mapping, missing required coverage, or unresolved adjusted-basis evidence.
- no-trade must be represented through explicit session/calendar/gap facts; age alone is not outage.
- history/BARS never impersonates QUOTE.
- stale/blocked/unavailable states must never be relabeled LIVE.

## 7. Provider-disabled boundary

Default `provider_enabled=false`.

P2-03 code must have zero provider-network construction path. No refresh/retry/scheduler/backfill.

If configured `provider_enabled=true` before provider integration exists:
- report truthful NOT_INTEGRATED/UNKNOWN/UNAVAILABLE diagnostics;
- do not import or instantiate provider transport;
- do not attempt network.

Fixtures are test-only and cannot become an INVESTOR fallback.

## 8. Acceptance/test set

Run deterministic offline tests covering the source-lock mandatory list and map evidence to these existing IDs only:

`FOX2-06-T02/T03/T04/T07/T08/T09/T15/T16/T18`
`FOX2-N1-T01/T02/T07/T09`

Do not mark the canonical/provider/UI scenario PASS unless fully executed. P2-03 reports offline subcase PASS and canonical `PARTIAL/NOT_RUN`.

Required commands should include at least:

- `python -B -m pytest tests/p2_03 -p no:cacheprovider -q --tb=short`
- relevant read-only P2-02 regression subset
- relevant P2-01 validator/port regression subset if needed
- syntax/import check
- `git diff --check`
- changed-path allowlist check
- obvious-secret scan
- explicit socket/DNS zero-attempt proof

No package installation.

## 9. Result Contract

Write only under `reports/FOX2-M1-P2-03/**`.

Required:
- `report.md`
- `evidence_manifest.json`
- hashed evidence files under `evidence/**` as needed

Report:
- exact immutable source/base/branch/worktree
- actual model/thinking/quota if exposed; otherwise `NOT_EXPOSED`
- changed paths
- exact tests/results
- rights/freshness/capability/gap/fixture/no-network evidence
- acceptance subcases versus canonical remaining obligations
- NOT_RUN provider/API/frontend/LIVE
- final commit and remote readback SHA

## 10. Git and final boundary

Preferred worktree:
`C:\Projects\FOX2-worktrees\FOX2-M1-P2-03-CODEX`

Before mutation, verify:
- branch HEAD equals this executable handoff commit;
- exact worktree ownership;
- no preexisting unreviewed WIP;
- no concurrent writer.

Commit/push only:
`work/FOX2-M1-P2-03-dsm-codex`

No PR, main merge, deployment, DNSE Production, broker write or LIVE.

Final execution state:
`PUSHED_UNREVIEWED`

CHAT will independently read back the exact remote SHA before acceptance.
