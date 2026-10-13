# FOX2 — COPILOT PROMPT BRG-003 REV2 — RELEASE-LOCKED SOURCE BASELINE IMPORT READINESS / PRECOMMIT

Prompt ID: FOX2-BRG-003-PRECOMMIT-COPILOT-20261013-REV2
Priority: P0 Local Agent Bridge; task FOX2-BRG-003; Change ID FOX2-BRG-SOURCE-PRESERVATION-20261013; Stage PRE-DEV/READ_ONLY; role COPILOT (manual VS Code host observer), Agent model and thinking = OBSERVED_OR_UNKNOWN; no automatic Agent selection or quota probing.
Result: return sanitized report to CHAT; do NOT store files/commit/push via this prompt.
Owner has approved only a **standing review-event metadata** Git writer grant for the Bridge output branch. That permission does NOT cover BRG-003 code source import.
Source version decision (CHAT verified 2026-10-13, owner wants latest finalized release): `POLICY=1.8.2 RELEASED_EFFECTIVE`; `BRIDGE_TECHNICAL=0.4 RELEASED_EFFECTIVE`. The old prompt's `Bridge v0.3 effective / v0.4 Candidate` binding is superseded for NEW handoffs. This is a correction of an actual stale-release handoff gap, not a retroactive rewrite of accepted prior WP evidence.

**FAIL-CLOSED ACTIVE-SOURCE GATE:** Before host inspections, verify current effective release from CHAT-authenticated Library source/manifest and the exact Git refs below; do not choose by filename, version number alone, search ranking, issue comment, or moving default branch. If Library is inaccessible from Copilot, use CHAT's exact verified source-lock + published release manifest for this bounded manual task, record that Copilot cannot independently certify 'no newer Library release'. If available evidence shows a newer effective version or the source lock differs, return `BLOCKED_SOURCE_VERSION` and STOP for CHAT reissue. Candidate may inform design but not override Released/Policy. Under no condition silently fall back to v0.3.

Task source authority:
- FOX2 Policy V1.8.2 RELEASED_EFFECTIVE at source-set commit `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`; Library raw SHA256 `552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc`, Git blob `0783c024d19f96a0b87ab770dad80bab449fa21f`.
- **FOX2 Bridge Technical Spec v0.4 RELEASED_EFFECTIVE (CURRENT FOR NEW BRIDGE TASKS)**: Library `/Trading/FOX2/02_Architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4.md`, exact raw SHA-256 `8a7d5e55239c07fb32834f856fbe59b33cbc90d92768a7804c9a70236907cd9e`, 59,353 bytes. Git `36e4249d10d82e258626e3e49d796d8a8f498b8d:docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4.md`, blob `e74402d294c713a07a08b2c4e68b6caafbe2ad48`, verified exact-byte match. Read this as binding v0.4 normative design, not a Candidate.
- **v0.4 RELEASE MANIFEST (CURRENT RELEASE PROOF)**: Library `/Trading/FOX2/02_Architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4_RELEASE_MANIFEST_20261013.json`, raw SHA-256 `3ceb1f5ea1ca55dd17a1060fe36a12a317e4e3738481fca2a3456eb04abc6493`. Git `5b17d4a3947679b60403d95c558536b1af5b8e48:docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4_RELEASE_MANIFEST_20261013.json`, blob `52306026977bd649427e9ddb7b7000fb446609af`.
- Historical v0.3 RELEASED_EFFECTIVE remains immutable but **SUPERSEDED FOR NEW BRIDGE TASKS** by v0.4. v0.4 Candidate `d712794d...` is superseded by the released v0.4 exact source above; do not use Candidate as current.
- Owner standing grant at Git `bcd78aabeaf7817b7d9b682a0180445293061f41:docs/agent_handoff/BRIDGE/FOX2_BRIDGE_STANDING_GIT_BRANCH_GRANT_20261013.md`, blob `ca2d414c0daacda1ba5a20ed963e1eb314e7cc7b`.
- Existing BRG-001/BRG-002 and reconciliation Copilot reports were already reviewed by CHAT in FOX2 Issue #10: https://github.com/dunglt2505/FOX2/issues/10 ; DO NOT rerun prior host tests/inventory or P1.

## Mandatory rules / routing (before acting)
`POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK → RESPONSE`.
R0 accept previous 20 INCLUDE/3 REVIEW_REQUIRED/55 EXCLUDE evidence as Copilot-reported; recheck only deltas from previous inventory.
R1 BRG-003 is read-only *import readiness*, NOT actual Git import.
R2 v0.4 RELEASED_EFFECTIVE and Policy V1.8.2 current verified Library+manifest+Git source lock; earlier v0.3 superseded for new WPs; Gate A automated BLOCKED; standing Git event branch does not grant code import.
R3 actual Copilot Pro host/model/quota/access=UNKNOWN until safely observed; no CLI workload to consume quota.
R4 consider CHAT/COPILOT/CODEX/WORK costs/fit; do not choose a DEV executor. Copilot is host inspector only now.
R5 Windows local Bridge directory, target Git checkout, WIP/locks/current writers inspected read-only; exclusive writer not presumed from clean Git status.
R6 no REPORT_PUSH requested; no code source push; no creation of branch or staging dir.
R7 return frozen precommit plan and exact blockers; STOP before mutation.

## Scope and checks — perform once, read-only

1. Resolve Policy v1.8.2, latest effective Bridge v0.4, **release manifest** and standing grant against the exact refs above; independently read back available Git blobs and compare version/status and SHA-256. Inspect whether any newer RELEASED_EFFECTIVE artifact is known from CHAT/library. If Copilot cannot independently inspect Library, explicitly state `LATEST_LIBRARY_STATUS=CHAT_ATTESTED_NOT_INDEPENDENT` instead of claiming global latest. Exact-source failure/stale newer release is `BLOCKED_SOURCE_VERSION`; no default-branch or v0.3 fallback.
2. Inspect only **source snapshot scope** at `C:\Projects\FOX2-AgentBridge` and local FOX2 repository; never open Bridge SQLite through sqlite3 (READ_ONLY mode was observed to create `-wal/-shm`). No delete/cleanup; keep originals intact.
3. Compare the 20 approved proposed INCLUDE paths against the source hashes from the BRG-002 report; report `MATCH / CHANGED / MISSING / UNVERIFIABLE` for each without printing sensitive file content. The exact 20 file paths are:
   - root `pyproject.toml`, `README.md`;
   - `src/fox2_agent_bridge/__init__.py`, `__main__.py`, `app.py`, `config.py`, `dispatch_poller.py`, `errors.py`, `hashing.py`, `ledger.py`, `logging_config.py`, `models.py`, `paths.py`, `process_lock.py`, `runtime_tools.py`;
   - `tests/conftest.py`, `test_config_paths.py`, `test_dispatch_poller.py`, `test_lock_logging_health.py`, `test_runtime_ledger.py`.
   Use BRG-002 manifest baseline expected SHA-256 if accessible from already supplied report. If full baseline is unavailable, report UNVERIFIABLE and identify missing source; do not invent expected hashes or repeat full-tree hashing. Report changed/unchanged count.
4. Inventory `config/bridge.example.toml`, `reports/BRG-010.md`, `reports/BRG-020.md` only as REVIEW_REQUIRED; identify any user-specific absolute path, account/secret/credential without quoting its value; recommend parameters or safe deferral, but DO NOT edit these files or silently sanitize before an immutable raw source snapshot. Test fixtures with fake tokens must be independently reviewed before eventual import, not classified secret-free by regex alone.
5. Verify exact denylist for any eventual source-only Git import: `.venv/**`, `data/**` (bridge.db, -shm, -wal, lock, bare control.git), `logs/**`, `.pytest_cache/**`, `**/__pycache__/**`, `**/*.pyc`, `**/*.egg-info/**`, `**/.env*`, `**/*secret*`, `**/*credential*`, and any newly discovered sensitive item. Do not modify `.gitignore` in this step.
6. Determine safe proposed destination `dunglt2505/FOX2` branch `work/FOX2-BRG-003-SOURCE-BASELINE-copilot`, target path `agent_bridge/**`, isolated worktree `C:\Projects\FOX2-worktrees\FOX2-BRG-003`; check branch collision/remote identity/owner WIP and current Writer. This is a **PROPOSAL ONLY**, not permission to create. Check whether local Git source HEAD lacks new release commits, do not mutate/fetch.
7. Distinguish grants:
   - Owner standing `work/FOX2-REVIEW-EVENTS-bridge` review-event **metadata only** (no repeat per-event approval after actual host credentials and gates are proven);
   - BRG-003 source backup **code files** requires a **separate scoped one-time WP grant** and observed host Git permissions. Once granted for BRG-003, do not request approval per commit inside unchanged authorized path/branch.
   - No merge, main push, live, production, provider, or automatic Agent launch.
8. Build deterministic BRG-003 IMPORT PLAN (not executed): source snapshot before edits; confirm SHA for 20 file allowlist; isolated staging, .gitignore and denylist; no hardcoded host paths/secrets; remote branch fast-forward push; exact remote SHA/blob/diff readback; independent 59 tests in authorized separate sandbox; no Gate A PASS inferred from missing control branch being created.
9. Return report only, no file writes, no trial push and no test run. Do NOT claim original source is backed up on Git until verified remote.

## Required report

# FOX2 BRG-003 SOURCE IMPORT PRECOMMIT READINESS
- Timestamp, actual COPILOT product/model/mode/quota evidence or UNKNOWN
- Policy V1.8.2 / active Bridge v0.4 Released / release manifest / standing grant with exact Git+Library hashes; state previous v0.3 historical only; any newer effective release evidence
- Previous source inventory accepted; delta 20-source-file hash table MATCH/CHANGED/MISSING/UNVERIFIABLE
- Three REVIEW_REQUIRED, secrets/PII risks sanitized, no leaked contents
- Writer and worktree status, possible Codex processes; unchanged evidence vs newly observed
- Destination branch/path/source base; collisions and WIP
- Git credentials/permissions evidence or UNKNOWN, without any write probe
- Gate table: SOURCE_VERSION_CURRENT, LIBRARY_RELEASE_VERIFIED_BY_CHAT, GIT_SOURCE_READ, BRG003_CODE_IMPORT_GRANT, GIT_CODE_PUSH, WORKTREE_WRITER, GIT_EVENT_STANDING_GRANT, AUTOMATED_GATE_A, MERGE, LIVE
- One-time suggested BRG-003 allowed-paths+operation grant proposal, clear exclusion of output-event branch
- Acceptance/tests NOT_RUN, risks, STOP conditions
- Verdict `READY_FOR_OWNER_SCOPED_IMPORT_DECISION / BLOCKED / INCOMPLETE_EVIDENCE`

If evidence sufficient for BRG-003 grant, finish with a compact complete proposed one-time grant in the report for CHAT to approve. Do not self-authorize or proceed to mutate based on this prompt.

STOP: any newer-effective release or evidence that source lock is stale, missing Library release/manifest/Git readback, source/hash mismatch, sensitive data, unexpected process/writer activity, quota unknown triggering paid CLI probe, lack of read rights, or any operation requiring local write, Git commit/push or branch creation.

