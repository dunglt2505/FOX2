# FOX2-M1-A-APP-BATCH-A implementation result

Status: IMPLEMENTED / UNREVIEWED. This is one whole WP. Agent-owned delivery on `work/FOX2-M1-A-APP-BATCH-A-codex`; no PR, main write, merge, deployment, provider/broker access or LIVE. CHAT's source authority was used as supplied; no release discovery was repeated. The starting worktree was clean at `0b559eb`; the accepted application base is `d90987afd861a41aef01059d95ca039509ede09c`.

## Implemented behavior

Offline FastAPI composition joins the frozen Foundation contracts, SQLite store and DataSourceManager. Only the eight approved method/path pairs are exposed. Process health is independent of source readiness; DSM's frozen conservative source-health DTO continues to report UNKNOWN/UNAVAILABLE and NOT_INTEGRATED because provider transport is absent.

The application registry accepts trusted, locally supplied instrument DTOs with explicit source/revision/coverage. It rejects missing provenance and ambiguous IDs/symbols. It provides bounded symbol search and universe/query-bound opaque cursors. The default registry is empty with UNKNOWN coverage; no invented default stock/index universe or market values is installed. Overview returns index envelopes for locally verified indices, or repeated `symbols=IDX` queries. An empty universe returns `[]`. Unknown symbols return sanitized 404; malformed symbols/queries return 422. Stock output is `{instrument,quote}` with a frozen market envelope in `quote`.

Every market request invokes the accepted DSM with DISPLAY rights. QUOTE/BARS/INDEX remain separate. Unavailable observations preserve null payload, source/record identifiers and observation timestamps, UNKNOWN rights/mapping, a selection audit ID and sanitized reason. Unsafe store reads return 503. Genuine zero values and null missing amounts survive successful selection unchanged. No history-to-quote fallback, synthetic investor values, account/order endpoints, provider client, scheduler or network retry exists.

Bars accept timeframe `1D`, `from`/`to` UTC timestamps and a 1..366-day window, with RAW/ADJUSTED/UNKNOWN basis. Unsupported basis or a requested window outside the selected observation coverage returns an unavailable envelope. Supported windows filter bar start times using `[from,to)`. This batch consumes frozen store projections; it does not add a history repository or aggregate missing history. Existing verified bar gaps are rejected by DSM; missing coverage is explicit via unavailable selection reason, rather than fabricated bars/gap payloads. With no verified policy supplied, the DSM fails closed.

Watchlist GET/PUT uses the existing SQLite preference repository. PUT validates strict DTO types, uniqueness and max100 before the atomic repository CAS. Unverified IDs return 422, stale versions 409, successful writes increment version/time once, and failures return sanitized 503 with rollback. Exactly100 items, concurrent HTTP writers, restart persistence and every preference fault-hook transaction stage are covered. Preferences trigger no market/provider operations.

Peer, Host, same HTTP Origin, duplicate-header and JSON content-type guards precede mutation. Authority validation supports localhost, 127.0.0.1 and bracketed ::1 while rejecting external/malformed Hosts, credentials, paths and invalid ports. Requests are limited to 64KiB for PUT. Validation and unexpected exceptions do not echo input values, headers, database paths or raw exceptions.

## Local runtime configuration

`create_app(Settings(store_root=<absolute FOX2-only path outside every Git worktree>))` builds the runnable ASGI application. Store creation is lazy and uses the accepted safety checks/migration. The factory performs no store initialization or provider I/O. Import loads the frozen local schema but does not initialize the store. Environment variables/credentials are never read. Without an explicit store root, preference/data operations requiring a store return sanitized 503; the empty-universe search/overview and diagnostics remain usable. A trusted local composition may pass `OfflineRuntime(settings, registry=InstrumentRegistry(...), policies=...)`; HTTP cannot add instruments or enable provider access.

Example for a host with Uvicorn installed (existing project packaging was kept read-only):

```powershell
$env:PYTHONPATH='backend/src'
python -c "import uvicorn; from fox2.config import Settings; from fox2.main import create_app; uvicorn.run(create_app(Settings(store_root='C:/FOX2-offline-store')), host='127.0.0.1', port=8000)"
```

No actual listener was launched for verification. Loopback ASGI requests test the application under socket/DNS and HTTP transport construction denial. The DSM's sanitized audit records are retained in a bounded 1000-record in-memory ledger; this is local diagnostic evidence, not a new durable store schema.

## Validation and evidence

Run `python -B tests/app_batch_a/verify_delivery.py` from this exact worktree. It records exact per-suite and combined commands, selected environment/package versions, complete outputs, frozen-file hashes, changed-path allowlist, secret pattern scan and diff checks in `evidence/`; `evidence_manifest.json` binds evidence byte counts and SHA256 values. Final results: APP Batch A 92 passed; P2-01 78 passed / 2 deselected; P2-02 96 passed / 1 deselected; P2-03 98 passed; combined 364 passed / 3 deselected. All minimum task gates passed before Git publication. No acceptance-matrix blanket PASS or P4 acceptance is claimed; UI, provider/WebSocket and later-domain cases remain outside this WP.

Three upstream stage-only tests are explicitly deselected without editing upstream tests:

- P2-01 `test_route_allowlist` assumes only foundation health routes. Replaced by the batch exact eight-route allowlist.
- P2-01 `test_domain_dependency_boundary` ends by asserting store/DSM do not exist. Its complete AST dependency checks and provider absence are retained in `test_frozen_domain_dependency_boundaries`.
- P2-02 `test_domain_dependency_boundary_for_p2_02_stage` ends by asserting DSM does not exist. The same domain checks/provider absence remain covered, and upstream store import/frozen-file checks run unchanged.

The read-only upstream Windows temporary-directory compatibility plugin is loaded explicitly. Asyncio's harness wakeup socket is created before socket denial; connect/connect_ex/bind/listen/sendto/DNS and HTTP transport construction are denied throughout batch requests. Blocking `send` on that preexisting wakeup socket initially stalled the test harness; that harness-only overblocking was corrected, without permitting any socket creation/connection or application transport. An initial IPv6 assertion exposed Starlette TrustedHost parsing behavior; explicit authority validation fixed it. A test basename collision during combined collection was resolved by renaming only the batch test. All final regressions run after those corrections.

Secret scanning checks common private-key/token formats and long credential assignments without printing matched content. Test-only sentinel values and isolated DTO claims are deliberate negative/contract fixtures. No real credentials, private accounts or licensed provider data were used. All P2-01/P2-02/P2-03 modules and tests remain unchanged, as checked against the accepted application base.

## Publication procedure

Stage only allowed paths, verify staged diff/allowlist, commit this task branch, push it to the exact same origin branch, then read back its full SHA with `git ls-remote` and require equality to local HEAD. The final user receipt is issued only after that remote publication succeeds. Git commands/output provide the actual commit and remote-readback evidence; a commit cannot contain its own SHA without changing it.
