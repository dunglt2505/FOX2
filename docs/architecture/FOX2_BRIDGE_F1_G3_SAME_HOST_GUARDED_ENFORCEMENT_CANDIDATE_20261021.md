# FOX2 — Bridge F1 G3 Same-Host Guarded Enforcement — CANDIDATE

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`
Stage: DESIGN / BUILD REWORK BEFORE TEST
Target: Owner physical Lenovo Windows 11 Pro host only

## Trigger

Owner clarified that FOX2 will run only on the physical Lenovo Windows 11 Pro machine and no isolated VM/secondary host exists.

Historical G3 PreExec:
- receipt commit: `14a02ab5f42a7659efd2b1e60324c49ff70695b5`;
- status: `BLOCKED`;
- real blockers at that time: non-elevated shell and isolated-target requirement;
- AppLocker-module blocker was a PowerShell 7 probe false-negative and was fixed separately;
- host mutation started: false.

This receipt remains historical and is not reclassified.

## Why the isolated-host G2 policy cannot be applied unchanged

Current G2 `f1_policy.py`:
- creates Exe, Script, Msi and Dll rule collections with `EnforcementMode='Enabled'`;
- requires exact hash inventory;
- rejects path/publisher rules;
- treats unknown identities as denied in its model;
- enables service enforcement for Exe/Dll.

On a single daily-use Windows host, applying this policy unchanged would create a machine-wide allowlist for the affected collections. Required Windows and Owner applications that are not explicitly allowed can be blocked. DLL enforcement is especially unsuitable without a complete compatibility baseline because every loaded DLL can be evaluated.

Therefore direct G3 apply of the accepted isolated-host artifact is **HOLD**.

## Design decision

Adopt a **same-host guarded composite policy** for the physical Owner host.

The goal remains unchanged: F1 positive authority must fail closed and copied/retired Bridge launch paths must not bypass the privileged service. The method changes so FOX2 does not unintentionally lock the Owner out of the only host.

### D1 — Audit before Enforce

No new F1 AppLocker enforcement is applied until:
1. current local/effective policy is exported and hashed;
2. current AppIDSvc state is captured;
3. a host application compatibility baseline is collected in AuditOnly or equivalent non-blocking evaluation;
4. rollback commands/files are verified before any Enforce transition;
5. required Owner applications and FOX2 dependencies have an explicit safe coverage reason.

Audit evidence never counts as final G3 enforcement PASS.

### D2 — Exe and Script are the mandatory F1 enforcement surfaces

For same-host G3:
- Exe collection: mandatory;
- Script collection: mandatory;
- Msi collection: NOT_REQUIRED unless a concrete F1 runtime/install path needs it;
- Dll collection: NOT_REQUIRED unless audit evidence proves complete safe coverage.

Rationale: F1 service runtime integrity is additionally protected by protected ProgramData ownership/DACL checks plus exact runtime SHA-256 bindings. DLL global enforcement is not required merely because Python/native DLLs exist.

Any later decision to enable Msi/Dll requires separate compatibility evidence.

### D3 — Host-safe baseline is allowed, but broad user-writable trust is still forbidden

The composite effective policy may contain host compatibility rules that were forbidden by the isolated-host canonical subset, provided they are bounded:

Allowed baseline classes:
- Windows/SystemApps coverage;
- trusted non-user-writable Windows / Program Files locations;
- reviewed publisher rules for signed host applications;
- exact hash rules for required unsigned binaries/scripts;
- Administrator recovery allowance only when explicitly required for rollback.

Forbidden:
- broad allow of arbitrary user-writable locations;
- `C:\Users\*\*` style trust;
- unrestricted allow-all for the Owner user;
- weakening an explicit F1 deny with another allow;
- policy generated from unreviewed event-log observations alone.

### D4 — Separate host-policy identity from F1-control identity

Current single `policy_digest` is insufficient for a composite host policy.

The service/adoption plan must bind two identities:

1. `effective_policy_digest`
   - digest of the complete expected effective AppLocker policy actually deployed on this host;
   - detects host policy drift.

2. `f1_control_digest`
   - canonical digest of only the FOX2 F1 control subset;
   - covers mandatory F1 Exe/Script rules, legacy deny identities, required rule principals, service/system extension semantics and collection enforcement modes;
   - proves the F1 security boundary remains present even when host-safe baseline rules coexist.

HostFence requires both to match.

### D5 — Canonical parser must accept only reviewed baseline rule types

Rework `policy_digest()` into two validators:

- full effective policy canonicalizer:
  - supports reviewed FileHashRule, FilePublisherRule and restricted FilePathRule;
  - rejects unsupported XML/rule types;
  - preserves deterministic canonical identity.

- F1 subset canonicalizer:
  - selects only rules carrying deterministic FOX2 F1 IDs/names/metadata;
  - requires exact expected principals/actions/identities;
  - rejects missing, duplicate or conflicting F1 controls.

Path rules used by host baseline must not be accepted into the F1 control subset.

### D6 — Physical-host rollback is a first-class security gate

Before Enforce:
- export current local AppLocker XML;
- record effective-policy digest;
- record AppIDSvc start mode/status;
- record F1 service absence/state;
- record protected-root absence/state;
- generate tested rollback script;
- verify rollback script syntax and required files before policy mutation.

During G3:
- any unexpected application-control failure or inability to run rollback tooling => stop positive F1 test;
- do not continue by broadening policy ad hoc.

After G3:
- either preserve accepted same-host policy under explicit adoption state or restore prior policy exactly;
- G3 result must state which outcome occurred.

### D7 — G3 and G4 remain distinct even on the same physical machine

Same machine does not collapse evidence semantics.

- G3: temporary/bounded enforcement verification on the physical target with rollback readiness.
- G4: explicit adoption of the accepted F1 authority as the Owner's ongoing installed runtime.

G3 PASS alone does not create G4 adoption.

## Required code changes

Minimum impacted implementation:
- `agent_bridge/src/fox2_agent_bridge/f1_policy.py`
- `agent_bridge/src/fox2_agent_bridge/f1_service.py`
- policy-generation script(s)
- G3 host runner/preexec support
- focused policy/service tests
- regression tests for consumer/no-replay behavior

Expected contract changes:
- adoption plan fields: `effective_policy_digest`, `f1_control_digest`;
- host fence validates both;
- Exe/Script mandatory, Msi/Dll conditional;
- baseline rule safety validator;
- audit-to-enforce transition evidence format.

## Mandatory tests before physical-host execution

1. composite policy preserves Windows/Program Files/default host-safe coverage;
2. user-writable broad path rule is rejected;
3. missing/altered F1 deny/allow rule changes `f1_control_digest` and is rejected;
4. host baseline changes alter `effective_policy_digest`;
5. Exe/Script required collections cannot be AuditOnly at final G3 positive gate;
6. Msi/Dll may remain AuditOnly/NotConfigured only when not required by the accepted package path;
7. copied legacy executable/script remains denied by exact identity regardless path;
8. current launcher/consumer cannot bypass service;
9. HostFence denies when either digest drifts;
10. rollback artifact is generated before Enforce and validated;
11. full Bridge regression remains green;
12. no main/merge/Canary/LIVE side effect.

## Physical-host PreExec after build acceptance

A new task identity is required because target semantics materially changed.

New PreExec must verify:
- exact physical Lenovo target identity;
- PowerShell 7 elevated Administrator;
- current effective/local AppLocker export and hashes;
- AppLocker cmdlets operational;
- AppIDSvc present;
- current policy is not already unexpectedly enforcing FOX2 controls;
- rollback files generated and readable;
- exact accepted same-host code/result SHAs;
- one writer / clean worktree;
- no existing F1 authority collision;
- Owner daily-host target directive present.

The old isolated-target check is removed and must not be silently treated as PASS.

## Current verdict

`SAME_HOST_REDESIGN_REQUIRED / G3_EXECUTION_HOLD`

Current G2 BUILD remains accepted for the isolated-host design evidence that it actually satisfied. It is not revoked retroactively.

However, the physical-host-only Owner constraint exposes a compatibility gap between the accepted G2 AppLocker policy model and the only permitted runtime target.

NEXT_SAFE_ACTION:
1. publish a re-scoped same-host build task;
2. implement and test the composite policy/double-digest changes;
3. CHAT result review;
4. issue new physical-host PreExec;
5. only then perform bounded G3 enforcement on the Lenovo host.

