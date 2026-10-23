# FOX2-M1-A-APP-BATCH-B — CHAT direct Website increment (2026-10-23)

**Logical task:** FOX2-M1-A-APP-BATCH-B (same Whole-WP)  
**Status:** IN_PROGRESS / PRODUCT_NOT_ACCEPTED  
**Source:** work/FOX2-M1-A-APP-BATCH-B @ 51a97bfa7420efa0a0e0ea9a1f35f77d2e823613 (before this commit)  
**Route:** CHAT / direct Git-native reversible DEV / scope-limited; no Agent/Bridge dispatch.

## What changed
- Invalidate the previous stock/refresh response synchronously at render when a request key changes; stale asynchronous results remain discarded after effect cleanup.
- Sanitize *all* backend non-2xx error text before displaying it to investors; retain HTTP status and a safe 409 CAS-version hint.
- Add Node built-in regression tests for backend-only paths, watchlist CAS shape, secret-safe 4xx/5xx handling and request-key isolation.

## Evidence / limitations
- Standalone reconstructed-file Node test harness: **3/3 PASS** in isolated tooling sandbox (Node 22 + TypeScript 5.8.3); this is NOT a current Git checkout/full frontend result.
- Git branch commit and remote byte readback to be verified separately after publication.
- Actual `npm install/ci`, `npm run typecheck`, `npm run build`, browser tests at 1440/1024/390, backend localhost API integration and security review remain **NOT_RUN/NOT_VERIFIED** on this committed branch.
- Do not claim `FOX2_M1_A_RUNNABLE_LOCALHOST_OFFLINE_ACCEPTED` until those material gates pass.

## Scope
Changed files only under `frontend/**`, `tests/app_batch_b/**` and this `reports/FOX2-M1-A-APP-BATCH-B/**` report.
No `backend/**`, `agent_bridge/**`, BRD, governance, provider/broker/LIVE, main, merge or deploy changes.

**NEXT_SAFE_ACTION:** Install/reuse frontend dependencies on an authorized isolated host; run frontend tests/typecheck/build and localhost/browser offline integration; review actual remote result and record acceptance or same-WP rework.
