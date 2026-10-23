# FOX2-M1-A-APP-BATCH-B — CHAT direct Website increment (2026-10-23)

**Logical task:** FOX2-M1-A-APP-BATCH-B (same Whole-WP)  
**Status:** IN_PROGRESS / PRODUCT_NOT_ACCEPTED  
**Source:** work/FOX2-M1-A-APP-BATCH-B @ 51a97bfa7420efa0a0e0ea9a1f35f77d2e823613 (before this commit)  
**Route:** CHAT / direct Git-native reversible DEV / scope-limited; no Agent/Bridge dispatch.

## What changed
- Invalidate the previous stock/refresh response synchronously at render when a request key changes; stale asynchronous results remain discarded after effect cleanup.
- Render local process health as OK/UNHEALTHY, never as market LIVE; show Unknown provider mode if health evidence is missing.
- Sanitize *all* backend non-2xx error text before displaying it to investors; retain HTTP status and a safe 409 CAS-version hint.
- Add Node built-in regression tests for backend-only paths, watchlist CAS shape, secret-safe 4xx/5xx handling, request-key isolation and differentiation of local process health from market LIVE availability.

## Evidence / limitations
- Standalone reconstructed-file Node test harness: **4/4 PASS** in isolated tooling sandbox (Node 22 + TypeScript 5.8.3); this is NOT a current Git checkout/full frontend result.
- Remote Git commit/readback: **VERIFIED** for both CHAT changes `b48651b14e877e53be578a8512141e3f93878938` and `fe506361a9be6ab28e44791c2ba27988144049a8`; branch HEAD and changed path allowlist checked.
- Exact test-source Git blob parity: `api.ts=20b20989fb3ba60bb46076eff2a608ed74efb568`, `resourceVisibility.ts=4253deb9ce0b49d0f4eef2067ba5fd65e1ba18f5`, `healthTruth.ts=f096b65c9136db2345bb01a2444aec2e9f2639fb`, `api-resource.test.mjs=bab96c326da35324611cd4e756f3b1049e49fcf0`; all four hashes match locally executed sources.
- Static backend routing review: all eight invoked frontend API methods map to the accepted backend's `/api` endpoints; this is **not** an actual HTTP integration test.
- Actual `npm install/ci`, `npm run typecheck`, `npm run build`, browser tests at 1440/1024/390, backend localhost API integration and security review remain **NOT_RUN/NOT_VERIFIED** on this committed branch.
- Do not claim `FOX2_M1_A_RUNNABLE_LOCALHOST_OFFLINE_ACCEPTED` until those material gates pass.

## Scope
Changed files only under `frontend/**`, `tests/app_batch_b/**` and this `reports/FOX2-M1-A-APP-BATCH-B/**` report.
No `backend/**`, `agent_bridge/**`, BRD, governance, provider/broker/LIVE, main, merge or deploy changes.

**NEXT_SAFE_ACTION:** Install/reuse frontend dependencies on an authorized isolated host; run frontend tests/typecheck/build and localhost/browser offline integration; review actual remote result and record acceptance or same-WP rework.


## Native launcher recovery 2026-10-23

HOLD / BLOCKED_HOST_SANDBOX. Git identity was corrected locally; source-locked R3 invoked Codex once but sandbox setup failed before any process/test/code change. R3 is consumed: do not replay. See evidence/native-recovery-r3-20261023/report.md and evidence_manifest.json for actual host evidence, provenance and next safe action. Historical evidence above remains unchanged.

## Native Codex R4 outcome — 2026-10-23

**HOLD / BLOCKED_HOST_DNS_AND_SANDBOX.** R4 at assigned prompt commit `9b4386e9` was claimed and invoked once. The first native exec failed before PowerShell started. Codex also logged DNS failures connecting to its WebSocket endpoint. No product changes or tests were reported; independent Git readback showed no remote product code result. Owner launcher correctly stopped at missing deliverable. **R4 CONSUMED; do not replay.** Source observations and limitations: `evidence/native-r4-20261023/host-blocker.md`. All historical tests retain their original provenance; Website remains unaccepted.
