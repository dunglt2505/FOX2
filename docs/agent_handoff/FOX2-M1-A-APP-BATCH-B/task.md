# FOX2-M1-A-APP-BATCH-B — Whole-WP Task

**Status:** CODE_FIRST_RESUME_APPROVED / SOURCE_READY_FOR_FRESH_APP_PREEXEC / CODING_NOT_YET_ADMITTED  
**Project phase:** M1-A second execution phase  
**Governance:** Project Dictionary v1.2 -> Policy V1.8.9 -> Routing Index V1.3.0  
**Protocol:** PreExec Evidence v1.1 + Receipt Schema v1 + CHAT Preflight Intake v1.1 + Dispatch Schema v3 + Git-first Protocol v12  
**Final Agent assignment for integration/test remainder:** PENDING shared PreExec Intake; CHAT visual slicing is Owner-authorized directly  
**Execution path:** MANUAL_LOCAL candidate (must prove an actual independent DEV admission route before Agent execution)  
**Delivery owner:** AGENT candidate

## Source binding

- Accepted application base: `3db6298e4286022e5820eb7b712c436cbade6a62`
- Accepted APP-BATCH-A result: same SHA above; 364 PASS / 3 superseded stage-only deselections.
- Current Master Plan: `f109d16f78da4a412cc30b512f152f79616b872c:docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md`
- Project Dictionary v1 source set: `544cd7003972e6a29ff25de1062231c3769affbf`
- Canonical Dictionary identity source: `28866ee6a61bde3fc3837ebd999c7b470afc7486:docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`
- Current semantic sources:
  - BRD-08 v0.5 — localhost investor dashboard/presentation;
  - M1 Technical Spec v0.1;
  - Market Data Contract/schema v0.4;
  - M1 Acceptance Matrix v0.4;
  - M1 Technical Spec Registry Binding v1.
- Backend API shape is frozen at accepted APP-BATCH-A unless a material integration defect is proven. If frontend cannot correctly implement against it, STOP and return the exact blocker rather than editing backend opportunistically.

## CHAT UI-slicing authorization — 2026-10-14

Owner explicitly authorized CHAT to implement the visual/UI slicing portion of this existing whole-WP.

Bound scope for CHAT:
- `frontend/**` only;
- Dark/White theme presentation with an explicit user toggle and local presentation-only preference persistence;
- information architecture, React component hierarchy, HTML/CSS structure, responsive 1440/1024/390 behavior, loading/empty/unavailable/stale/gap visual states;
- source/provenance badges and read-only navigation/presentation;
- no backend/provider/domain semantic changes;
- no claim that build/integration/acceptance has passed until actually executed.

The remaining API wiring hardening, automated tests, large refactor and integration certification may be routed to an eligible coding Agent after project-wide PreExec readiness.

This is not a new WP and does not authorize main/merge/deploy/provider/broker/LIVE.

## Owner priority pause — Bridge first

Owner has frozen further APP-BATCH-B execution at dual-theme source head:
`1b1a7d23c5a0a2c99afd060f5b793f162c8f6ed2`.

Do not continue frontend build/test/integration work until `BRIDGE-DESKTOP-BATCH-B` reaches `INTERNAL_FOX2_BRIDGE_READY`.

When resumed, preserve the CHAT-approved Dark/White UI and continue with build/typecheck/API integration/tests/runtime acceptance rather than redesigning the presentation.


## Whole-WP objective

Absorb historical P3 + P4 into one implementation/acceptance batch and produce the first **runnable localhost M1-A product**.

Deliver together:

1. React + TypeScript + Vite frontend under `frontend/**`;
2. routes/screens:
   - `/overview`;
   - `/watchlist`;
   - `/stocks/:symbol`;
   - `/settings/data-sources`;
3. browser communicates only with the FOX2 backend;
4. truthful source/data state, as-of/coverage/freshness/gap/unavailable display;
5. no fake zero, price, trend, score, BUY/SELL, NAV or investor synthetic fallback;
6. watchlist UX over the accepted local preference/CAS API;
7. responsive review targets: 1440 / 1024 / 390;
8. text + visual status communication; unknown units/status explicitly labeled;
9. localhost startup/navigation/refresh/security behavior;
10. frontend + backend integrated offline acceptance evidence;
11. one final M1-A offline acceptance package.

## Writable scope

Allowed code:
- `frontend/**`
- `tests/app_batch_b/**`

Allowed reports:
- `reports/FOX2-M1-A-APP-BATCH-B/**`

Everything else READ-ONLY, including:
- `backend/**`;
- accepted APP-BATCH-A tests/evidence;
- contracts/store/DSM/provider code;
- governance/BRD/Technical/Data Contract;
- `agent_bridge/**`.

If a frozen API/backend defect is material, STOP with reproducible evidence. Do not silently expand scope.

## Required product behavior

- UI never calls DNSE/provider endpoints or local DB directly.
- Provider-disabled runtime remains fully usable with explicit unavailable states.
- Manual refresh must not trigger provider backfill/network.
- History close must not masquerade as current quote.
- `UNKNOWN != 0`; unavailable values are not charted/fabricated.
- Watchlist is local preference only, never holdings/broker state.
- No account/order/cash/margin/LIVE UI.
- Data Sources diagnostics are read-only and secret-safe.
- Future unavailable domains may render explanatory unavailable states only.
- No provider/private secret in frontend bundle, source map, logs or error text.

## Required acceptance

At minimum:

- `NODE_NPM_VITE_CAPABILITY=PASS`
- `FRONTEND_BUILD=PASS`
- `FRONTEND_TESTS=PASS`
- `BACKEND_ACCEPTED_API_COMPATIBILITY=PASS`
- `OVERVIEW_UI=PASS`
- `WATCHLIST_UI_CAS=PASS`
- `STOCK360_UI=PASS`
- `DATA_SOURCE_DIAGNOSTICS_UI=PASS`
- `SOURCE_STATE_TRUTHFULNESS=PASS`
- `NO_SYNTHETIC_INVESTOR_FALLBACK=PASS`
- `NO_PROVIDER_DIRECT_BROWSER_CALL=PASS`
- `RESPONSIVE_1440_1024_390=PASS`
- `LOCALHOST_STARTUP_RESTART_NAVIGATION=PASS`
- `LOOPBACK_SECURITY=PASS`
- `M1_OFFLINE_ACCEPTANCE_MAPPING=PASS`
- `CHANGED_PATH_ALLOWLIST=PASS`
- `SECRET_SCAN=PASS`
- `GIT_DIFF_CHECK=PASS`

Map evidence to BRD-08 / Acceptance Matrix IDs without redefining their semantics.

## Material pre-execution gates

Before executable Dispatch v3:

1. exact branch/worktree ownership = PASS;
2. Node + npm + package-manager/Vite-capable toolchain = PASS;
3. selected Agent CLI + required FULL_ACCESS capability = PASS;
4. current Agent execution capacity must be demonstrably usable or classified non-material under Policy; no invented quota state;
5. no competing writer on `frontend/**`.

Until those are evidenced:
`CODE_ALLOWED_FOR_EXECUTION=HOLD`.

## Routing candidates — not final assignment

- COPILOT CLI / NATIVE_AUTO / Balance / FULL_ACCESS:
  preferred cost route for clear React/TS/Vite implementation **if current execution capacity is demonstrated**.
- CODEX CLI / PINNED / gpt-6.1-sol / Medium / FULL_ACCESS:
  fallback/alternate if Copilot cannot execute or task debugging becomes materially complex.
- CHAT:
  requirements/source binding/routing/acceptance only after this task source is published.
- WORK:
  not needed for implementation; optional only at final M1-A acceptance if independent audit materially improves confidence.

No Agent is assigned by this task file while R3/R5 remain unresolved.

## Git authority after executable dispatch

Candidate delivery is `delivery_owner=AGENT`, exact non-main branch only.

No PR/main/merge/deploy/provider/broker/LIVE authority.

## STOP

Stop for:
- source/base/branch/worktree mismatch;
- material Node/npm/Vite capability absent;
- actual Agent capacity/auth failure;
- overlapping frontend writer;
- backend change required;
- required test/security failure;
- secret/private/provider exposure;
- out-of-scope write;
- push/readback failure.

## Delivery

Expected after execution:
- `reports/FOX2-M1-A-APP-BATCH-B/report.md`
- `reports/FOX2-M1-A-APP-BATCH-B/evidence_manifest.json`
- material evidence under `reports/FOX2-M1-A-APP-BATCH-B/evidence/**`

Final milestone target:
`FOX2_M1_A_RUNNABLE_LOCALHOST_OFFLINE_ACCEPTED`


---

## Owner-authorized resumption — 2026-10-19: CODE-FIRST offline APP-BATCH-B

**Decision status:** Owner-approved APP-BATCH-B priority reversal and scoped coding/integration authorization on this existing Whole-WP. **This section supersedes only the earlier `Owner priority pause — Bridge first` and corresponding status/scheduling text above.** Preserve earlier text as historical; it must not be used as a current block for APP offline readiness or product coding once DEV admission is valid.

**Binding:**
- Owner CODE-FIRST/CHAT-FIRST directive: `7ac3cc986aa7a8b3e8e2365655edc1a9f25d818a:docs/governance/releases/FOX2_CODE_FIRST_CHAT_FIRST_OWNER_DIRECTIVE_AND_ROUTING_20261019.md`.
- Updated Master Plan candidate: `5cdcd21503dd70da1e57d863660757b8c69b3466:docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md`, Owner-approved 2026-10-19 priority amendment; its release-synchronization/effectivity status is separate.
- Current APP branch/source before this update: `fc8aba202e15bddfcc5156b2c1bb36ed222329eb`. The immutable task SOURCE_HEAD for subsequent PreExec becomes the exact new publication commit containing **this** task.md, not this pre-update SHA and not the accepted APP-BATCH-A code base.
- Current Policy remains Dictionary v1.2 -> Policy v1.8.9 -> Routing v1.3 -> shared PreExec v1.1 and schema v1. No Policy or Dictionary machine enum changed here.

**Owner-approved bounded APP development actions:** resume and finish remaining offline `frontend/**`, `tests/app_batch_b/**`, `reports/FOX2-M1-A-APP-BATCH-B/**` code/build/typecheck/tests/integration/delivery in this existing WP. Do not alter `backend/**`, contracts, provider/network operations, `agent_bridge/**`, main/PR/merge/deploy/LIVE, or other protected paths without a new material impact/authority decision. Do not repeat completed UI slicing, redraw the Dark/White presentation, or falsely claim previously accepted backend tests have just rerun.

**APP-BATCH-B route and minimal material preflight:**
1. CHAT binds exactly one APP task branch/worktree/source HEAD, approved code/test/report allowlist and one named writer. A remote Git-only task update is *document-only*; live Windows WIP and competing process ownership remain HOST_NOT_RECHECKED until observed.
2. Prefer an actual available **CLI-first CODEX/Copilot development execution route independent of installed Bridge**. Resolve `execution_path` only from the current Dictionary; do NOT invent a machine enum or claim `MANUAL_LOCAL` is implemented solely because the Dictionary declares it. A direct unsupported `codex exec` is not a governed replacement for an immutable Dispatch/attempt record. If manual admission is absent, report `DEV_ROUTE_NOT_IMPLEMENTED` once and resolve it at the existing engineering/dependency scope; never bypass claim/no-replay.
3. Shared task-specific PreExec v1 requires *app-relevant material checks*: correct Owner/code scope/source and worktree, one writer, supported Agent/model/permission and available Node/npm/pnpm only if actually required by this frontend, Python/backend/test dependencies if material, report delivery/readback, and proof of any manual DEV attempt control. **Bridge worker PAUSED is NOT a material check for an independently proven non-Bridge development route**; it remains material if Bridge is the route chosen. An old BLOCKED receipt (`reports/FOX2-M1-A-APP-BATCH-B/preexec/local_preflight.json` with `NO_AGENT_CURRENT_EXECUTION_PROOF`) is immutable historical evidence, NOT a present PASS or a reason to rerun stale profile checks as the answer.
4. Publish fresh shared v1 receipt at an unused append-only `reports/FOX2-M1-A-APP-BATCH-B/preexec/*.json` path, source-bound to exact branch HEAD before receipt publication; verify schema, remote SHA, byte readback, task/receipt identity, worktree and no-replay. No worker-control mutation is needed for CLI-first app-only checks if technically independent.
5. Only after actual `PASS` and CHAT R0–R7 `PASS_TO_ASSIGN` may the final Agent route/immutable handoff/attempt be issued. Allowed candidate: `CODEX / PINNED gpt-6.1-sol / medium / FULL_ACCESS` based on the earlier host marker proof for another WP, **not yet a live APP execution admission**. Keep `max_runs=1` and distinct APP attempt identity; no replay if started or uncertain.
6. CODEX/Copilot completes app build/typecheck, API wiring, watchlist CAS, data-source/unavailable truthfulness, responsive 1440/1024/390, offline localhost tests and security negative tests, then scoped non-main Git push/readback. CHAT reviews real diff/test logs; `ACCEPT/REWORK/HOLD` is separate from Agent self-report.

**Delivery sequencing:** APP-BATCH-B is the next product coding milestone; Bridge Manual Admission is its own existing infrastructure WP and can follow or run separately with distinct writers/paths once admitted. No new Owner-facing micro-WP, no routine WORK audit and no need to obtain the Owner's priority decision again. WORK is only for a concrete independent safety/release question.

**Protection:** Original PreExec compatibility Dispatch001 remains `PUBLISHED/HOLD`, Canary009 `HOLD`. The Bridge infrastructure receipt remains `BLOCKED`; it does not block APP preparation. No old Dispatch is relabeled or consumed. The current task document update does not launch an Agent.

```text
APP_BATCH_B_PRIORITY=ACTIVE
APP_BATCH_B_OWNER_BOUNDED_CODE_SCOPE=APPROVED
APP_BATCH_B_SOURCE_TASK=UPDATED
APP_BATCH_B_FRESH_PREEXEC=NOT_RUN
APP_BATCH_B_CHAT_ASSIGNMENT=HOLD_FRESH_PREEXEC
APP_BATCH_B_CODE_STARTED_BY_THIS_UPDATE=NO
BRIDGE_INDEPENDENCE=REQUIRED_FOR_CLI_FIRST_DEV_ROUTE
MASTER_PLAN_RELEASE_SYNC=PENDING
WORK=NOT_NEEDED
DISPATCH001=HOLD
CANARY009=HOLD
```
