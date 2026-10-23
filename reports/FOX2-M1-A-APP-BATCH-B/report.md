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

## Codex Extension continuation — 2026-10-23 (Asia/Saigon)

**Status: BLOCKED_BACKEND_LOCALHOST / CHAT_ACCEPTANCE=PENDING.**
Same Whole-WP, assigned source `ee4784e9fbf055979dea540242ce74f2b79736cc`, branch `work/FOX2-M1-A-APP-BATCH-B`.

### Preflight and scope
- Exact workspace/branch/HEAD matched; `git status --porcelain=v1` empty before writes. Repeated HEAD/status observations unchanged.
- VS Code window title: `Welcome - repo - Visual Studio Code`; workspaceStorage folder resolves to the assigned repo. Extension activation and current task activity observed in its log. CHAT designated this current Extension as the only Website writer; no competing writer/source change observed. Existing app-server processes alone are not treated as writers.
- No R5 execution process/marker observed in checked locations. No CLI/Bridge/launcher replay or model change initiated. Requested route remains Extension/manual handoff; model/effort not independently attested by these shell checks.
- No frontend source, backend, contracts, governance or historical evidence edited. npm generated `frontend/package-lock.json` for reproducibility. Aggregate report/manifest were copied byte-for-byte to `evidence/ide-20261023/history/` before updates.
- Initial history-copy command used the frontend working directory and failed to resolve report paths; corrected before aggregate updates. No historical files overwritten.

### Actual commands and results
Working directory for npm commands: `frontend/`. Logs: `evidence/ide-20261023/`.

| Command | Exit | Result | Evidence |
|---|---:|---|---|
| `npm install --no-audit --no-fund` | 0 | PASS; 67 packages installed | `install.txt` |
| `npm run typecheck` | 0 | PASS | `typecheck.txt` |
| `npm run build` | 0 | PASS; 35 modules, production bundle generated | `build.txt` |
| `npm run test` | 0 | PASS; 4 passed, 0 failed | `test.txt` |
| Node fetch to `http://127.0.0.1:8000/api/health`, 5-second timeout; non-OK/network failure sets exit 1 | 1 | FAIL / ECONNREFUSED | `backend-http.txt` |

Runtime dependencies FastAPI, uvicorn, httpx and pytest import successfully under installed Python. No backend or frontend listener was observed on 8000/5173 before integration. No services were launched by this continuation. Build output is local; build PASS is not browser or HTTP acceptance.

### Acceptance mapping
| Acceptance | Current observation | Status |
|---|---|---|
| Typecheck/build/focused tests | Current checkout commands above | PASS |
| `/overview`, `/watchlist`, `/stocks/:symbol`, `/settings/data-sources`, direct reload | No browser runtime performed | NOT_RUN |
| Watchlist add/remove, persistence/restart, CAS 409, invalid/unknown 422, duplicate, max 100 | Existing helper checks CAS request shape only; no localhost mutation | NOT_RUN |
| UNKNOWN/STALE/GAP/UNAVAILABLE, provenance/as-of, missing != zero | Existing helper checks request-key isolation and health != LIVE; broader render behavior untested | PARTIAL_HELPER_ONLY / runtime NOT_RUN |
| API error secrecy | Helper executes 400/401/403/404/409/422/429/500/503 and checks sentinel not reflected | PASS_HELPER_ONLY |
| Real HTTP 404/409/422/503, Host/Origin/content-type negatives | Health connection failed before HTTP response | NOT_RUN |
| Backend localhost connectivity | ECONNREFUSED | FAIL |
| Dark/Light at 1440/1024/390 | No browser checks/screenshots | NOT_RUN |
| No direct provider calls | Helper confirms eight methods use relative `/api/` paths | PASS_HELPER_ONLY |
| Full bundle secret scan, polling-storm, browser network and no fake price/NAV/action checks | Not executed | NOT_RUN |

### Blocker and handoff
First material runtime blocker: no accepted backend service reachable at `127.0.0.1:8000`. Per task STOP instruction, no further runtime tests or speculative frontend changes followed.
The read-only backend composition defaults to an empty instrument registry and no explicit store root (`backend/src/fox2/runtime/__init__.py`, `backend/src/fox2/config.py`); starting that default alone would not establish a configured persistent Watchlist. Data Contract v0.4 requires an explicit FOX2 DEV store outside the repo, while this assignment limits writable paths to frontend/tests/report paths. No external store or synthetic investor universe was created.

CHAT next action: provide/start the accepted offline backend at port 8000 with its authorized explicit store and verified instrument source, then resume this same Whole-WP. Isolated test fixtures must remain labelled test-only.

`RESULT_MODE=CODE_CHANGE` remains the assignment; **TEST_EVIDENCE_ONLY_CANDIDATE** is proposed because no application source defect was changed. CHAT must decide classification; this is not acceptance.
`GIT_DELIVERY_PENDING`: no commit/push performed; session publication rights not verified and runtime result blocked. Remote result SHA not claimed.

## Backend integration recovery in the same Extension session — 2026-10-23

**Current status: STOP / BLOCKED_FRONTEND_PROXY_ORIGIN_GUARD. CHAT_ACCEPTANCE=PENDING.**
The earlier ECONNREFUSED was absent service, not an API defect. Per CHAT authorization, the continuation used accepted `create_app`, `OfflineRuntime`, `SQLiteStore(profile='ISOLATED_TEST')` and `InstrumentRegistry(source='ISOLATED_TEST_UNIVERSE', coverage='PARTIAL')`. Only fixture instrument identifiers and preferences were created. No quote/bar values were seeded; investor default composition is unchanged. Each execution used a fresh FOX2 SQLite root outside Git, recorded in `http-results.json` and retained for inspection.

### Reproducible commands and exits
- Frontend cwd: `npm run dev -- --host 127.0.0.1 --strictPort` started Vite 5.4.14 successfully on port 5173 (ready in 307 ms). The owned dev server was stopped after the safety finding; interrupt exit 1 is service shutdown, not a build/test result.
- Repo cwd: `python -B tests/app_batch_b/http_integration.py --evidence reports/FOX2-M1-A-APP-BATCH-B/evidence/ide-backend-integration-20261023` — exit **1**. Fifteen checks passed before the reload harness sent `Accept: application/json` and got 404. This was a harness header error; it is not evidence that browser reload is broken. Original output/results preserved.
- Repo cwd: `python -B tests/app_batch_b/http_integration.py --evidence reports/FOX2-M1-A-APP-BATCH-B/evidence/ide-backend-integration-20261023-corrected` — exit **1**, **17 PASS / 1 FAIL**. Corrected reload requests use `Accept: text/html`. Execution stopped immediately at the critical proxy guard failure.
- ASGI child commands are implemented in the harness: `python -B tests/app_batch_b/local_test_backend.py --store-root <fresh external root> --port 8000`, restart on the same root, and port 8001 with `--unconfigured` for real HTTP 503. Child output is preserved in each directory's `asgi-output.txt`.
- Prior install/typecheck/build/focused **4/4 PASS** and their command/output/exit evidence remain under `evidence/ide-20261023/`; unaffected frontend source/dependencies were not changed, so these were not rerun.

### Observed safety defect — STOP condition
Direct accepted backend rejects a foreign Origin with **403** and preserves preferences. The Website dev proxy accepts the same foreign Origin mutation:

```http
PUT http://127.0.0.1:5173/api/watchlist
Origin: https://evil.example
Content-Type: application/json

{"expected_version":5,"items":[]}
```

Observed **200**, stored preference version **5 -> 6**, items cleared in the isolated test store. `frontend/vite.config.ts` unconditionally removes `origin` in `proxyReq`, so backend Origin enforcement does not survive the Website proxy boundary. This is an HTTP boundary failure; browser exploitability/CSRF was not tested or asserted. Only loopback HTTP was used; the Origin header did not contact the example domain.

Per the user's explicit safety STOP, **no proxy/application fix or further product test followed**. Next safe action for CHAT: authorize the bounded frontend proxy correction in this same Whole-WP, validating the incoming loopback Host/Origin before translation; preserve legitimate same-origin JSON PUT while rejecting foreign/mismatched/null Origin before forwarding. Backend/API contract changes are not needed by the observed reproduction.

### Updated acceptance mapping (test fixtures only)
| Acceptance | Result and scope |
|---|---|
| Backend health, watchlist, stock and Vite proxy | PASS over actual TCP HTTP; provider disabled, no seeded market values |
| Watchlist add/remove, readback | PASS HTTP; actual accepted SQLiteStore |
| Persistence/restart | PASS after terminating and recreating the owned ASGI process with the same external SQLite root |
| CAS stale update / concurrent update | PASS 409 preserves prior state; concurrent statuses [200,409] and persisted winner |
| Invalid/unknown/duplicate/max 100 | PASS 422 preserves state; exactly 100 accepted, 101 rejected |
| 404/422/503 | PASS real HTTP; 503 from a separate unconfigured-store composition, sanitized body |
| Backend Host/Origin/content-type guards | PASS 400/403/415 with unchanged preferences; valid same-origin health accepted |
| Website proxy foreign Origin guard | **FAIL: expected 403, actual 200 with mutation** |
| Four routes/direct reload | PASS HTTP HTML entry for overview/watchlist/stocks/AAA/settings/data-sources; browser navigation/rendering NOT_RUN |
| UNAVAILABLE/UNKNOWN and missing != zero | PASS HTTP: payload/as_of null, freshness UNAVAILABLE, source UNKNOWN, audit ID present |
| STALE/GAP/provenance presentation, UI Watchlist behavior | NOT_RUN; no market fixture values were created to pretend provider evidence |
| Dark/Light and 1440/1024/390, screenshots, polling/network browser checks | NOT_RUN: browser inventory empty; IAB creation returned `Browser is not available: iab` |
| Full bundle secret scan | NOT_RUN; helper secret-redaction PASS retains its narrower scope |

All owned ASGI children and Vite were stopped; listener readback showed no listeners at 8000/8001/5173. Existing external test stores and all run evidence retained. No backend/Bridge/governance edits or Git publication.

`RESULT_MODE=CODE_CHANGE` remains assigned. Changes in this continuation are test harnesses/evidence; application correction remains outstanding. `GIT_DELIVERY_PENDING`: safety STOP; publisher rights not verified, no commit/push. This is not a successful Whole-WP closure or an evidence-only reclassification.

## Vite Origin guard rework — 2026-10-23 (same Whole-WP)

**SECURITY_ORIGIN_GUARD=PASS / HTTP_TESTS=PASS / CHAT_ACCEPTANCE=PENDING.**
Assignment result mode remains **CODE_CHANGE**. Application change is confined to the existing Vite 5 dev proxy and its type dependency; no UI redesign, backend/API contract or investor-default fixture changes.

### Implementation
`frontend/vite.config.ts` registers a `configureServer` middleware directly, before Vite's internal proxy. It checks exact Host `127.0.0.1:5173`, exact supplied Origin `http://127.0.0.1:5173`, duplicate Host/Origin/content-type via raw header pairs, and requires Origin on every method except GET/HEAD/OPTIONS. Wrong/missing/duplicate Host and duplicate headers return 400; invalid/null/foreign or missing mutation Origin returns 403. Responses contain fixed safe text.

Only middleware-validated requests may enter the proxy's `proxyReq` path (WeakSet receipt). A verified frontend Origin is translated to `http://127.0.0.1:8000`; read-only requests with no Origin retain its absence. `changeOrigin` continues to send backend Host correctly. No unconditional Origin deletion or CORS relaxation. `strictPort: true` prevents silently moving away from the pinned frontend authority.

Added pinned `@types/node` 22.10.5 to type-check Node raw headers used by Vite config; package lock updated. Initial typecheck failed because Node declarations were missing (exit 2; `typecheck.txt` retained), then dependency install and all final checks passed. This failure was corrected, not omitted.

### Commands and observed results
All new evidence: `evidence/ide-origin-guard-rework-20261023/`.

| Command | Cwd | Exit | Result / output |
|---|---|---:|---|
| `npm install --save-dev --save-exact @types/node@22.10.5 --no-audit --no-fund` | frontend | 0 | PASS, 2 packages; `node-types-install.txt` |
| `npm run typecheck` | frontend | 0 | PASS; `typecheck-final.txt` |
| `npm run build` | frontend | 0 | PASS, 35 modules; `build-final.txt` |
| `npm run test` | frontend | 0 | PASS 4/4; `test-final.txt` |
| `npm run dev -- --host 127.0.0.1 --strictPort` | frontend | service | Ready in 350 ms; `vite-output.txt`; owned server stopped after checks (interrupt exit 1) |
| `python -B tests/app_batch_b/http_integration.py --evidence reports/FOX2-M1-A-APP-BATCH-B/evidence/ide-origin-guard-rework-20261023` | repo | 0 | PASS **22/22**; `http-command-output.txt`, `http-results.json` |
| `node tests/app_batch_b/scan_frontend.mjs` | repo | 0 | PASS; 14 source/config/dist files including sourcemap, 5 credential patterns, 0 findings; `secret-scan.txt` |
| `git diff --check` | repo | 0 | PASS |

### Before/after proof and acceptance mapping
- Before: immutable `evidence/ide-backend-integration-20261023-corrected/http-results.json` records **17 PASS / 1 FAIL**, foreign Origin PUT 200 and isolated version 5 -> 6.
- After: foreign Origin PUT **403**, **0 upstream ASGI receipts**, entire Watchlist snapshot unchanged. This includes version, items and updated_at, not only item count.
- **28 additional header cases PASS:** null/malformed/spoofed/scheme/authority/path/query/fragment/comma/port Origin variants; missing Origin on PUT/POST/PATCH/DELETE; duplicate identical and mixed Host/Origin; missing/wrong/alias Host; duplicate content-type; foreign/null Origin GET. Each denial is checked before any backend receipt; snapshots remain unchanged.
- Valid frontend same-origin JSON PUT **200**, real backend receipt contains Origin **http://127.0.0.1:8000** and Host **127.0.0.1:8000**. Six trusted-origin backend PUT receipts cover positive and contract-negative requests.
- CAS stale/concurrent updates **409**, winner preserved; invalid/unknown/duplicate and 101 items **422**, exactly 100 accepted. Contract checks execute both directly and through the fixed Website proxy. Non-JSON content-type still **415**, backend policy unchanged.
- Persistence PASS after actual ASGI child termination/restart on the same external SQLite store. Direct backend foreign Origin remains **403**. Real HTTP **404/422/503** checks PASS.
- Honest data states PASS over HTTP: payload and as_of stay null; UNAVAILABLE and source UNKNOWN remain explicit; no prices/bars seeded. Fixture registry is `ISOLATED_TEST_UNIVERSE`, store metadata `ISOLATED_TEST`; this is not investor-universe verification.
- Provider boundary: provider_enabled=false. Test-only transport tripwires on DNS/connect/connect_ex reject non-loopback targets; three child-process logs have **0 non-loopback attempts**. This does not substitute for browser network inspection.
- Secret safety: existing error-redaction helper covers 400/401/403/404/409/422/429/500/503; bounded static credential scan found no matches. This is not an assertion that every possible secret can be detected.
- Four direct route requests return HTML for `/overview`, `/watchlist`, `/stocks/AAA`, `/settings/data-sources`. **Browser UI/navigation, Dark/Light, responsive 1440/1024/390, screenshots, STALE/GAP rendering and polling inspection remain NOT_RUN.** Current browser tool inventory is `{apps:[],browsers:[]}`; no browser surface available. HTTP entry serving is not browser rendering evidence.

Backend receipt logs record only test method/path/Host/Origin (no request bodies/secrets); external stores retained. All owned Vite/ASGI servers stopped; listener readback showed no listeners on 5173/8000/8001. Prior evidence files remain untouched; pre-rework aggregate report/manifest copies are preserved in this run's history directory.

### Publication and handoff
Publisher verification: local `gh api user --jq .login` -> dunglt2505; `gh api repos/dunglt2505/FOX2 --jq '{full_name:.full_name,permissions:.permissions}'` -> matching repository with push/admin true (exit 0). Local Git origin points to `https://github.com/dunglt2505/FOX2.git`; branch/HEAD match the assignment. `git ls-remote --exit-code origin refs/heads/work/FOX2-M1-A-APP-BATCH-B` read back expected source SHA `ee4784e9fbf055979dea540242ce74f2b79736cc` (exit 0). `git push --dry-run origin HEAD:refs/heads/work/FOX2-M1-A-APP-BATCH-B` succeeded (exit 0, Everything up-to-date). This establishes the scoped publisher precondition; actual commit/push/readback result is reported separately after this artifact is finalized.

Whole-WP is **not DONE**: browser acceptance remains NOT_RUN and CHAT owns final acceptance. No merge/main/deploy/provider/broker/LIVE action.

Publication result: code/tests/evidence commit `5690afb29b662bd62a0adaea364c2c29a1146e45` pushed to `work/FOX2-M1-A-APP-BATCH-B` (exit 0) and independently read back with `git ls-remote` (exit 0, identical SHA). All 42 pre-commit inventory entries match committed bytes; original aggregate history copies match the assigned source bytes. Receipt: `evidence/ide-origin-guard-rework-20261023/publication-receipt.json`. A following metadata commit records this receipt; its final observed remote SHA is returned in the handoff. CHAT_ACCEPTANCE=PENDING.
