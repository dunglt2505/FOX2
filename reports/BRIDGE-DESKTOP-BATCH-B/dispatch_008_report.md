# FOX2 Dispatch 008 — uninstall correction certified; real recovery certification stopped

Status: **STOPPED_NEEDS_RECONCILIATION**. Dispatch 008 is consumed exactly once. Dispatches 001–007 were not replayed. **INTERNAL_FOX2_BRIDGE_READY=NO** and **BRIDGE_RECOVERED_READY_FOR_FINAL_CANARY=NO**. Real startup/Tray/Worker certification remains unfinished in addition to the final canary gates.

The immutable dispatch at `737e9851b2367f5e2aeb6597d0445b6df0ffcc71` was independently read before any mutation. Full v3 schema, Dictionary/Policy/Task/Prompt SHA-256 bindings, prompt Git blob identity, exact branch/worktree/source head `0c739db91553ab8dd39a30b221f079b9538b0836`, clean tree, remote head, prerequisites, and absence of a competing writer passed. An exclusive worktree lock was held through execution and publication. Current authorized execution used unrestricted filesystem access and approval never; 007 execution/readiness evidence was preserved. No additional Agent, prior dispatch harness, PR, main, merge, deployment, provider, broker, or LIVE execution was invoked.

## Production correction

The installer now writes stable `uninstall.ps1` and `uninstall.py` entry points directly in the Bridge root, outside `versions/**`. The PowerShell supervisor synchronously invokes the external base Python using fixed arguments, `-I -B`, and an environment without inherited `PYTHONPATH`/`PYTHONHOME`. The bootstrap accepts no arbitrary arguments, validates the current import target, loads the current Bridge package, and changes its working directory to the stable root. It never starts an installed Python process.

Uninstall from a version's Python now fails before deletion and directs the caller to the stable entry point. It does not spawn a deleting child or wait inside the deletion target. The supported Windows command is:

```powershell
pwsh -NoProfile -File "$env:LOCALAPPDATA/FOX2/AgentBridge/uninstall.ps1"
```

Deletion retains all receipt/path/link and singleton-lock checks. It verifies versions are empty and the pointer/launchers are absent before reporting `UNINSTALLED`. Sharing errors propagate; there are no blind retries, ignored deletion errors, arbitrary process kills, reboot deletion, or deferred success. Durable directories are preserved. Older automation that invokes uninstall through a version's Python must use the stable entry point. No earlier dispatch automation was executed or modified.

The successful 007 `_installation_environment()` and `_run()` isolation fix is unchanged.

## Verification and complete disposable lifecycle

- Focused invocation: **29 passed**, including 007 environment regressions, installed-interpreter refusal without spawn/wait, external bootstrap process/environment/argument bounds, completion-before-success, sharing/incomplete-deletion failures, durable 001–008 consumption preservation, and absent-startup-task idempotence.
- Full Bridge suite: **373 passed**, zero failures/errors/skips, **one invocation**, 186.02 seconds. No production or test changes followed that invocation. JUnit credential-URL fixture names were redacted without changing outcomes or counts; original and sanitized hashes are recorded.
- Two complete builds are byte-identical. Certified package SHA-256: `6d6b66b6fa8d1b986835e3bf4368a9f7a8749a37f687c79d2ed4d95d88f3d5a6`. The previously provisioned build environment was reused read-only; host tooling was not modified.
- New disposable profile: `C:\Temp\fox2-core008-a_0i_um1\user`. Parent `PYTHONPATH` and `PYTHONHOME` contamination remained deliberate throughout the lifecycle. Packaged installation subprocesses excluded both variables and retained an ordinary environment sentinel.
- Package → install → setup → repeated setup → update → normal stable installed launcher → duplicate Tray/Worker rejection → graceful exit/lock release → diagnostics → synchronous external uninstall → empty versions and removed pointer/launchers → durable preservation → exact-package reinstall → setup → fresh-process 001–008 rejection → Tray/Worker restart → diagnostics: **PASS**.
- Zero processes executing version Python were observed before uninstall. The stable bootstrap hashes, actual uninstall receipt, preserved durable-file hashes, fresh-process rejection results, and final diagnostics are recorded. The disposable run did not register a host logon task because the profile shares the host SID scheduler namespace.

Only after `isolated_summary.json=PASS` was the real root inspected or changed.

## Bounded real recovery completed before stop

The read-only inventory found two owned version identities tied to historical Dispatch 004 package evidence: the partial five-file current version `6e96ee19ea103e7bd606a63abf071d00de6fa3c6cd1663b8d9d921b01d70b3a9` and the older intact version `e4df598f1e9ffb2dc17c7f6316c62a4dc9d96c113d892340cdec407940eed4cc`. Both had matching receipts/manifests. All inspected paths were contained in the fixed root without links/junctions; remaining payload hashes matched receipts. The pointer and stable launcher were owned. No version executable process or exact SID-qualified startup task was present. The worker was STOPPED and paused.

Private durable copies and a SQLite backup were made at `C:\Temp\fox2-core008-a_0i_um1\real-preservation`; raw configuration/ledger content is not published. Original manual-consumption fields/identities were preserved, with consumed 005–008 appended. The certified package's installer code was materialized outside the version tree for reconciliation. It removed only the validated owned versions/pointer/launcher, proved versions empty, and preserved original config/log/report hashes. The exact certified deterministic package was installed. Repeated setup remained paused. Every original dispatch row retained its values, and two fresh installed processes rejected all identities 001–008 with zero pending executions.

## Mandatory stop and precise remaining state

The first real startup registration returned successfully. The harness then failed its literal action equality assertion before a second registration or any real Tray launch. Read-only diagnosis proves a **harness comparison error**: discovery returned `C:\Program Files\PowerShell\7\pwsh.EXE`, while Task Scheduler stored `C:\Program Files\PowerShell\7\pwsh.exe`. Both resolve to the same Windows executable. SID, task name, exact launcher arguments, Limited privilege, Interactive logon and IgnoreNew behavior all match. This is not evidence of an installation or task ownership defect.

The failed required assertion remains recorded; it was not erased, patched, retried, or represented as a completed certification run. No further real runtime mutation followed the stop. The real Bridge currently has the certified version installed, setup complete, intake **paused**, worker **STOPPED**, and the owned current-user startup task registered/enabled. Real installed Tray/Worker health, graceful exit/restart, final real diagnostics and complete startup certification were **NOT_RUN**. No rollback, arbitrary task deletion, or process termination was attempted.

Compatibility/binding suites passed in the full source suite, but final installed-runtime binding/compatibility certification was not reached. Exact installed Agent configuration/application and final Full Access certification are not claimed. No new immutable control-branch canary was invented; REAL_ELIGIBLE_FOX2_DISPATCH, RESULT_REMOTE_READBACK and USAGE_SNAPSHOT remain unproven. Disposable and fresh-process no-replay results do not replace the unfinished real Worker restart gate.

## Publication

Changes are confined to the installer, its focused tests, README usage guidance, this new 008 report/manifest, and `evidence/core008/**`. All 61 historical report/evidence files from the source head are preserved byte-for-byte. New files pass changed-path allowlist, secret hygiene and `git diff --check` before exact task-branch publication. The push/readback receipt is emitted after publication to avoid a self-referential commit in this report.

The first staged whitespace check flagged CRLF line endings in 16 newly generated evidence files. Only new 008 evidence was normalized to LF; `text_normalization.json` records original and normalized hashes. Counts, outcomes and semantic evidence are unchanged. The final check includes staged new files, rather than only previously tracked edits.

The published result is **STOPPED_NEEDS_RECONCILIATION**, not completed Bridge recovery or readiness. Dispatch 008 must not be rerun.
