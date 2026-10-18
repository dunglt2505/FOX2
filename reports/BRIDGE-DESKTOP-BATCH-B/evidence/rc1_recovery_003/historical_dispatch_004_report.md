# FOX2 Bridge Desktop Batch B — Dispatch 004 WIP

Status: STOPPED_NEEDS_RECONCILIATION. BRIDGE_READY=NO. Dispatch 004 is CONSUMED; never replay. Dispatches 001/002/003 remain consumed and were not replayed.

Immutable control: `056fd4f4a2f1d99355d78f7ebf8cdc4b13109c29`. Exact clean source and remote head at launch: `9bb217d14a1689495039196cc2d695185e253baf`. Branch: `work/FOX2-BRIDGE-DESKTOP-BATCH-B`. Bound source hashes, schema, exact Codex gpt-6.1-sol / medium / Full Access, bounded current capacity, build tools, and exclusive writer lock passed. Existing PreExec receipt was reused; Shared PreExec and Batch A were not rerun.

The confirmed Tray defect was heartbeat parsing: PowerShell converts the ISO JSON heartbeat to DateTime, then implicit culture formatting makes DateTimeOffset.Parse fail on this Windows host. The timer catches the error before reaching its shutdown condition, even though Worker is STOPPED with stop_requested=true. A diagnostic trace observed this exact failure. Only the owned diagnostic Tray was terminated after Worker stopped.

The narrow correction handles typed and string heartbeat values without culture-dependent reparsing, checks completed Worker shutdown before optional UI formatting, drains both control pipes concurrently, bounds control waits, and disposes the owned control process. No Worker, Agent dispatch, or replay business logic changed. Lifecycle certification now verifies released Worker lock and preserves consumption of 004 alongside 001–003. All 17 restored files remain; 15 are byte-identical and only Tray and lifecycle certification were narrowly edited. Five focused regressions passed in 12.58 seconds. An initial test command omitted PYTHONPATH and failed before collection; the configured focused run passed.

Two offline package builds had identical SHA-256 `6e96ee19ea103e7bd606a63abf071d00de6fa3c6cd1663b8d9d921b01d70b3a9`. Baseline per-user installation and fixed-package update succeeded. Installed certification passed setup, Limited interactive startup registration, two-launch single Tray/Worker behavior, rejected second Worker, graceful Tray exit with STOPPED state and released Worker lock, support export, and startup disable.

Certification then failed at installed `uninstall`: exit 2. The helper reports only the exit code; its captured stderr was not retained. The underlying uninstall cause is UNKNOWN. The incomplete lifecycle run did not write its final success JSON. No reinstall or further test/repair was attempted. Full pytest was NOT_RUN because the mandatory immediate STOP condition takes precedence. The 24 gates are individually recorded; full certification is incomplete.

Read-only inspection after STOP found Worker STOPPED, startup task absent, all four dispatches NEEDS_RECONCILIATION, and installation pointer plus both version directories still present. Runtime integrity after the failed uninstall is UNKNOWN. Do not restart or automatically retry; return to CHAT for reconciliation and fresh authorization.

This publication contains authorized WIP code and truthful evidence only. No PR, main, merge, deployment, provider, broker or LIVE action. PUSHED_UNREVIEWED, if remote readback succeeds, describes WIP publication only and does not imply acceptance or readiness. Only CHAT can accept INTERNAL_FOX2_BRIDGE_READY.
