# FOX2 — CHAT Recovery Review — Host Lifecycle A02 PreExec v2

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Stage: TEST
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02`
Accepted source: `085cc8302e824dbccf9cbef80422ed48894b9cb4`

## Recovery verdict

**RECOVERED / HOST-SAFETY BLOCKED BEFORE MUTATION**

The Owner-host PreExec v2 reached host-state observation and stopped because exactly one `FOX2.Bridge.Desktop.exe` process existed but the accepted UI inspection seam could not find the required top-level window `FOX2 Bridge RC1`.

Observed failure:

`WPF_INSPECT_FAILED: Installed Desktop window unavailable`

No PreExec receipt was committed or pushed. No executable Dispatch exists for Host Lifecycle A02. No Agent lifecycle execution started. No Bridge package build/install/update/uninstall/reinstall, WPF exit, Worker/F1, G3/G4 or Canary mutation occurred.

Remote task branch remained at:

`39b0d5f609d629c9daa29a49751d5720e87d72bb`

The receipt path remained absent.

## Historical corroboration

Historical Host Lifecycle A01 result `9dd91becf47d934183baf147d0a4f03f4bf5933d` recorded:
- one exact-package WPF Desktop process remained after the failed certification;
- no forced termination or UI mutation was performed after that failure;
- CLI request-exit did not close the WPF presentation;
- Worker remained STOPPED and paused;
- stable uninstall was NOT_RUN.

This is consistent with the current blocked state but does not prove the currently observed process is the same PID/process instance.

## Governance boundary

Current A02 task allows optional stale-WPF cleanup only when the process is exact current package **and** the existing UI inspection seam passes.

Because UI inspection failed, A02 does not authorize graceful cleanup, force termination, install/update, uninstall or lifecycle continuation.

## NEXT_SAFE_ACTION

Run a read-only Owner-host reconciliation that records:
- current WPF PID;
- executable path;
- process start time/session/responding state;
- MainWindowHandle and MainWindowTitle;
- exact current package pointer/path comparison;
- `desktop.lock` presence/metadata;
- top-level UI Automation window names/process IDs;
- accepted UI inspect outcome.

Do not close/kill the process and do not alter Bridge state.

After CHAT reviews that evidence:
- if a valid accessible accepted WPF window exists, resume through a fresh PreExec path;
- if the process is an orphan/headless stale exact-package process, create a separately authorized bounded recovery action before any TEST mutation;
- if process identity is not exact/known, STOP and investigate provenance.

G3 remains locked.
