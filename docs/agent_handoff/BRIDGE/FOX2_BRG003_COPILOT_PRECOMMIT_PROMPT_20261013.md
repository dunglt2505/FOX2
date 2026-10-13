# FOX2 — COPILOT PROMPT BRG-003 — SOURCE BASELINE IMPORT READINESS / PRECOMMIT

Prompt ID: FOX2-BRG-003-PRECOMMIT-COPILOT-20261013-001
Priority: P0 Local Agent Bridge; task FOX2-BRG-003; Change ID FOX2-BRG-SOURCE-PRESERVATION-20261013; Stage PRE-DEV/READ_ONLY; role COPILOT (manual VS Code host observer), Agent model and thinking = OBSERVED_OR_UNKNOWN; no automatic Agent selection or quota probing.
Result: return sanitized report to CHAT; do NOT store files/commit/push via this prompt.
Owner has approved only a **standing review-event metadata** Git writer grant for the Bridge output branch. That permission does NOT cover BRG-003 code source import.
Task source authority:
- FOX2 Policy V1.8.2 RELEASED_EFFECTIVE at source-set commit `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`; Library raw SHA256 `552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc`, Git blob `0783c024d19f96a0b87ab770dad80bab449fa21f`.
- FOX2 Bridge Technical Spec v0.3 RELEASED_EFFECTIVE, Git `c9dc41b97ca8bc58f06cc2f3701832ba083422e3:docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.3.md`, blob `db38c9f0291ac3b4c6184e5a97f957a9b608f0cb`.
- v0.4 **CANDIDATE, NOT RELEASED**: Git `d712794da4a4b624592925d18c9ecb83933d200e:docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4_CANDIDATE.md`, blob `7b150ec9d5e51e76a7ed0993bf6dcfb487866af0`; use as planning delta only.
- Owner standing grant at Git `bcd78aabeaf7817b7d9b682a0180445293061f41:docs/agent_handoff/BRIDGE/FOX2_BRIDGE_STANDING_GIT_BRANCH_GRANT_20261013.md`, blob `ca2d414c0daacda1ba5a20ed963e1eb314e7cc7b`.
- Existing BRG-001/BRG-002 and reconciliation Copilot reports were already reviewed by CHAT in FOX2 Issue #10: https://github.com/dunglt2505/FOX2/issues/10 ; DO NOT rerun prior host tests/inventory or P1.

## Mandatory rules / routing (before acting)
`POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK → RESPONSE`.
R0 accept previous 20 INCLUDE/3 REVIEW_REQUIRED/55 EXCLUDE evidence as Copilot-reported; recheck only deltas from previous inventory.
R1 BRG-003 is read-only *import readiness*, NOT actual Git import.
R2 source authority v0.3 effective and v0.4 candidate; Gate A automated BLOCKED; Git output branch exists but is not code import permission.
R3 actual Copilot Pro host/model/quota/access=UNKNOWN until safely observed; no CLI workload to consume quota.
R4 consider CHAT/COPILOT/CODEX/WORK costs/fit; do not choose a DEV executor. Copilot is host inspector only now.
R5 Windows local Bridge directory, target Git checkout, WIP/locks/current writers inspected read-only; exclusive writer not presumed from clean Git status.
R6 no REPORT_PUSH requested; no code source push; no creation of branch or staging dir.
R7 return frozen precommit plan and exact blockers; STOP before mutation.

## Scope and checks — perform once, read-only

1. Independently read exact Policy/spec/grant refs above; report blob/hash match or SOURCE_UNKNOWN. No default branch substitutes.
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
- Policy/current v0.3/v0.4 candidate/grant Git full refs verification
- Previous source inventory accepted; delta 20-source-file hash table MATCH/CHANGED/MISSING/UNVERIFIABLE
- Three REVIEW_REQUIRED, secrets/PII risks sanitized, no leaked contents
- Writer and worktree status, possible Codex processes; unchanged evidence vs newly observed
- Destination branch/path/source base; collisions and WIP
- Git credentials/permissions evidence or UNKNOWN, without any write probe
- Gate table: GIT_SOURCE_READ, BRG003_CODE_IMPORT_GRANT, GIT_CODE_PUSH, WORKTREE_WRITER, GIT_EVENT_STANDING_GRANT, AUTOMATED_GATE_A, MERGE, LIVE
- One-time suggested BRG-003 allowed-paths+operation grant proposal, clear exclusion of output-event branch
- Acceptance/tests NOT_RUN, risks, STOP conditions
- Verdict `READY_FOR_OWNER_SCOPED_IMPORT_DECISION / BLOCKED / INCOMPLETE_EVIDENCE`

If evidence sufficient for BRG-003 grant, finish with a compact complete proposed one-time grant in the report for CHAT to approve. Do not self-authorize or proceed to mutate based on this prompt.

STOP: source/hash mismatch, sensitive data, unexpected process/writer activity, quota unknown triggering paid CLI probe, lack of read rights, or any operation requiring local write, Git commit/push or branch creation.
