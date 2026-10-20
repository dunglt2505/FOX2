# FOX2 Bridge — CHAT direct offline engineering progress (F1 package provenance)

**Date:** 2026-10-21 ICT. **Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Stage:** BUILD / PACKAGE_PROVENANCE_SOURCE_AND_TEST_SUBGATES_PASS / F1_AUTHORITY_BLOCKED. **Actor:** CHAT direct-first, not CODEX/WORK Result. **Source baseline:** immutable `c3af81429b389bb3301effc96c68fbf88744aeff` containing previously accepted F0 source `611ec26c28484de740e963d86de6b00946f1492d`. **Work branch:** `work/FOX2-BRIDGE-F1-CHAT-DIRECT-INTEGRATED-20261021`. **Last code+test commit:** `ecaff9c62736560d0dc8e4606052c302ae4a4c5a`. No replay of consumed Attempt-001.

## Implemented — bounded F1 package chain dependency

1. `agent_bridge/scripts/build_user_package.py` (`NECESSARY_DEPENDENCY`): resolves all five runtime wheel versions using the exact isolated selected build interpreter, not an unrelated host interpreter. Rejects non-isolated/unproven/incomplete dependency metadata. Adds a source commit resolver refusing uncommitted packaged source paths; records `source_git_commit`, the actual `source_files` SHA-256 inventory and `wheel_source_modules` verified byte-for-byte against the staged Python modules along with existing `source_sha256` in the manifest. This is build provenance, not a signature or installed authorization.
2. `agent_bridge/tests/test_rc1_package.py` (`REQUESTED / NECESSARY_DEPENDENCY`): sixteen new negative/positive synthetic tests of isolated dependency discovery, selected build-Python/platform metadata, incomplete/host-like environments, uncommitted source, unavailable Git identity, wheel module mismatch and missing module. Does not launch installed Bridge or manipulate real ledger.
3. `.github/workflows/fox2-bridge-f1-offline-ci.yml` (`JUSTIFIED_GENERATED`): exact-branch Windows hosted isolated test, read-only checkout token, Python 3.13 syntax check, affected package tests and full current-source Bridge suite. No `main`, no broker/provider, no installation or runtime activation.

## Execution and acceptance matrix

| Gate | Exact current state |
|---|---|
| Git source/changed-path candidate | `PUBLISHED_NONMAIN / CHAT_READBACK_PASS` |
| Added automated tests | `16_NEW_CASES_COMMITTED; 23_PACKAGE_TESTS_PASS; 444_FULL_REGRESSION_PASS` |
| GitHub Actions Windows isolated test | `RUN_39512223944_COMPLETED_SUCCESS_WINDOWS; COMMIT_f035eaa147be3cae4abac66ad1a65a97978a1889` |
| Offline package archive | `NOT_RUN`; F1 claim authority is not complete so this is not a release package |
| F1 durable old-executor retirement enforcement | `NOT_IMPLEMENTED/NOT_ATTESTED`; no false positive unblocking token |
| F0 six protected negatives, historic C3/F0 | `HISTORICAL_ACCEPTANCE_PRESERVED; FRESH_444_FULL_PYTHON_TESTS_PASS_ON_f035eaa` |
| Installed module adoption, Worker lease, Canary009, Internal Ready | `HOLD / NOT_RUN` |
| Current CODEX `unelevated` write boundary | `UNSAFE_OUTSIDE_WRITE_ALLOWED`; **NO-GO** for FOX2 source coding on that host |
| CHAT acceptance of this partial candidate | `SCOPED_PACKAGE_PROVENANCE_SOURCE_TEST_PASS_ONLY; F1_FULL_BUILD_HOLD` |

This progress is an independently traceable engineering update within the same Whole-WP, **not** a new WP, Agent task/attempt, executable Dispatch, ACCEPT_BUILD or claim-authority release. Source provenance fields in a manifest do **not** prove source binaries are signed/OS-retired; actual host-based legacy retirement and lease guards are still needed before positive claims.

**NEXT_SAFE_ACTION:** preserve Windows CI pass against immutable f035eaa; do not build/install an F0-only package. Retain F0 deny. Continue integrated F1 contract/host fencing via an actually secure isolated executor with true writer restrictions. No installed Bridge, old writer, ledger or UI E2E lifecycle touched. Keep F1 Windows-installed gate separate.

## CI incident and fresh execution (no historical PASS laundering)

- Prior run `39465107989` against source `15f56336...`: **FAIL** at new package tests due to syntax corruption introduced by CHAT during a Git text splice (`pydef` and a broken `TemporaryDirectory` line); 11 failed, 7 passed, full regression SKIPPED. Failure preserved as factual evidence.
- Fresh run `39511855970` against source `ecaff9c62736560d0dc8e4606052c302ae4a4c5a`: immutable checkout and Python 3.13 install PASS; **syntax and affected package tests PASS** at last review; **full current-source Bridge regression FAILED**, 397 PASS / 4 FAIL / 43 ERROR because shallow Git checkout omitted historical source objects and the Windows owner-layout fixture was absent; this is preserved as a CI infrastructure failure, not a test PASS.
- No package archive produced; no Windows installed Bridge or legacy worker interacted with; F1 positive authority and runtime admission remain DENY/HOLD.

## Fresh immutable Windows CI evidence — PASS (2026-10-21 ICT)

- Final branch source tested: `f035eaa147be3cae4abac66ad1a65a97978a1889`; this is descendant of package/code commit `ecaff9c62736560d0dc8e4606052c302ae4a4c5a` with **only Windows CI workflow configuration amended**.
- GitHub Actions workflow run `39512223944` / Windows job `118935781394`: `completed/success`. All checkout, Python 3.13, pinned source SHA, full-history fixture, dependency install and test steps PASS.
- Actual Windows log: `23 passed in 0.30s` (affected package tests); `444 passed in 179.62s` (complete `agent_bridge/tests`); no skips/failures/errors reported in these final two test summaries. The full suite includes the existing F0 protection test file but this report does not claim Windows installed/E2E proof.
- The preceding failure against `ecaff9c` is preserved. A GitHub Actions fix changed checkout from shallow to full source history, and created an **isolated CI-only** `C:\\Projects\\FOX2` worktree for historical source-bound tests, matching the known successful runner pattern. Neither file was changed in a real Owner Windows host.
- `RESULT_CLASS = CHAT_DIRECT_BUILD_SUBGATE_SOURCE_TEST_ACCEPTANCE`, **NOT** F1 authority implementation/production package/adoption/release. Package archive `NOT_RUN`, host retirement proof `NOT_ATTESTED`, Canary HOLD.
