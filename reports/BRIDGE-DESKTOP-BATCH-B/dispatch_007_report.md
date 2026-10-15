# FOX2 Dispatch 007 — installer environment fixed; lifecycle stopped at uninstall

Status: **STOPPED_NEEDS_RECONCILIATION**. Dispatch 007 was consumed exactly once. No retry or replay is authorized by this result. **INTERNAL_FOX2_BRIDGE_READY=NO**. The real per-user Bridge was never inspected, repaired, launched, uninstalled, or otherwise touched.

## Binding and implementation

Dispatch was independently read from `7bac9176a24bbcbdd49f2074f88d355c5d88d906:docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-007.json` before any mutation. Dictionary, Policy, Task and Prompt SHA-256 bindings, prompt Git blob identity, full v3 schema, branch, worktree, clean initial tree and exact source/remote head `ce7a8253926b7489c79311e26d7dc75ba8c81fc6` passed. The report-only descendant relationship to the earlier code baseline was verified. The exact Core006 package SHA-256 and presence of the Bridge module inside its wheel were independently verified without executing any prior Dispatch.

A fresh bounded Codex readiness probe passed for `CODEX / PINNED / gpt-6.1-sol / high / FULL_ACCESS`, using `danger-full-access` and approval `never`. This is launch readiness evidence, not final installed dispatch certification. An exclusive worktree OS lock was held through implementation, tests, lifecycle and publication preparation; no competing material writer was observed.

Production change: one central `_installation_environment()` helper supplies a copied environment to the existing installation `_run` boundary, excluding `PYTHONPATH` and `PYTHONHOME` case-insensitively. Ordinary environment values remain intact, and the parent environment is unchanged. Venv creation, offline pip, and the isolated installed-module proof all use this boundary. Packaging format, `-I`, package/manifest verification, path ownership, ProcessLock and the existing bounded nonzero-error message remain unchanged.

## Fresh verification

- Focused installer tests: **22 passed**. New regressions cover both Python variables, case variants, actual child-process environment, preserved OS environment, unchanged parent environment, sanitized failure/rollback at each of the three install stages, and exact venv → offline pip → isolated module proof ordering.
- Full Bridge suite: **367 passed**, zero failures, one full invocation, 149.41 seconds. The complete current code was tested before packaging; no production or test code changed afterward.
- Two complete package builds: **byte-identical**, SHA-256 `58081a5fe85f7b519d352bdc398af655efc2d337d927cf6819da80859d85e642`. The already provisioned isolated build interpreter was reused read-only. The host Python environment was not modified. Package construction may acquire build wheels; installation itself uses the bundled wheelhouse with `--isolated --no-index --only-binary=:all:`.
- A new disposable profile was created at `C:\Temp\fox2-core007-sxoruwke\user`, disjoint from the real Bridge. Parent `PYTHONPATH` pointed at Bridge source; parent `PYTHONHOME` explicitly pointed at the base Python installation. Both remained present throughout the lifecycle. Observations around the packaged production installer's real subprocess calls prove both were stripped from venv, offline pip and isolated proof, with an ordinary sentinel preserved.
- Disposable install, first-run setup, repeated setup/config idempotence, update using an archive variant of the same verified payload, installed normal startup entrypoint, duplicate Tray launch, duplicate Worker lock rejection, graceful exit/lock release and sanitized diagnostics **passed**.
- The startup check used the installed launcher and single-instance behavior. Actual Windows logon-task registration was not attempted in the disposable profile because its SID-qualified scheduler namespace is shared with the host. The existing host Bridge task was confirmed absent before uninstall; no host startup task was changed.

## Mandatory stop

The first disposable installed `uninstall` command exited **2**. Its error identifies a failed installation subprocess through the existing sanitized error boundary. The evidence records exit/classification and output hashes; no unrestricted command output or credentials are published. The precise inner removal failure is **UNKNOWN**, and no root cause is asserted from this sanitized observation.

Read-only post-stop inspection of the disposable profile found the current pointer still present, one receipt-bearing update version with five files remaining, and the durable directories still present. That inventory does not establish completed uninstall or durable preservation across reinstall. There was no uninstall retry, second lifecycle attempt, expanded production fix, or additional DEV execution.

Required reinstall, durable preservation across reinstall and restart/no-replay were **not reached**. The disposable full lifecycle therefore failed. The condition authorizing real-user recovery was not met, so the real per-user runtime remains quarantined. Final installed compatibility, eligible dispatch/result, route application, usage, real startup/login and restart certification were not run. No deferred uninstall is claimed as acceptable success; **UNINSTALL_PATH=FAIL**.

Dispatches 001–006 were never replayed. Disposable setup seeded consumed identities 001–007 in its own ledger before any Worker start; diagnostics show those consumed states, and the Worker remained paused. This is not a substitute for the unreached restart/no-replay gate. Historical source reports/evidence are preserved byte-for-byte, verified against the bound base commit.

## Publication

Only `agent_bridge/src/fox2_agent_bridge/installation.py`, `agent_bridge/tests/test_installation.py`, this report, the new Dispatch 007 manifest and `evidence/core007/**` may change. Changed-path allowlist, historical byte preservation, secret hygiene and `git diff --check` are checked before publication. Delivery is restricted to `work/FOX2-BRIDGE-DESKTOP-BATCH-B`; no PR/main/merge/deploy/provider/broker/LIVE action is authorized or performed.

The initial hygiene scan flagged two credential-bearing URL fixture parameters in JUnit testcase names. Those parameters were redacted; counts and outcomes remain unchanged. `junit_redaction.json` records original/sanitized hashes and the exact scope of this evidence-only redaction. Final publication requires the sanitized artifacts to pass the scan.

The publication receipt is emitted after commit/push and exact remote readback, avoiding a self-referential commit SHA in this report. Publication does not convert the failed lifecycle into certification success. CHAT owns independent acceptance and any further recovery authorization.
