# FOX2 — P2-01 Coding-Host DEV Readiness Precheck (READ-ONLY)

**Record status:** `AUTHORIZED_READ_ONLY_PRECHECK / CODE_ALLOWED=NO / NO_APPLICATION_MUTATION`  
**Project:** FOX2  
**WP_ID:** `FOX2-WP-M1-P2-01-DEV-READINESS`  
**TASK_ID:** `FOX2-M1-P2-01-DEV-READINESS-20261012`  
**Tracking Issue:** https://github.com/dunglt2505/FOX2/issues/9  
**Target Agent:** GitHub Copilot Pro / VS Code on FoxLe-PC  

## Authority and source binding

- Effective Policy: `FOX2_POLICY_V1.8.md`, Policy ID `FOX2-POLICY-V1`, status `RELEASED_EFFECTIVE`.
- Official Policy raw SHA-256: `226fecb094843d492e87c4768f5741726a4651b7556d5ec0abf3739e9720dd7b`.
- Verified Policy Git commit: `736863e18c43236509130c6a683b982491d2867d`.
- Git-first Task/Result Protocol: **v8**; Result Contract: **v2**.
- M1 BRD/contract source commit: `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`.
- Owner-approved Roadmap/P2 release source commit: `282fe0654de13e8d9c679e171e7ac81f29a545ca`; Git sync receipt containing commit: `ba9714b697f26172fbbcd67704698bc1aae43b70`.
- P1 bounded evidence accepted at `0dba7673ee8ad3b2d64ceabfeacce21564f3bed3`; Issue #5 closed. Do not rerun P1.

## Purpose

Observe the **current** Windows coding workspace immediately before any P2-01 DEV decision. This task is intentionally read-only. It does not implement P2-01 and does not install or modify dependencies.

## Routing decision

- R0: reuse accepted P0/P1 and released Roadmap/P2; no redo.
- R1: READ_ONLY execution-readiness precheck, not DEV.
- R2: Policy/source PASS for the precheck; `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `MERGE_ALLOWED=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO`.
- R3: Copilot is selected for this precheck because it recently operated on the actual FOX2 Windows host and can observe VS Code/worktree state directly. Actual model/mode/quota must be recorded if exposed; otherwise `NOT_EXPOSED`.
- R4: CHAT cannot inspect local Windows WIP; WORK has completed design audit; CODEX local-host access is not established. Copilot is the lowest-cost eligible observer for this host-only check.
- R5: inspect exact repo/worktree/branch/WIP and proposed future P2-01 paths; never clean or rewrite WIP.
- R6: use only the immutable source identities above and the task publication commit supplied externally by CHAT.
- R7: perform checks below, publish only the deterministic result package if report push is technically available, and STOP before any source-code mutation.

## Required current observations

On `C:\Projects\FOX2`, record sanitized evidence with UTC observation time and command exit status:

1. Host/OS, `git --version`, `python --version`.
2. `git remote get-url origin`, current HEAD, branch, `status --porcelain=v1 --untracked-files=all`, `worktree list --porcelain`, merge/rebase/cherry-pick/revert markers.
3. Count/list only paths (not contents) for ignored WIP relevant to the repository; preserve `.venv` and all user WIP.
4. Confirm current remote task/result refs and whether any unexpected writer changed them.
5. Record actual Copilot product/model/mode/quota if exposed by the UI/session. If not exposed, write `NOT_EXPOSED`; do not guess.
6. Read-only Python dependency availability: `fastapi`, `pydantic`, `jsonschema`, `pytest`, `uvicorn` via import/spec/version checks. **Do not install** anything.
7. Inspect whether any proposed future P2-01 path below already exists, is modified, untracked, ignored, owned by another task, or would collide with user work. Do not create the files.
8. Confirm the authoritative Contract/Acceptance/Roadmap/Policy files are readable at the task source commit and match the pinned identities.
9. Check report-only Git authentication by observing the designated result branch. Do not push application code. Report push may occur only after exact staged diff proves all paths are under `reports/FOX2-WP-M1-P2-01-DEV-READINESS/**`.

### Proposed future P2-01 path ownership — inspection only, not a write grant

- `backend/pyproject.toml`
- `backend/src/fox2/__init__.py`
- `backend/src/fox2/main.py`
- `backend/src/fox2/config.py`
- `backend/src/fox2/contracts/__init__.py`
- `backend/src/fox2/contracts/market.py`
- `backend/src/fox2/contracts/health.py`
- `backend/src/fox2/contracts/instruments.py`
- `backend/src/fox2/contracts/watchlist.py`
- `backend/src/fox2/validation/__init__.py`
- `backend/src/fox2/validation/schema.py`
- `backend/src/fox2/validation/semantics.py`
- `backend/src/fox2/ports/__init__.py`
- `backend/src/fox2/ports/store.py`
- `backend/src/fox2/ports/dsm.py`
- `backend/src/fox2/ports/preferences.py`
- `backend/src/fox2/api/__init__.py`
- `backend/src/fox2/api/health.py`
- `tests/p2_01/test_contract_schema.py`
- `tests/p2_01/test_semantics.py`
- `tests/p2_01/test_offline_startup.py`
- `tests/p2_01/test_security_boundary.py`

## P2-01 design subset to preserve

Acceptance IDs planned for P2-01 backend/offline evidence only:
`FOX2-00-T01, FOX2-00-T02, FOX2-00-T03, FOX2-00-T04, FOX2-06-T05, FOX2-06-T13, FOX2-06-T14, FOX2-06-T16, FOX2-06-T18, FOX2-N1-T01, FOX2-N1-T02, FOX2-N1-T03, FOX2-N1-T04, FOX2-N1-T12`.

These remain `NOT_RUN` in this precheck. Do not execute application tests beyond harmless environment/import checks. Do not claim runtime acceptance.

## Deterministic result destination

- Repository: `dunglt2505/FOX2`
- Agent result branch: `work/FOX2-WP-M1-P2-01-DEV-READINESS-copilot`
- Report: `reports/FOX2-WP-M1-P2-01-DEV-READINESS/report.md`
- Manifest: `reports/FOX2-WP-M1-P2-01-DEV-READINESS/evidence_manifest.json`
- Evidence: `reports/FOX2-WP-M1-P2-01-DEV-READINESS/evidence/**` sanitized minimum only
- Schema: `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`
- Standing report-only authority: Policy V1.8 C6F.2A, subject to actual host/Git/writer checks.
- `PR_CREATE=NO`; result commit is `PUSHED_UNREVIEWED` until CHAT independently reads it.

## Required readiness verdict

Return separately:
- `P2_01_SOURCE_READY=YES|NO`
- `P2_01_HOST_READY=YES|NO|PARTIAL`
- `P2_01_WRITER_READY=YES|NO|UNKNOWN`
- `P2_01_DEPENDENCIES_READY=YES|NO|PARTIAL`
- `P2_01_AGENT_CAPABILITY=PASS|PARTIAL|UNKNOWN`
- `P2_01_DEV_RECOMMENDATION=READY_FOR_CHAT_DEV_DECISION|REWORK|BLOCKED`

A readiness recommendation **does not grant DEV**. CHAT remains the next actor.

## STOP / forbidden

No application code edits; no dependency installation; no checkout/reset/clean/stash/rebase; no force push; no main push; no PR; no merge; no DNSE REST/WebSocket; no browser provider call; no broker/account/private data; no credential output; no raw licensed market data; no P2 runtime implementation.

If any source/policy mismatch, branch collision, unsafe WIP, unexpected remote writer, missing required repo access, or secret risk is found, STOP the affected operation and report it exactly.
