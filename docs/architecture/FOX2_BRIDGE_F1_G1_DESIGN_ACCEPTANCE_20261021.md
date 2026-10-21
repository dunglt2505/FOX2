# FOX2 Bridge F1 — G1 Design Acceptance
Date: 2026-10-21
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Feature: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION
Disposition: CHAT ACCEPT — DESIGN ONLY
Effect: G1 ACCEPTED; G2 remains separately BLOCKED; no runtime authorization

## Source set reviewed
- Integrated plan/tracker: 98ac60768db260d6f6e46635823c6525f2673e2d and later tracker updates on the same non-main branch.
- Integrated architecture candidate: d05252acf8af7d9fd44afc5f00732909527433ae.
- BRD/TechSpec compatibility review: 62be753a775b2bb59538213d3738f3e239af38cf.
- Windows enforcement decision candidate: f15f8efba214d0f5a3ca51304ff5127d293356cc.
- Owner host capability intake: 21f9b36159c020f60efd4468abc7c6b284c9e3e6.
- F1 host authority contract: reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/f1_host_authority_contract.md.

## Correct stage boundary
G1 DESIGN must not require the host policy to already be installed or enforced, because that would collapse G1 into G3/G4 and violate the Whole-WP gate order. Therefore the prior candidate sentence requiring an 'effective independently administered AppLocker policy' before G1 acceptance is superseded for DESIGN by this rule:

**G1 requires a verified deployable host mechanism, locked administrative/trust boundary, protocol/consumer contract and testable acceptance. G3 proves isolated enforcement. G4 proves Owner-host installed adoption.**

This correction does not weaken any runtime safety condition: until G3/G4 evidence exists, F1 positive authority remains DENY.

## Locked Windows enforcement baseline
### Baseline for G2 build: AppLocker enforced policy boundary
AppLocker is selected as the F1 OS fence baseline for this actual host because the Owner-host observation confirms:
- Windows 11 Pro host and AppLocker policy cmdlet availability.
- Application Identity service exists.
- Get-AppLockerPolicy -Effective returns successfully.
- the observed interactive token is not administrator.

The current host has no effective AppLocker rule collections and AppIDSvc is stopped. That is EXPECTED to remain non-enforced at G1 and must not be called PASS. G3/G4 must explicitly configure and verify enforcement under separate authorization.

Signed App Control for Business remains an optional stronger hardening path, not a prerequisite for G2. Secure Boot is currently UNKNOWN because its cmdlet failed in a non-elevated probe. Avoiding a signed-policy dependency at G1 also avoids introducing a boot-recovery/key-management obligation before isolated testing.

### Required AppLocker policy properties
1. Policy administration must require an elevated Windows administrative principal outside the ordinary Bridge requester token. The Bridge desktop/worker/service requester cannot edit the policy.
2. Use explicit Enforce rules mode, never Audit-only, for every collection relied upon by F1.
3. Cover executable and script legacy surfaces at minimum; Windows Installer and DLL collections are included when package/runtime inventory shows they are executable dependencies or bypass surfaces.
4. Copy/alternate-root closure uses publisher or exact file-hash identity where available; path-only deny is insufficient for legacy artifacts that can be copied.
5. Prefer allow-by-current-approved identity plus explicit legacy denies/exception closure over broad path trust. Exact rule material is generated only after G2 inventory and is tested in G3.
6. AppIDSvc must be running/enforcing before any positive claim on a target host; stopped/unreadable/drift => DENY.
7. Service/non-user process enforcement must be enabled where F1 service or protected launch surfaces require it; Windows system code must remain explicitly allowed.

## Locked trusted-service boundary
1. F1 authority component is a Windows service under LocalSystem (or an equivalently privileged dedicated service account accepted during implementation review); desktop/tray remains interactive-user software.
2. The service owns the global consumed-ID/epoch store in a protected ProgramData location writable only by the service/administrators.
3. Named-pipe IPC uses an explicit DACL and derives caller identity from the OS-authenticated pipe/token. Caller-provided identity fields never confer trust.
4. Project task authority remains external to the service. The service only validates immutable task/source/package/actor scope already authorized by CHAT/Git governance.
5. Claim and Agent child creation are one service-owned operation under a bounded lease. The unprivileged requester never receives a bearer capability that permits independent spawn.
6. To preserve the interactive user's Agent credentials/environment, implementation may duplicate the authenticated caller token and use a service-owned CreateProcessAsUser-equivalent spawn; the service remains the creator/owner of the authorization decision and job lifecycle.
7. Service startup creates a new authority epoch; all pre-restart leases become invalid. Claimed/uncertain dispatch IDs remain consumed and are never replayed.
8. Policy drift, AppIDSvc loss, source/package mismatch, epoch mismatch, lease loss, clock rollback or service-store ambiguity fail closed.

## Locked interface contract
Request fields: protocol_version, dispatch_id, immutable_task_sha, source_digest, package_digest, requested_actor, request_nonce, epoch.
Server-derived context: caller OS identity/session, active policy identity/status, authority epoch, service boot instance.
Operations: inspect_authority (non-granting); reconcile_and_stage (privileged); claim_and_spawn (atomic); revoke (privileged); report_outcome (idempotent).
Decision: DENY(reason_code) or internal one-use service authorization immediately consumed by service-owned spawn; no reusable client bearer token.

## Consumer closure required in G2
- ledger.py: no positive installed direct claim without F1 service.
- desktop.py/app.py: requester only; no local bypass.
- ops_runner.py/e2e_runner.py: same service gate.
- f1 broker/reconcile logic: reuse offline reconciliation semantics but move trusted claim/epoch/lease ownership to service.
- installation.py/launcher.py/Windows scripts: install service/policy support only under separately authorized host route; rollback returns to DENY and never resurrects legacy.
- package/tests: protocol, identity, tamper, replay, lease, crash, reboot, policy-loss, copied legacy and direct-consumer tests.

## Acceptance trace
A1 every installed claim/spawn path denies without service + active OS fence.
A2 forged caller/source/package/nonce/epoch deny.
A3 cross-root same dispatch concurrency produces one global consumed result.
A4 stale/revoked lease, service crash/restart and clock rollback produce no new spawn.
A5 legacy executable/script copies and alternate roots are blocked by the selected AppLocker policy in isolated Windows.
A6 manual consumed markers and uncertain/in-flight histories remain consumed.
A7 exact package/source provenance is bound before positive execution.
A8 rollback returns to DENY with tombstones preserved and no legacy reactivation.
A9 positive execution is first demonstrated only in isolated Windows after OS fence verification.
A10 frozen F0 negatives and existing regression suites remain preserved.

## G1 disposition
STAGE=DESIGN
STATUS=ACCEPTED
EVIDENCE=CHAT_ACCEPTED_DESIGN_WITH_OWNER_HOST_CAPABILITY
EXIT_GATE=MET_FOR_DESIGN_ONLY
BLOCKER=NONE_FOR_G1
NEXT_SAFE_ACTION=G2_ENTRY_REVIEW: re-resolve source/task/routing/coding authority, preserve explicit coding HOLD unless separately lifted, then bind one integrated build task if authorized.

Preserved runtime state: F1=DENY; G3=NOT_RUN; G4=NOT_RUN; Canary009=HOLD; INTERNAL_FOX2_BRIDGE_READY=NOT_ATTESTED.
