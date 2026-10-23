# FOX2 Website — Native Codex R4 (same Whole-WP)

## Goal
Finish the EXISTING `FOX2-M1-A-APP-BATCH-B` localhost website, not a new task. Preserve Dark/White UI and accepted backend, complete remaining frontend/API integration, tests, browser checks and Git evidence.

## Scope
Write only `frontend/**`, `tests/app_batch_b/**`, `reports/FOX2-M1-A-APP-BATCH-B/**` except immutable historical `preexec/**` and `evidence/native-recovery-r3-20261023/**`. Backend, accepted tests, BRD/TechSpec/contracts, governance, `agent_bridge/**` and all other paths READ-ONLY. One Codex writer only; no subagents. Do not modify Git history, branch, task/prompt files or any credential. No main, merge, PR, deploy, provider network, broker, order, account or LIVE. Localhost/test fixtures only; no fabricated investor prices or missing=zero.

## Context
Product/result branch `work/FOX2-M1-A-APP-BATCH-B` at immutable source `21d023c6c3fd4d379f7e7427d9eb6c97b5ea0e05`; its parent is `92191f1d9701a9886ed886e6653e39d604b8b617`. R3 published only 15 report/evidence changes and is CONSUMED/HOLD; never replay. R3 source report `reports/FOX2-M1-A-APP-BATCH-B/evidence/native-recovery-r3-20261023/report.md` remains historical. Owner-host independent sandbox probe: `SANDBOX_PROBE=PASS`, `FOX2_SANDBOX_RECOVERY=PASS` on 2026-10-23; proves PowerShell startup and temporary read/write/delete, NOT Website tests or full Codex capacity.

Current human authority: Governance Registry `main@0da03b052c6a63d560e830c7956a2625c0bfe843`, Policy 2.1.0 / Routing 1.5.0 / Protocol 13. Same already-approved offline bounded APP DEV scope. Released product sources: BRD-00/06/08 v0.5, Technical Spec v0.1, Market Data Contract/schema v0.4, Acceptance Matrix v0.4. Accepted backend APP-BATCH-A SHA `3db6298e4286022e5820eb7b712c436cbade6a62`; historical 364 PASS does not constitute this run. Existing focus tests 4/4 PASS in isolated tooling, not full actual checkout. Read existing task.md, R3 report, source, existing frontend/tests and applicable contracts. Avoid obsolete machine-only Bridge PreExec/Dispatch wording for this independent native DEV route.

## Execution
Actor `CODEX`; Model `gpt-6.1-sol`; thinking `medium`; Windows PowerShell / native CLI; sandbox `workspace-write`. Runner supplies command, isolated writer/process claim, source verification, Git publisher and exact result destination. Never change model/effort/sandbox. Do NOT git commit/push; OWNER_POWERSHELL_RUNNER is the authorized result publisher on the same product branch only.

Run actual dependency install within frontend (local, no global install), typecheck, build, tests, localhost backend HTTP integration, offline start/restart, and browser checks at 1440/1024/390 for both themes when browser capability is real. Preserve passing source/health/resource-key truthfulness and error-sanitization helpers. Fix causal defects only within allowlist, do not alter frozen API. If backend incompatibility occurs, include exact reproducer and STOP. Do not claim missing browser capability as PASS.

## Acceptance
- Real routes `/overview`, `/watchlist`, `/stocks/:symbol`, `/settings/data-sources` navigate and deep-link refresh.
- Watchlist CAS 409/conflict recovery, duplicate/invalid/unknown/max-items validation, persistence; no broker holdings semantics.
- Loading, empty, stale, gap, unavailable, source/provenance/as-of/coverage, units and genuine-zero remain truthful; health OK never implies market LIVE.
- Browser only same-origin FOX2 backend. No provider calls, polling storms, credentials, synthetic quote/trend/NAV/BUY-SELL or secret/error leakage.
- Tests include material negatives: 404, 409, 422, 503, Host/Origin, content-type, loopback; actual backend integration, not mocks alone.
- Typecheck, build, focused tests, relevant backend regressions, responsive browser evidence, changed-path allowlist, secret/diff checks. Map to applicable BRD-08 acceptance IDs without claiming unrelated provider tests.
- Actual test commands/exit codes and capabilities recorded; missing check = NOT_RUN/NOT_VERIFIED, never inferred PASS.

## Return
Preserve old `reports/FOX2-M1-A-APP-BATCH-B/**` evidence. Update aggregate `report.md` and `evidence_manifest.json` (with `task_id=FOX2-M1-A-APP-BATCH-B`), and add sanitized new evidence under `evidence/native-r4-20261023/**`. If unable to run, report exact blocker and test status; no fake PASS. No git commit/push from Codex. Authorized OWNER_POWERSHELL_RUNNER validates path/changed-file scope and local tests before Git commit/push to `work/FOX2-M1-A-APP-BATCH-B`, returns observed REMOTE_RESULT_SHA externally; CHAT independently reviews before ACCEPT/REWORK/HOLD. Do not report DONE based on process exit 0.

STOP for dirty/drifted source, other writer, unavailable supported model/CLI/auth, sandbox errors, out-of-scope mutation, secrets/network/provider access or failing tests. Once R4 is claimed or started, never replay it; reconcile host and Git before any separate attempt.
