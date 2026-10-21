# FOX2 F1 G1 — BRD/TechSpec compatibility review and host decision gate
Date: 2026-10-21 | Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Class: CHAT read-only source review / design candidate, not a release, executable task, or permission.
Design base: d05252acf8af7d9fd44afc5f00732909527433ae.

## Resolved documentary identity
Owner governance Registry d34da1e3b4918a902646621b487ca8ad3e05b0e0 selects Policy 2.0.0, Dictionary 1.3, Routing 1.4.0 and Protocol 12 for new/re-scoped CHAT human work. Dictionary source b25f7f728de67cf8595bf24f22fcbd79ef50babc points to:
- BRD-09 v0.1 REV3 CANDIDATE: docs/brd_mirror/FOX2-BRD-09_v0.1_CANDIDATE.md, observed Git blob 99971d65ccb90874e75ace54e6a4f8ec21ba0188.
- Bridge Technical Spec v0.7 REV10 CANDIDATE: docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md, observed Git blob 5a82bd74b30f71f7b46652f67a70cd7768f68143.
These are candidates, not promoted EFFECTIVE by this review. File/blob observation alone does not prove external signer authority or installed adoption.

## Material requirement/contract gaps
| Requirement | Existing source semantics | F1 architecture implication | Verdict |
|---|---|---|---|
| BRD R11 | Bridge transports task authority decided outside Bridge; no new DEV/merge/deploy/provider/broker/LIVE permission | Windows F1 broker must enforce local execution safety, NOT grant project authorization or trading/broker rights | COMPATIBLE IF EXPLICITLY SCOPED |
| BRD R12 | Pause blocks new launches, resume does not replay | Revocation/paused gates before claim and spawn; preserve uncertain consumed records | COMPATIBLE, TEST REQUIRED |
| BRD R02/R03 | Per-user logon startup and tray | Service authority can be privileged but user-facing desktop/tray remains interactive user | DESIGN SEAM REQUIRED |
| TechSpec § runtime | Default process runs under interactive Windows user, not SYSTEM | New service must be a separate trusted authority component, not silently change entire desktop process to SYSTEM | DESIGN ADDENDUM REQUIRED |
| TechSpec § claim/replay | Local ledger/ReplayGuard protects task transitions | Cross-root global authority must own atomic claim; old direct SQLite paths must deny | CONTRACT ADDENDUM REQUIRED |
| TechSpec § permission | CHAT grants project task permission; Bridge applies exact profile | Trusted F1 service validates immutable task permissions, never creates them | COMPATIBLE IF BOUNDED |
| Host retirement | Neither candidate specifies OS-enforced legacy deny and independent issuer | Select supported mechanism and trust anchor, no self-issued receipt | MATERIAL SPEC GAP |
| Direct consumers | Desktop, app, worker, ops, E2E and direct ledger may claim/spawn | Single authenticated broker gate for every installed path | K1/TEST GAP |

## Interface decisions required to close G1
1. Distinguish project authority from OS F1 execution safety authority in all APIs, logs and user-visible statuses. Do not name privileged Windows service a trading broker.
2. Versioned protocol: dispatch/task immutable identity, source/package digest, nonce, monotonic epoch, caller OS identity, lease expiry; server derives caller identity independently.
3. Atomic global consumed-ID state with old-root reconciliation and no-replay tombstones. Positive claim must never be granted by direct ledger local flag.
4. Service-managed spawn authority: if service only returns a bearer token to unprivileged worker, a compromised worker could bypass control; define who actually creates Agent child and its Windows logon token, environment and job ownership.
5. OS retirement policy: choose based on real host Windows edition/build/administrative issuer; validate coverage for PowerShell scripts, copies, aliases, tasks/COM, manual starts, reboot, and policy tamper. A path-only rule or user-editable ACL is not enough.
6. Define service lifecycle/SCM recovery, service account least privilege, authenticated named-pipe DACL, code signing and update/rollback with denial on drift.
7. Acceptance trace: BRD R11/R12, TechSpec runtime/permissions/claim/replay, six frozen F0 negatives, all installed claim consumers, synthetic Windows tests and owner-host installed gate.

## Narrow read-only host capability evidence needed
Collect without executing Bridge, changing policy, installing service, stopping process, or reading credentials:
- Windows product name/edition/build and available OS policy providers; effective AppLocker policy availability/collection mode; WDAC/App Control policy presence and policy issuer information when readable.
- Whether the current user is admin (boolean only), service-control ability (read-only), and whether a distinct administrator/policy issuer exists (UNKNOWN until independently attested).
- Report only redacted capability booleans and provider versions; do not dump system-wide rules, SIDs, usernames, secrets or unrelated applications.
Host read-only data can select a mechanism, but does NOT attest enforcement until isolated negative tests.

## Decision
G1: IN_PROGRESS / CONTRACT_GAP. Documentary reconciliation is COMPLETE AS CANDIDATE, with material addendum gaps recorded; OS policy capability and trust anchor remain NOT_VERIFIED. No code, installation, service creation, privilege grant or Canary authorized.
NEXT_SAFE_ACTION: resolve narrowly scoped Windows enforcement capability and approve service/OS-policy seam; then CHAT issues G1 design disposition and only afterward checks separate G2 coding route.
