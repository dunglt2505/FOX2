# FOX2 P1 Final Evidence Delta

Project: FOX2
WP: FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY
Policy: FOX2 Policy V1.7.1
This file records the bounded E01-E04 verification only. It does not recreate
the original P1 logs and contains no raw OHLCV values, credentials, or account
data.

## E01 — Current Windows, toolchain and FOX2 Git state

Observed at `2026-10-12T09:18:07Z` on `FoxLe-PC`.

| Command | Result | Exit |
|---|---|---:|
| `hostname` | `FoxLe-PC` | 0 |
| `[Environment]::OSVersion.VersionString` | `Microsoft Windows NT 10.0.26300.0` | 0 |
| `git --version` | `git version 2.56.0.windows.1` | 0 |
| `python --version` | `Python 3.13.15` | 0 |
| `node --version` | command unavailable (`CommandNotFoundException`) | unavailable |
| `npm --version` | command unavailable (`CommandNotFoundException`) | unavailable |
| `git -C C:\Projects\FOX2 rev-parse HEAD` | `906adba0450781d1f8b05b0e9d471acf8a684f68` | 0 |
| `git -C C:\Projects\FOX2 branch --show-current` | `work/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY-copilot` | 0 |
| `git status --porcelain=v1 --untracked-files=all` | empty; no tracked/untracked changes | 0 |
| `git worktree list --porcelain` | one local worktree at `C:\Projects\FOX2`, same HEAD and branch | 0 |
| `git remote get-url origin` | `https://github.com/dunglt2505/FOX2.git` | 0 |
| ignored-file inventory | 1,109 ignored paths, all rooted under `.venv`; not inspected or modified | 0 |
| merge/rebase/cherry-pick/revert markers | none present | 0 |

At `2026-10-12T09:17:29Z`, the remote result branch also resolved to
`906adba0450781d1f8b05b0e9d471acf8a684f68`. The local working tree remained
clean at the time of this observation. The ignored `.venv` is preserved.
After capturing E01, this report-only amendment created changes to the three
allowlisted paths; those changes are not staged in the captured baseline.
A GitHub server-side lease is not exposed, so exclusive
remote writer ownership cannot be independently asserted beyond the unchanged
expected remote HEAD and sole known local worktree.

## E02 — FOX source parity and inspected patterns

Observed at `2026-10-12T09:18:49Z`. Local `C:\Projects\Fox` is on `master` at
`27fb4d643a9a27f9db80ae285f39622dff6c19ab`, with a clean tracked/untracked
status. The pinned reference is `dunglt2505/Fox` commit
`740051933ec4fbf29180d0f5fb698c34e8c91ece`. For each named file, SHA-256 is
computed from local filesystem bytes and from `git show <pinned-sha>:<path>`.
All four raw byte streams compare equal; there is no line-ending-only delta.

| File | Local SHA-256 | Pinned SHA-256 | Result |
|---|---|---|---|
| `fox/dnse.py` | `e27a67cfa133ee3da675dd7683f47343882f805dde6240aab788146d46a797ef` | `e27a67cfa133ee3da675dd7683f47343882f805dde6240aab788146d46a797ef` | `PASS`, byte-identical |
| `fox/market_store.py` | `012547de1c6eba719a862217d23788ddf00a72b4b78926cf02ddd10977663c11` | `012547de1c6eba719a862217d23788ddf00a72b4b78926cf02ddd10977663c11` | `PASS`, byte-identical |
| `fox/market_calendar.py` | `ef805eeb305b2fdd1ac2b5054f23f391405c6366ef7df123e40e337392584eb5` | `ef805eeb305b2fdd1ac2b5054f23f391405c6366ef7df123e40e337392584eb5` | `PASS`, byte-identical |
| `fox/app.py` | `0a9499030ad268bad0d656dd1a4e91704f0de581502729d05f708150cf57f2ae` | `0a9499030ad268bad0d656dd1a4e91704f0de581502729d05f708150cf57f2ae` | `PASS`, byte-identical |

Observed source support:

- `fox/dnse.py:1,57-68`: explicitly GET-only; `client.get`; records SHA-256 of
  raw response bytes before semantic handling. No WebSocket implementation
  was observed in the four-file scope.
- `fox/market_store.py:18-32,43,63-68`: validates aligned OHLC arrays and
  monotonic timestamps, preserves native units as unverified, records
  request-window/pagination limits, reloads cache as stale, and records
  last-success metadata.
- `fox/market_calendar.py:9,22-35,128-149`: explicitly uses
  `Asia/Ho_Chi_Minh`; unknown timestamp semantics and unverified calendar
  coverage remain UNKNOWN.
- `fox/app.py:40-41,99-109,139-159`: serves static UI through the backend and
  exposes market/dashboard APIs; offline loading uses an adapter and synthetic
  account/sample values are labelled separately from the DNSE source.

This is pattern evidence only. No FOX code was copied or modified. Relevant
FOX2 mapping: provider/data provenance, stale/unknown and timestamp semantics
to BRD-06; backend-mediated dashboard/API and clear sample/live separation to
BRD-08.

## E03 — Existing market-cache metadata only

Observed at `2026-10-12T09:18:50Z`; cache path:
`D:\Data\Fox\market\production\cache\snapshot.json`.

- File exists; 46,639 bytes; last filesystem modification:
  `2026-10-08T09:15:02.0476868Z`.
- Root reports environment `production`; no schema/version field is recorded.
- Root last attempt: `2026-10-08T09:14:56.322431+00:00`.
- Seven symbol entries: `VNINDEX`, `VN30`, `ACB`, `HPG`, `FPT`, `SSI`, `MWG`.
- Each entry records 40 bars, first timestamp `2026-08-10T02:00:00+00:00`,
  last timestamp `2026-10-07T02:00:00+00:00`.
- Per-entry last-success timestamps range from
  `2026-10-08T09:14:57.100614+00:00` (VNINDEX) through
  `2026-10-08T09:15:02.045562+00:00` (MWG). Stored entry status is `fresh`,
  but the cache is about 4 days old at observation and is therefore classified
  stale for current use.
- Recorded source metadata says `DNSE production`; units are
  `UNVERIFIED_NATIVE`, adjustment `UNVERIFIED`, bar finality
  `UNVERIFIED_NO_ANALYSIS`, completeness `REQUEST_WINDOW_ONLY`.
- The current file therefore confirms 7 x 40 for this specific snapshot only.
  The historical Git audit recorded by CHAT in Issue #5 at the pinned FOX
  commit reports 7 x 39. No matching older cache snapshot was found here;
  the difference remains unreconciled and neither count substitutes for the
  other.
- No provider endpoint was called. No bar values were emitted or committed.
  DNSE read/redisplay/retained-use rights and retention terms remain
  `NOT_VERIFIED`.

## E04 — Readiness decision

| Area | Status | Evidence / remaining gate |
|---|---|---|
| Windows/toolchain | `PARTIAL` | Windows, Git and Python observed; Node/npm unavailable. No installation performed. |
| FOX2 repository / worktree | `PARTIAL` | Correct report branch, pinned expected HEAD, clean tracked/untracked tree, one known worktree; 1,109 ignored `.venv` paths preserved; no remote lease API. |
| Legacy FOX parity/patterns | `PASS` for four named files | Raw bytes match pinned commit for exactly the requested files. Read-only pattern evidence only; no code reuse. |
| Local DNSE cache | `PARTIAL` | Snapshot metadata observed, 7 x 40; stale, incomplete provenance and historical 7 x 39 discrepancy; rights unknown. |
| M1 v0.4 source binding | `PASS` for source identity only | Pinned FOX2 source manifest/receipt identifies source commit `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`; receipt reports 10/10 remote source/companion readbacks. This does not grant DEV or runtime readiness. |
| M1-A offline DSM/API readiness | `PARTIAL / NOT_AUTHORIZED` | Source contract and sample/stale/unknown semantics are available for design. Still needs a fresh authorized WP/DEV grant, exclusive file ownership, offline-only provider-disabled fixtures, deterministic tests, and validated provenance/quality handling. Node/npm absence blocks frontend build until separately provisioned. |
| M1-B DNSE real-data readiness | `BLOCKED` | Data read/redisplay/retained-use rights, retention, and provider authorization are not verified. Production access was not attempted and is not authorized here. |
| 105 M1 acceptance cases | `NOT_RUN` | As recorded in current Issue #5, these belong to later milestones, not a blanket P1 acceptance gate. |

Current Issue #5 state, read during this session: CHAT has
`RESULT_DELIVERY_VERIFIED=YES` and `P1_ACCEPTANCE=ACCEPTED_PARTIAL` for recovery
and evidence review only. `P1_FULL_READINESS=OPEN`; original logs remain
`NOT_RETAINED`; no DEV/P2/P3/Production/merge/LIVE permission follows.

## Result timestamp and prior push probes

- The prior manifest's `submitted_at_utc=2026-10-12T08:51:48Z` predates the
  pending-update push dry-run at `2026-10-12T08:54:47Z` and the prior result
  commit. Treat the old value as the earlier draft timestamp, not as the time
  of completed delivery. This amendment has a new manifest timestamp.
- The earlier no-op
  `git push --dry-run origin <task-commit>:refs/heads/<result-branch>` did run
  at `2026-10-12T08:45:45Z` and returned `Everything up-to-date`; it had no
  pending ref update and did not test write permission. Its earlier
  classification as `NOT_RUN` described the permission test, not command
  execution. A later pending-update dry-run at `08:54:47Z` proposed the
  expected fast-forward, and a subsequent actual push of the prior report
  commit succeeded. These prior immutable facts are not overwritten.
