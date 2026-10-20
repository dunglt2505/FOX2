# FOX2 Bridge — CHAT direct offline engineering progress (F1 package provenance)

**Date:** 2026-10-21 ICT. **Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Stage:** BUILD / PARTIAL_SOURCE_CANDIDATE / TEST_RUNNING_OR_QUEUED. **Actor:** CHAT direct-first, not CODEX/WORK Result. **Source baseline:** immutable `c3af81429b389bb3301effc96c68fbf88744aeff` containing previously accepted F0 source `611ec26c28484de740e963d86de6b00946f1492d`. **Work branch:** `work/FOX2-BRIDGE-F1-CHAT-DIRECT-INTEGRATED-20261021`. **Last code+test commit:** `ecaff9c62736560d0dc8e4606052c302ae4a4c5a`. No replay of consumed Attempt-001.

## Implemented — bounded F1 package chain dependency

1. `agent_bridge/scripts/build_user_package.py` (`NECESSARY_DEPENDENCY`): resolves all five runtime wheel versions using the exact isolated selected build interpreter, not an unrelated host interpreter. Rejects non-isolated/unproven/incomplete dependency metadata. Adds a source commit resolver refusing uncommitted packaged source paths; records `source_git_commit`, the actual `source_files` SHA-256 inventory and `wheel_source_modules` verified byte-for-byte against the staged Python modules along with existing `source_sha256` in the manifest. This is build provenance, not a signature or installed authorization.
2. `agent_bridge/tests/test_rc1_package.py` (`REQUESTED / NECESSARY_DEPENDENCY`): sixteen new negative/positive synthetic tests of isolated dependency discovery, selected build-Python/platform metadata, incomplete/host-like environments, uncommitted source, unavailable Git identity, wheel module mismatch and missing module. Does not launch installed Bridge or manipulate real ledger.
3. `.github/workflows/fox2-bridge-f1-offline-ci.yml` (`JUSTIFIED_GENERATED`): exact-branch Windows hosted isolated test, read-only checkout token, Python 3.13 syntax check, affected package tests and full current-source Bridge suite. No `main`, no broker/provider, no installation or runtime activation.

## Execution and acceptance matrix

| Gate | Exact current state |
|---|---|
| Git source/changed-path candidate | `PUBLISHED_NONMAIN / CHAT_READBACK_PASS` |
| Added automated tests | `16_NEW_CASES_COMMITTED; TARGETED_WINDOWS_CI_PASS_FULL_REGRESSION_RUNNING` |
| GitHub Actions Windows isolated test | `RUN_39511855970_TARGETED_TESTS_PASS_FULL_REGRESSION_IN_PROGRESS`; later result must be independently read |
| Offline package archive | `NOT_RUN`; F1 claim authority is not complete so this is not a release package |
| F1 durable old-executor retirement enforcement | `NOT_IMPLEMENTED/NOT_ATTESTED`; no false positive unblocking token |
| F0 six protected negatives, historic C3/F0 | `HISTORICAL_ACCEPTANCE_PRESERVED`; fresh regression not yet attested |
| Installed module adoption, Worker lease, Canary009, Internal Ready | `HOLD / NOT_RUN` |
| Current CODEX `unelevated` write boundary | `UNSAFE_OUTSIDE_WRITE_ALLOWED`; **NO-GO** for FOX2 source coding on that host |
| CHAT acceptance of this partial candidate | `PENDING_AUTOMATED_TEST_EVIDENCE` |

This progress is an independently traceable engineering update within the same Whole-WP, **not** a new WP, Agent task/attempt, executable Dispatch, ACCEPT_BUILD or claim-authority release. Source provenance fields in a manifest do **not** prove source binaries are signed/OS-retired; actual host-based legacy retirement and lease guards are still needed before positive claims.

**NEXT_SAFE_ACTION:** independently read the Windows workflow run and fix real failures only within scoped code/test; retain F0 deny. Continue integrated F1 contract/host fencing via an actually secure isolated executor with true writer restrictions. No installed Bridge, old writer, ledger or UI E2E lifecycle touched. Keep F1 Windows-installed gate separate.

## CI incident and fresh execution (no historical PASS laundering)

- Prior run `39465107989` against source `15f56336...`: **FAIL** at new package tests due to syntax corruption introduced by CHAT during a Git text splice (`pydef` and a broken `TemporaryDirectory` line); 11 failed, 7 passed, full regression SKIPPED. Failure preserved as factual evidence.
- Fresh run `39511855970` against source `ecaff9c62736560d0dc8e4606052c302ae4a4c5a`: immutable checkout and Python 3.13 install PASS; **syntax and affected package tests PASS** at last review; **full current-source Bridge regression IN_PROGRESS**; its final count and status must be read after completion.
- No package archive produced; no Windows installed Bridge or legacy worker interacted with; F1 positive authority and runtime admission remain DENY/HOLD.
