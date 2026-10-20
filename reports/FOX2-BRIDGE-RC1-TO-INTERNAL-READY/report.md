# FOX2 Bridge — CHAT direct offline engineering progress (F1 package provenance)

**Date:** 2026-10-21 ICT. **Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Stage:** BUILD / PARTIAL_SOURCE_CANDIDATE / TEST_RUNNING_OR_QUEUED. **Actor:** CHAT direct-first, not CODEX/WORK Result. **Source baseline:** immutable `c3af81429b389bb3301effc96c68fbf88744aeff` containing previously accepted F0 source `611ec26c28484de740e963d86de6b00946f1492d`. **Work branch:** `work/FOX2-BRIDGE-F1-CHAT-DIRECT-INTEGRATED-20261021`. **Last code+test commit:** `15f56336e3ec6ea207f8383d406eaae7810dd257`. No replay of consumed Attempt-001.

## Implemented — bounded F1 package chain dependency

1. `agent_bridge/scripts/build_user_package.py` (`NECESSARY_DEPENDENCY`): resolves all five runtime wheel versions using the exact isolated selected build interpreter, not an unrelated host interpreter. Rejects non-isolated/unproven/incomplete dependency metadata. Adds a source commit resolver refusing uncommitted packaged source paths; records `source_git_commit` and the actual `source_files` SHA-256 inventory along with existing `source_sha256` in the manifest. This is build provenance, not a signature or installed authorization.
2. `agent_bridge/tests/test_rc1_package.py` (`REQUESTED / NECESSARY_DEPENDENCY`): eleven new negative/positive synthetic tests of isolated dependency discovery, incomplete/host-like environments, uncommitted source and unavailable Git identity. Does not launch installed Bridge or manipulate real ledger.
3. `.github/workflows/fox2-bridge-f1-offline-ci.yml` (`JUSTIFIED_GENERATED`): exact-branch Windows hosted isolated test, read-only checkout token, Python 3.13 syntax check, affected package tests and full current-source Bridge suite. No `main`, no broker/provider, no installation or runtime activation.

## Execution and acceptance matrix

| Gate | Exact current state |
|---|---|
| Git source/changed-path candidate | `PUBLISHED_NONMAIN / CHAT_READBACK_IN_PROGRESS` |
| Added automated tests | `11_NEW_CASES_COMMITTED; EXECUTION_NOT_YET_ATTESTED` |
| GitHub Actions Windows isolated test | `RUN_39465107989_QUEUED_AT_LAST_CHECK`; later result must be independently read |
| Offline package archive | `NOT_RUN`; F1 claim authority is not complete so this is not a release package |
| F1 durable old-executor retirement enforcement | `NOT_IMPLEMENTED/NOT_ATTESTED`; no false positive unblocking token |
| F0 six protected negatives, historic C3/F0 | `HISTORICAL_ACCEPTANCE_PRESERVED`; fresh regression not yet attested |
| Installed module adoption, Worker lease, Canary009, Internal Ready | `HOLD / NOT_RUN` |
| Current CODEX `unelevated` write boundary | `UNSAFE_OUTSIDE_WRITE_ALLOWED`; **NO-GO** for FOX2 source coding on that host |
| CHAT acceptance of this partial candidate | `PENDING_AUTOMATED_TEST_EVIDENCE` |

This progress is an independently traceable engineering update within the same Whole-WP, **not** a new WP, Agent task/attempt, executable Dispatch, ACCEPT_BUILD or claim-authority release. Source provenance fields in a manifest do **not** prove source binaries are signed/OS-retired; actual host-based legacy retirement and lease guards are still needed before positive claims.

**NEXT_SAFE_ACTION:** independently read the Windows workflow run and fix real failures only within scoped code/test; retain F0 deny. Continue integrated F1 contract/host fencing via an actually secure isolated executor with true writer restrictions. No installed Bridge, old writer, ledger or UI E2E lifecycle touched. Keep F1 Windows-installed gate separate.
