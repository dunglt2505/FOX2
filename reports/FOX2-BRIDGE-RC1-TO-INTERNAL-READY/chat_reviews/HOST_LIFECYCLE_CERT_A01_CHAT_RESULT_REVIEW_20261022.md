# FOX2 — CHAT Result Review — Host Lifecycle Cert A01

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001`
Result branch: `work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021`
Observed remote result SHA: `9dd91becf47d934183baf147d0a4f03f4bf5933d`

## Verdict

**CHAT_REWORK — REAL HOST LIFECYCLE FAILED BEFORE UNINSTALL**

This result is accepted as a truthful, immutable failed TEST result. It is **not** accepted as Phase-2 lifecycle certification.

The consumed Dispatch must never be replayed.

## Immutable chain

Verified:
- accepted A03 source: `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`;
- host-cert task commit: `d95f08ceed2f5a25ad288b9630ffc87b698f329c`;
- task blob: `86e0afaec6f6e47c9d15b51564a38bf5167a892b`;
- task SHA-256: `95d64b3cb3999c55700ded2a6451cd9ffa23872fb87fd00c97df7edbb8c06221`;
- prompt commit: `250c8ab15bdfd8339e6332dc105a559dbd5b3151`;
- prompt blob: `2fd33dbef3fc327ca71844b1e05670b312eefc7d`;
- prompt SHA-256: `4a3cab3096b9eca8a65938e5b36d658ceaca5e684def26524ce44cedebe1a689`;
- PreExec v5 PASS publication: `27e79ef9266760807187ce90f451ffa26bc97e2f`;
- PreExec v5 PASS receipt: `208de84f39dcf783bd4ee9053c0288cda9aa0024`;
- executable Dispatch commit: `8cac3d2798c4e3906ceac351676d32ada761056e`;
- Dispatch blob: `353ca16452d5d717ca023872a54c2eeb2f3c310b`;
- result commit: `9dd91becf47d934183baf147d0a4f03f4bf5933d`.

Remote result branch independently read back at the exact SHA supplied outside the report.

## Result ancestry and changed paths

`208de84f... → 9dd91bec...` is exactly one result commit.

Changed paths are limited to:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert/**`.

No product/source/test path changed.

K1:
- `UNEXPLAINED=0`;
- product hunks = 0.

The result therefore respected the no-code-write host-certification scope.

## Evidence integrity

CHAT independently remote-read the committed evidence and recomputed every manifest-listed SHA-256 from Git bytes:

**17 / 17 evidence hashes matched; 0 mismatches.**

Result Contract:
- contract version 2.0;
- task ID exact;
- report present;
- evidence manifest present;
- submission state `READY_FOR_CHAT_REVIEW`;
- allowlist/diff/secret/K1 checks report PASS.

## Real host lifecycle observations

The package stage succeeded:
- exact accepted-source package built once;
- package SHA-256 `52007843327db63acb0c7908f06ba33378404686f03b6f81d07178de4c2f16d4`;
- package manifest source commit exactly `2faa33f9...`;
- package provenance/hashes verified before host mutation;
- supported `install_user.ps1` returned exit 0 / UPDATED;
- installed pointer and receipt bind the exact package/source;
- pre-certification host state was STOPPED, paused=true, setup_complete=true.

The real lifecycle invocation then failed once:

`RuntimeError: installed tray/worker did not become healthy`

at `certify_user_lifecycle.py:133`.

Observed counters:
- lifecycle attempts = 1;
- lifecycle retries = 0;
- stable uninstall attempts = 0;
- reinstall attempts = 0;
- recovery attempts = 0.

No retry occurred.

## Independently verified source-contract mismatch

CHAT reviewed the accepted source at `2faa33f9...`.

`certify_user_lifecycle.py` currently requires, within 45 seconds:
- control state `PAUSED`;
- non-empty Worker heartbeat;
- exactly one `pwsh.exe` process whose command line contains `desktop_tray.ps1`.

The same accepted source has a different Desktop launch architecture:
- `desktop_launcher.ps1` invokes `fox2_agent_bridge.launcher`;
- `launcher.py` explicitly states presentation never starts or owns the Worker;
- `launcher.launch()` starts the WPF `FOX2.Bridge.Desktop.exe` presentation only and returns `worker_started=False`;
- WPF `MainViewModel` reads and controls Worker state via the control API; it does not itself become the Worker or a legacy PowerShell tray.

Therefore the current lifecycle health gate is incompatible with the accepted current Desktop launcher architecture.

This is a real source/test contract regression. It is not an uninstall failure and not evidence that the WPF presentation itself is healthy enough for Phase-2 certification.

## Preserved FAIL / NOT_RUN matrix

PASS:
- accepted-source package build provenance;
- package hash/manifest verification;
- durable pre-state snapshot;
- exact real install/update;
- installed pointer/receipt;
- safe paused pre-state;
- final pointer exact;
- consumed identity preservation;
- no replay;
- no G3/G4/AppLocker/service/ACL mutation;
- allowlist/secret/diff/K1/Result Contract.

FAIL:
- corrected real lifecycle certification;
- final required runtime health.

NOT_RUN:
- stable external uninstall;
- uninstall exit-zero gate;
- post-uninstall pointer/version absence;
- across-uninstall durable-state preservation;
- same-package reinstall.

Historical Batch-B uninstall FAIL remains historical and is not overwritten by this result.

## Final host state

At result observation:
- exact new package remains installed;
- Worker state STOPPED;
- paused=true;
- setup_complete=true;
- no active dispatch;
- durable config/database/manual-consumption hashes preserved across the actual install/failed-run window;
- database quick_check=ok;
- one WPF Desktop presentation process remained open;
- startup remained enabled / scheduled task Ready.

Across-uninstall preservation is still NOT_RUN because uninstall was never reached.

## Acceptance decision

The A01 result is **not accepted as successful TEST certification**.

**CHAT_REWORK** is required because the accepted source contains an internal launcher/lifecycle acceptance mismatch that prevents the real lifecycle test from reaching uninstall/reinstall.

No G3/G4/Canary progression is authorized.

## NEXT_SAFE_ACTION

Create a fresh source-rework task from immutable result/source evidence.

The rework must first establish the authoritative current Desktop/Worker lifecycle contract, then change the minimum source/test surface so that:
1. current launcher architecture and lifecycle health checks describe the same runtime model;
2. real WPF presentation identity is tested instead of assuming legacy `desktop_tray.ps1`, if the current architecture is authoritative;
3. Worker-start/heartbeat ownership is explicit and tested;
4. graceful-exit semantics account for WPF presentation lifecycle;
5. regression tests cover no legacy-tray false requirement;
6. no G3 authority is introduced.

After source rework is CHAT-accepted, issue a **new** current-package host lifecycle certification identity and rerun the real lifecycle from install through uninstall/reinstall exactly once.

The consumed A01 Dispatch must never be replayed.
