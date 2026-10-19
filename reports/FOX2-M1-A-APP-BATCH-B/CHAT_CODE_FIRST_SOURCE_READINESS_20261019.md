# FOX2-M1-A-APP-BATCH-B — CHAT code-first source readiness (19 October 2026)

**Result:** `SOURCE_INSPECTION_COMPLETED / EXECUTABLE_ASSIGNMENT_HOLD_FRESH_ROUTE_PROOF`  
**Mode:** CHAT direct, read-only source/contract QA; this file is a report in the existing Whole-WP, **not a new WP, coding Dispatch, executable Agent prompt, acceptance certificate, or host preflight receipt**.  
**Skills actually read:** `fox2-source-resolver`, `fox2-agent-route-runtime`, `fox2-governance-preflight`, `fox2-agent-prompt-builder`, `fox2-document-publication`, `fox2-status-roadmap`, `fox2-result-review`, `fox2-execution-recovery`, `fox2-dictionary-impact` from `skills://plugins/fox2-skills-integrated/<name>/skill.md`.

## R0 / task status and source evidence

- Existing WP: `FOX2-M1-A-APP-BATCH-B`; product branch `work/FOX2-M1-A-APP-BATCH-B` at immutable observed HEAD `51a97bfa7420efa0a0e0ea9a1f35f77d2e823613`. Original task: `docs/agent_handoff/FOX2-M1-A-APP-BATCH-B/task.md`, blob `c9ac5d3f1b966694f2ccb5a03deb9ce97948a53b`.
- Current governance `main@e26fc7aa87e787852407261db90506b3516ba5de`: project-wide Governance Registry `docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json`, blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`; Owner scope selects Policy **2.0.0**, Dictionary **1.3**, Routing Index **1.4.0**, Git-first Protocol **12** for new/re-scoped CHAT work. Machine/Bridge installed adoption is separate/not attested.
- APP task retains historical Policy 1.8.9 / Dictionary 1.2 source binding and its old Bridge-first pause text. The **2026-10-19 CODE-FIRST resumption clause within the same task** supersedes the historical pause, but does not erase or silently rebind a prior executable attempt. Any *new Agent execution attempt* needs an exact new task/source-set binding rather than pretending the old locked Dispatch changed.
- Previously accepted APP-BATCH-A baseline, `3db6298e4286022e5820eb7b712c436cbade6a62`: **364 PASS / 3 superseded-stage deselections** is historical only. Do not rerun old P2 suites without material reason or call these APP-BATCH-B results.
- APP receipt `reports/FOX2-M1-A-APP-BATCH-B/preexec/local_preflight.json` is **BLOCKED** (2026-10-14, source `1e3993ed854e3bf576f4e195d96d58f0abbf3292`): `NO_AGENT_CURRENT_EXECUTION_PROOF`. It reported local Node 24.20.0/npm 11.19.0 PASS on that date; Copilot 1.0.97 `AUTH_REQUIRED`, CODEX CLI 0.162.1 `CLI_NONZERO`. These are neither today's quota/admission nor a fresh PASS.
- Remote Git repository inspection cannot establish Windows worktree cleanliness/owner, active writer, current Agent authentication/quota, current Node/npm/npm-cache, or installed/manual-attempt claim. All are **UNKNOWN** for execution.

## R1 / actual implementation delta observed at APP HEAD

- `frontend/src/App.tsx` (blob `5dd393e19146cc97bec73ba243b59e2e5fdb1ecb`) contains four route/screen families, Dark/White presentation, source/unavailable states, watchlist CAS UI, Stock360 bars, data-source diagnostics. **Do not redraw the existing UI**.
- `frontend/src/api.ts` (blob `718902e6e01b0a787610257c04447087c8b8c353`) uses relative `/api/...` requests for health, source-health, overview, watchlist GET/PUT, instrument search, stock, bars. Corresponding backend route *definitions* were visually inspected at `backend/src/fox2/api/{health,market}.py`. This is **source-level API-shape alignment only**, not a running integration PASS.
- Vite defines development `/api` proxy to loopback backend; the backend has loopback/Origin/Host protections. Built/preview-mode proxy behavior and reload/restart have **NOT** been exercised.
- `frontend/package.json` has `build` and `typecheck` scripts but **no frontend test script**. Git tree contains **no files under `tests/app_batch_b/**`**, and no new `reports/FOX2-M1-A-APP-BATCH-B/report.md` or `evidence_manifest.json` at this inspected HEAD.
- No new frontend typecheck, Vite build, browser 1440/1024/390, watchlist conflict/error, loopback/security negative test, localhost restart or end-to-end acceptance was run in this read-only review. Treat all as **NOT_RUN**, not FAIL or PASS. Existing `tests/app_batch_a/**` and backend evidence are not a substitute.

## R2–R7 / decision and minimal continuation

- **R2 (authority):** Owner approved CODE-FIRST continuation of the *existing* offline APP-BATCH-B within `frontend/**`, `tests/app_batch_b/**`, `reports/FOX2-M1-A-APP-BATCH-B/**`. No backend, provider/network, `agent_bridge/**`, main, merge, deploy or LIVE grant. Use the new approved governance identity for any *new* execution binding; preserve historical base, task semantics, acceptance and old locked work.
- **R3 (host capability):** live Copilot/CODEX executable/permission/quota and Windows source/worktree writer **UNKNOWN**. Fresh material route-specific preflight, an append-only receipt and Git readback are required before final executable assignment. Do **not** replay or blindly re-run the historical `preflight.ps1`, which includes branch/worktree mutation and prior-receipt cleanup; inspect a safe non-destructive host procedure first.
- **R4 (cost):** CHAT completes Git/source/code inspection directly. COPILOT is preferred for clear React/TS/Vite tasks **if** current CLI/capacity PASS; CODEX only if a verified eligible route is more appropriate. WORK is NOT_NEEDED for routine app continuation. A candidate preference is **not a final Agent assignment**.
- **R5 (writer):** original APP branch's local Windows worktree status is UNKNOWN; no code or report write was made there. This report is on the **separate CHAT-owned, report-only branch** to prevent a shared writer collision.
- **R6 (handoff):** after a future valid preflight, CHAT must publish the *exact executable* task/prompt and new source-set/attempt on authorized Git paths, verify immutable blob/SHA-256/readback, then hand off. Agent checks out exact SHA and returns code + `report.md` + `evidence_manifest.json` to a named non-main Git destination. CHAT independently reads, verifies and records ACCEPT/REWORK/HOLD. Never treat a chat prompt, an old receipt or a Git push alone as completion.
- **R7 (next sequence):** ① actual host APP source/worktree/one-writer + Node/npm/CLI/quota/attempt-control proof; ② create **fresh source-bound** PreExec evidence; ③ only if route passes, issue Git-first Agent implementation for **existing** APP-BATCH-B; ④ build/typecheck/frontend tests/API/offline responsive & security acceptance; ⑤ Agent Git result → CHAT acceptance. **STOP** for source drift, no supported independent route, competing writer, secret exposure or unsafe backend/network expansion.

`CODE_ALLOWED_FOR_EXECUTABLE_AGENT=HOLD_FRESH_HOST_PREEXEC`  
`BRIDGE_READY_GLOBAL_DEPENDENCY=NO`  
`NEW_WP=NO`  
`DISPATCH001=HOLD_UNCHANGED`  
`CANARY009=HOLD_UNCHANGED`  
`PRODUCT_ACCEPTED=NO`
