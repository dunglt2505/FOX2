# Goal
Complete the EXISTING FOX2-M1-A-APP-BATCH-B Website Whole-WP: first runnable localhost M1-A React/TypeScript/Vite UI integrated with the accepted offline backend. Preserve the existing Dark/White presentation and theme toggle; finish wiring, correctness, tests and evidence, not a redesign.

# Scope
Only frontend/**, tests/app_batch_b/**, reports/FOX2-M1-A-APP-BATCH-B/** are writable. Everything else, especially backend/**, tests/app_batch_a/**, contracts, provider/DSM/store, agent_bridge/** and governance, is read-only. Do not modify historical preexec evidence. One named code writer: this Codex invocation in the runner's fresh isolated clone. No subagents or other code writers.
No main/merge/PR/deploy/provider/broker/LIVE, credential handling or real-money operations. No real investor data fixtures or synthetic fallback. Package registry/browser tooling downloads for development are allowed; runtime/test traffic must stay loopback or in-process and must not contact providers. Do not weaken tests, security guards or backend API to make a test pass.

# Context
Base branch work/FOX2-M1-A-APP-BATCH-B at 51a97bfa7420efa0a0e0ea9a1f35f77d2e823613; accepted backend APP-BATCH-A at 3db6298e4286022e5820eb7b712c436cbade6a62, historical 364 PASS / 3 superseded stage-only deselections (not a fresh test run).
Read source-lock.json and task.md supplied beside this prompt by runner. Governance files are read-only in governance/ beside it, pinned to main 0da03b052c6a63d560e830c7956a2625c0bfe843: Registry resolves Policy 2.1.0, Routing 1.5.0, Protocol 13 for this prospective native continuation. Do not apply old Bridge-only admission or scheduling text as a current native coding block; do not change/replay any old Dispatch, receipt or machine contract.
Product sources at base: BRD-00/06/08 v0.5, M1 Technical Spec v0.1, Market Data Contract/schema v0.4, M1 Acceptance v0.4 and its change/requirement map. Read the technical Registry Binding v1 supplied in governance (absent from APP base). BRD-08 v0.4 acceptance semantics stay pinned at 955e74ff67e6b4ed184dc2c2dcd4260c51dc529b where v0.5 delegates; same file bytes in APP base may be used after comparison if needed. Do not redefine acceptance IDs. Historical NO_DEV in source documents is not the separate current Owner bounded DEV authorization.
Backend/API is frozen. If a reproducible backend defect prevents completion, stop with request/response/test reproducer and report precise blocker, without a backend edit.

# Execution
Actor CODEX; model gpt-6.1-sol; reasoning medium; native Windows PowerShell. Runner pins these unchanged and grants workspace-write sandbox with development dependency downloads. Do not change model, bypass sandbox, elevate or edit user config.
Inspect existing frontend/package.json, Vite proxy, API client and accepted backend tests first. Establish actual dependencies and use a local environment within frontend/ or tests/app_batch_b/; do not install globally. Add lockfile and focused frontend/browser tests where needed. Test fixtures must be isolated and clearly labeled; normal investor startup stays provider-disabled and truthful unavailable.
Implement only causal frontend/test fixes. Use actual accepted API to prove compatibility, including loopback proxy Host/Origin handling; a mocked UI test alone is insufficient for backend integration acceptance. Use disposable app/store state under allowed test/report paths, never real Owner DB.
Run frontend typecheck/build; meaningful UI/API and negative tests; affected backend regression without changing accepted tests. Record exact selection and any deselection reason, not fabricated full-suite PASS. Ordinary in-scope test failures can be repaired and rerun here. Stop if missing host capability, auth/capacity failure, security boundary, source mismatch or out-of-scope fix is required.
Launch services only on 127.0.0.1, localhost or ::1, with provider disabled. Clean up only processes started by this invocation in finally; never kill unrelated services.

# Acceptance
- Four real routes /overview, /watchlist, /stocks/:symbol, /settings/data-sources navigate and reload.
- Watchlist search/add/remove, persistence through restart, stale-version 409/conflict recovery, invalid/unknown/duplicate/>100 validation are covered with verified instruments in isolated tests. No lost update.
- Truthful per-widget source, as-of, coverage, freshness, finality, gap/provisional/basis and unavailable state; UNKNOWN != 0, genuine zero retained, history close never current quote, no fake prices/trends/NAV/scores/BUY-SELL or private facts.
- Browser calls only FOX2 backend; disabled provider/manual refresh cannot trigger upstream, backfill or polling storms. No credentials, raw provider errors or unsafe text in UI/bundle/source maps/logs; diagnostics read-only.
- Actual browser checks at widths 1440/1024/390 for BOTH themes: navigation, tables, no page overflow, status text plus color, no unexplained console errors. Capture screenshots and console/network evidence. State variants may use isolated fixtures, clearly distinguish fixture UI coverage from real offline backend.
- Actual localhost startup/navigation/deep-link refresh/stop/restart works. Loopback Host/Origin/content-type security negatives and sanitized 404/422/503 behavior covered at relevant boundaries.
- Map evidence to FOX2-08-T01..T14 and relevant BRD-06/N1/WS08 IDs with subcase/environment. Offline/fixture coverage cannot prove real provider/WS readiness; label those NOT_RUN/out-of-scope and preserve historical PASS with original provenance.
- Scope allowlist, diff whitespace and focused secret scan pass. Do not claim acceptance from source inspection alone.

# Return
Write reports/FOX2-M1-A-APP-BATCH-B/report.md and evidence_manifest.json plus material evidence/** (test commands, exit codes, outcomes, source/environment, acceptance subcases, screenshots/logs and SHA-256 hashes). Exclude secrets, dependency caches, local DBs and generated bulk artifacts from Git.
Manifest must identify task, base, exact assigned model/effort, changed paths, evidence digests and actual PASS/FAIL/NOT_RUN/UNKNOWN; no self-referential result commit SHA. Report reused backend evidence separately from fresh tests and enumerate remaining defects and startup instructions.
No git commit/push by Codex: the authorized PowerShell runner owns publication after checking final paths and reports. If blocked, still produce truthful bounded report/manifest without relabeling blockers PASS; do not expand scope. Final response concise, with outcome and whether remaining work blocks acceptance. Runner publishes candidate result and returns REMOTE_RESULT_SHA outside committed files; CHAT then reviews ACCEPT/REWORK/HOLD. Do not mark whole task accepted yourself.
