# FOX2 Bridge F1 G1 — Windows enforcement decision candidate
Date: 2026-10-21
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Class: DESIGN CANDIDATE / NOT EFFECTIVE / NO HOST CHANGE / NO CODING AUTHORIZATION
Design base: 98ac60768db260d6f6e46635823c6525f2673e2d

## Decision
Preferred target is **signed App Control for Business (WDAC/App Control) enforced policy with Secure Boot**, issued and maintained by a trust principal that is independent of the ordinary Bridge desktop/worker principal. This is the preferred path because the F1 contract requires durable denial of legacy executable/script surfaces and tamper resistance beyond user-editable files, Scheduled Tasks, SQLite state or ordinary-user ACLs.

**AppLocker is a conditional fallback only**, not an equal default. It is admissible only when effective policy is actually supported on the Owner host; Executable/Script/Windows Installer/DLL coverage is sufficient for all legacy surfaces; the effective enforcement mode is verified; and the policy administration/distribution path is independent of the Bridge/ordinary user (for example separately administered GPO/MDM or an equivalently protected administrative boundary). A same-principal local AppLocker policy does not satisfy the independent authority requirement merely because rules exist.

If neither path meets the independent issuer/tamper-resistance requirement: **G1 HOLD; no weakened positive gate**.

## Current platform facts used for design
- Microsoft states AppLocker policy enforcement is supported on all Windows 11 editions and Windows 10 version 2004+ with KB5024351; edition name alone is therefore not a valid rejection criterion.
- Microsoft states App Control policies are effective across Windows 10/11 editions, though some PowerShell authoring cmdlets are unavailable on Home.
- Microsoft documents signed App Control policies as the strongest Windows anti-tamper option; Secure Boot is required for that signed-policy tamper protection.
- App Control deployment/version details vary by Windows build, so the actual Owner host build remains a required capability input.

References: Microsoft Learn — Requirements to use AppLocker; App Control for Business feature availability; Use signed policies to protect App Control against tampering; Deploy App Control policies using script. External documentation informs feasibility only and does not grant FOX2 authority.

## Service / OS-policy seam locked as candidate
1. Project task authority remains outside the Windows service. The F1 service validates a previously authorized immutable task/source/package identity; it never grants DEV/merge/deploy/provider/broker/LIVE rights.
2. OS policy blocks legacy executors and equivalent copied/script entrypoints before any positive F1 claim.
3. F1 service runs under a principal distinct from the interactive Bridge requester and owns the global claim namespace.
4. Client identity is derived from authenticated Windows IPC. Caller-supplied identity is advisory only.
5. Claim and actual Agent child spawn are service-owned and atomic under one bounded lease. An unprivileged worker must not receive a bearer token that independently authorizes spawn.
6. Loss/drift of OS policy, service, epoch, source/package identity, lease or clock floor denies further claim/spawn.
7. Rollback returns to DENY and preserves consumed/tombstone state. It never re-enables a runnable legacy executor.
8. Desktop/tray remains interactive-user software; only the trust/claim/spawn authority is privileged.
9. All installed direct claim paths, ops/E2E runners and ledger callers must converge on this single gate or fail closed.

## G1 host capability evidence still required
One narrow read-only observation must provide:
- Windows product/edition/version/build and architecture.
- Device Guard/App Control user-mode and kernel code-integrity enforcement status when queryable.
- AppLocker cmdlet availability plus effective collection enforcement modes, without rule bodies.
- Application Identity service read-only state.
- current token administrator boolean and read-only SCM query capability.
- Secure Boot boolean when readable.
- CiTool presence (availability only; no policy mutation).
- explicit policy_issuer_independence = NOT_ATTESTED unless separately evidenced.

The probe must not install/change policy, services, Scheduled Tasks, ACLs, registry values, Bridge state, SQLite, processes or files; output must contain no usernames/SIDs/credentials/rule bodies/command lines.

## Design acceptance rule
G1 may move to ACCEPTED only when the host evidence selects a feasible mechanism and CHAT can bind:
- preferred signed App Control path with Secure Boot + independent issuer, OR
- conditional AppLocker path with independently administered effective policy and complete legacy-surface coverage,
plus the already-defined service/IPC/global-claim/consumer/acceptance contract.

Host capability proof is not G3 enforcement certification. Actual denial/bypass/reboot tests remain G3.

Status: **G1 IN_PROGRESS / HOST_CAPABILITY_REQUIRED / F1 DENY / CANARY HOLD**.
