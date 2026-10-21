# FOX2 — CHAT Phase 2 Package Lifecycle Root-Cause Review

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Phase: 2 — package lifecycle / rollback closure
Reviewer: CHAT

## Historical fact preserved

Historical Batch-B lifecycle certification recorded `UNINSTALL_PATH=FAIL` with exit 2 and did not retain the underlying stderr. Full post-stop certification remained incomplete. That historical FAIL is not relabeled.

## Current-source comparison

Accepted same-host BUILD result:
- implementation `be883bb8106ca1c058b2b34765e55c2529fe883f`;
- result/evidence `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`;
- CHAT acceptance receipt `278daa5aff70b2e17a2bf3b563cbcd2585cd2f7f`.

Observed current source:
- `agent_bridge/scripts/certify_user_lifecycle.py` is byte-identical to the historical Batch-B version and performs `results['uninstall']=cli('uninstall')`.
- The `cli` helper always invokes the installed interpreter at `<BridgeRoot>/versions/<package_sha>/runtime/Scripts/python.exe -I -m fox2_agent_bridge ...`.
- `fox2_agent_bridge.__main__.py` dispatches the `uninstall` command directly to `installation.uninstall()`; there is no forwarding layer to the stable supervisor.
- `installation.uninstall()` explicitly rejects execution when `sys.executable` is under the installed `versions` tree and raises: `installed interpreter cannot uninstall itself; run the stable Bridge uninstall.ps1`.
- Installation creates `<BridgeRoot>/uninstall.ps1` and `uninstall.py` outside `versions`, bound to an external base Python interpreter specifically to provide safe synchronous deletion on Windows.
- Current unit tests explicitly preserve this contract and verify the external stable bootstrap.

## Root cause

**PROVEN HARNESS ENTRYPOINT DEFECT**

The historical certification harness invoked the product uninstall through the exact installed interpreter that the product correctly refuses to self-delete. The observed exit 2 is therefore structurally explained by the current/historical source contract even though the old stderr was not retained.

This is not evidence that the stable external product uninstall supervisor is broken. It is evidence that the lifecycle certification used the wrong entrypoint.

## Required correction

A bounded Phase-2 coding correction must:

1. change lifecycle certification uninstall from installed `cli('uninstall')` to the stable external `<BridgeRoot>/uninstall.ps1` using PowerShell 7;
2. execute synchronously from outside `versions`;
3. capture exit code plus bounded/sanitized stdout/stderr into lifecycle evidence;
4. fail immediately on non-zero exit without hiding the sanitized diagnostic;
5. preserve config/data/logs/reports and durable consumed identities;
6. keep install/update/reinstall verification semantics;
7. add a regression proving the certification harness never invokes installed Python for uninstall and does invoke the stable supervisor;
8. keep product uninstall fail-closed self-delete guard intact;
9. perform no real install/uninstall or host mutation during the coding task.

## Verdict

Phase 2 code defect: **PROVEN**.
Route for correction: **CODEX / gpt-6.1-sol / high / MANUAL_LOCAL / FULL_ACCESS bounded to code/tests/report paths**, subject to a fresh immutable task/prompt and task-specific PreExec.

No AppLocker/service/ACL/G3/G4/Canary/main/merge/provider/broker/LIVE authority is implied.
