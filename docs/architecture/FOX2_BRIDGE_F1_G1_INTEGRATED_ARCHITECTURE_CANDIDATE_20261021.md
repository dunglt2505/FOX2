# FOX2 Bridge F1 — G1 integrated architecture and contract review candidate
Date: 2026-10-21 | Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Status: G1 IN_PROGRESS / DESIGN_CANDIDATE / NOT_EFFECTIVE / F1 DENY / CANARY HOLD
Inputs: Route A design 7a5af1457dd094d79d870f3eee9bc2d68e494882; F1 host authority contract in 804b2e21cd2f8793168ca24bc402e5cdcdb70b3e; offline code/test 442721769dcca2643e111b6fefc16f2a2924cc94.

## Architecture decision (candidate)
Route A: deny legacy executor execution by an independently administered Windows enforcement boundary BEFORE permitting any positive claim. Legacy binaries cannot participate in a new shared ledger protocol; therefore Route B is not selected. A mere disabled Scheduled Task, ACL editable by ordinary user, process snapshot, file lock, signed-looking JSON, local SQLite flag, or package hash is not an enforcement boundary.

### Decision pending (must close before G1 ACCEPT)
Select and verify a *deployable* Windows enforcement policy for the actual Owner host: WDAC/App Control for Business, AppLocker where supported, or an equivalently independently enforced deny/allow mechanism. Check edition/build, policy issuer, administrative ownership, script/PowerShell enforcement, copied executable and alternate-root coverage, ordinary-user tamper resistance, restart/reboot persistence, permitted current broker/worker exceptions, and recovery without re-enabling legacy. DO NOT assume these capabilities exist from PowerShell 7 or CI runner observations. Unsupported => G1 HOLD / alternative design review; no weakened positive gate.

## Trust and process separation
- Trusted Windows service runs under a principal separate from ordinary desktop user, owns exclusive claim registry and agent spawning; ordinary Bridge desktop/worker are requesters, never authority.
- Authenticated local IPC (e.g. named pipe with explicit Windows security descriptor and client identity validation), request identity bound to immutable Git task/Dispatch, approved package/source digest, epoch and owner.
- Service validates independently attested OS retirement policy identity and liveness; no authority granted by a local mutable marker or untrusted client-provided boolean.
- Global consumed-ID store must reconcile all historical roots and manual consumed markers before enabling any positive claim. Ambiguous/missing roots, in-flight uncertainty, corruption or SQLite WAL/SHM uncertainty => DENY, preserve consumed IDs.
- Service-owned durable monotonic epoch/time floor, non-replayable lease and revocation; atomic claim before spawn, no duplicate claim; loss of policy, service, lease, clock, owner, or source identity => no further claim/spawn.
- On failure/rollback only paused or deny-state current version is permissible; never return to runnable legacy or erase tombstones.

## Proposed interface contract (NOT YET IMPLEMENTED)
Request: version, dispatch_id, immutable task_sha, source_digest, package_digest, requested_actor, caller_identity, request_nonce, epoch.
Decision: DENY(reason_code) OR opaque one-use authorization scoped to exact dispatch/source/package/owner/epoch with bounded expiry.
Operations: inspect_authority (non-granting), reconcile_and_stage (privileged maintenance), claim_and_authorize_spawn (atomic), revoke (privileged), report_outcome (idempotent).
Security: server derives caller identity from OS-authenticated channel, never trusts caller_identity field alone; nonce replay rejected; all deny/error outcomes auditable without secrets. No raw token or SQLite row independently grants spawn. Claim and spawn occur under service-controlled lease; no TOCTOU between external check and ledger commit.

## Consumer and change map (scope subject to K1)
| Component | Required integration |
|---|---|
| ledger.py | Installed direct claim must fail closed unless broker-owned atomic authority path; preserve F0 negative tests |
| desktop.py / app.py | Request authenticated broker authority, no local positive bypass |
| ops_runner.py / e2e_runner.py | Same claim/spawn enforcement, no alternative path |
| f1 broker store / f1_reconcile.py | Reuse offline logic; move trusted clock, inventory closure and claim ownership to service |
| installation.py / launcher.py / Windows scripts | Signed/provenance-bound service deployment, policy verification, restart/rollback, no legacy reactivation |
| tests and package builder | Broker protocol, tamper/identity/replay/lease/crash/reboot, source provenance, Windows isolation |
This map is impact analysis, NOT a blanket file-edit authorization.

## Acceptance coverage (G1 design -> G2/G3)
A1 all installed claim paths and direct ledger calls deny without trusted broker; A2 forged receipt/IPC caller/epoch/source/package deny; A3 two roots and same dispatch concurrent -> one atomic consumed result; A4 stale/expired/revoked lease, clock rollback, service crash -> no spawn; A5 old executor and copied/alternate launcher blocked after reboot/logoff; A6 manual consumed markers and uncertain in-flight work remain consumed; A7 exact installed package, wheel and source provenance; A8 failure rolls back to DENY without legacy restart; A9 safe positive execution only in isolated Windows with verified retirement; A10 6 frozen F0 cross-root negatives and all existing regression tests preserved.
All positive host enforcement tests: NOT_RUN. CI 493 PASS/23 PASS is historical offline proof only.

## G1 unresolved material questions
1. Windows edition/build, enforcement availability and issuer/principal ownership: NOT_VERIFIED.
2. Complete legacy executable/COM/alternate entrypoint closure: PARTIAL; 118 opaque non-Exec task actions cannot be called clear.
3. Privileged service identity, named-pipe DACL, service install/update/uninstall authority: DESIGN_REQUIRED.
4. Source-bound TechSpec/BRD/acceptance reconciliation and immutable interface signatures: NOT_FULLY_VERIFIED.
5. Owner coding HOLD / route-specific host capability and PreExec: HOLD_FOR_EXECUTABLE_ONLY.

## G1 exit verdict
IN_PROGRESS / NOT_ACCEPTED. CHAT can accept G1 only after the Windows enforcement mechanism is selected against actual host capabilities and interface/consumer/acceptance contract is reconciled with authorized TechSpec/BRD. No claim of OS policy proof, service implementation, installation, or runtime permission.
NEXT_SAFE_ACTION: targeted read-only host capability evidence (not another generic discovery) plus TechSpec source/consumer validation; then issue CHAT design disposition. No host changes.
