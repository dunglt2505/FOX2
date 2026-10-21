# FOX2 Bridge — Downstream Readiness Pack while CODEX quota is constrained

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Class: CHAT DIRECT READ-ONLY / CANDIDATE PREPARATION
Execution authorization: NONE
Host mutation: NONE
Agent execution: NONE

## Purpose

Use the period before the published Package Lifecycle A01 CODEX Dispatch is launched to prepare all non-CODEX downstream work without consuming the one-shot Dispatch or creating competing code writers.

Current Package Lifecycle A01 state:
- source code base: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`;
- task: `31caeb95ceb6d50644722527252f714a4406ab97`;
- prompt: `56f3a8058d5e2083e6190b180ff0181b97e259bb`;
- PreExec PASS receipt: `b224f029bc911c0a131342b8ac142fdd4952a96f`;
- CHAT PASS_TO_ASSIGN: `415249ccfea13d0e4022bb0c12e397029e2abdf9`;
- executable Dispatch: `f6cf96be87e50431209464d08cf5375575c0c85c`;
- Dispatch blob: `05ac5766c5e62c8a3c12ab9a2cd485f69b1ea972`;
- state: `PUBLISHED_UNCONSUMED`;
- implementation Agent started: false.

Do not replace/rebind/reissue this Dispatch while it remains valid and unconsumed.

## Work that can proceed without CODEX

### A. Phase 2 acceptance review template — prepared now

When Package Lifecycle A01 result arrives, CHAT can immediately review:

1. ancestry:
   - runtime base must be `b224f029...`;
   - implementation/result commits must be descendants without hidden rebase;
2. changed paths:
   - `agent_bridge/scripts/certify_user_lifecycle.py`;
   - permitted lifecycle/package tests only;
   - bounded report/evidence paths only;
3. harness behavior:
   - stable external `<BridgeRoot>/uninstall.ps1` is the only certification uninstall entrypoint;
   - no installed `versions/<sha>/runtime/Scripts/python.exe -m fox2_agent_bridge uninstall`;
   - synchronous external supervisor execution;
4. failure evidence:
   - exit code retained;
   - bounded sanitized stdout retained;
   - bounded sanitized stderr retained;
   - non-zero supervisor exit stops once; no retry/alternate entrypoint;
5. product contract:
   - installed-interpreter self-delete fail-closed guard remains intact;
   - product `installation.py` / `__main__.py` unchanged unless a test-driven blocker was explicitly reported;
6. tests:
   - focused harness regressions PASS;
   - installation/package regressions PASS;
   - full `agent_bridge/tests` PASS;
   - static/diff/secret/allowlist PASS;
   - K1 `UNEXPLAINED=0`;
7. result:
   - valid Result Contract v2;
   - real host lifecycle remains `NOT_RUN`;
   - historical Batch-B `UNINSTALL_PATH=FAIL` remains factual.

This checklist does not predetermine ACCEPT. Missing evidence remains HOLD/REWORK.

## B. Phase 3 G3 physical-host readiness — current findings

### Existing accepted design

Owner target:
- physical Lenovo Windows 11 Pro only;
- no VM/secondary target.

Accepted same-host constraints:
- Audit-first before Enforce;
- Exe + Script mandatory;
- MSI/DLL conditional;
- host-safe reviewed baseline;
- no broad user-writable trust;
- full `effective_policy_digest` + `f1_control_digest`;
- HostFence denies drift of either;
- rollback artifacts validated before Enforce;
- G3 and G4 remain separate.

### Source already suitable for G3 preparation

At accepted same-host source `b065a468...`:

`agent_bridge/scripts/f1_policy_artifact.py` already:
- requires an explicit reviewed baseline;
- can generate final policy + manifest;
- can generate audit policy via `transition_artifact()`;
- binds local/effective pre-enforcement snapshots;
- binds rollback artifact;
- emits `effective_policy_digest`;
- emits `f1_control_digest`;
- marks `host_compatibility=NOT_RUN_G3`;
- marks `rollback_validation=NOT_RUN_G3`;
- marks `host_mutation=false`;
- marks `adoption_authority=false`.

Therefore the same-host policy artifact layer is not the main remaining G3 design blocker.

### Existing G3 PreExec is obsolete for the physical-host route

Current:
`agent_bridge/scripts/f1_g3_host_preexec.ps1`

still explicitly represents the old isolated-host contract:
- header: `G3 isolated-host PreExec`;
- requires a virtual non-domain target;
- produces blocker `G3_ISOLATED_TARGET_UNPROVEN`;
- messages still require elevated Administrator on an isolated target;
- commit message says `record G3 isolated-host readiness`.

This script **must not be reused or synthetically treated as PASS** for the Lenovo physical-host route.

Historical G3 BLOCKED receipt remains factual.

### New physical-host G3 PreExec requirements

After Phase 2 current-package lifecycle acceptance, a new source-bound G3 identity must verify at minimum:

1. exact Lenovo physical-host identity and Owner directive;
2. elevated Administrator PowerShell 7;
3. exact accepted source/package/result SHA;
4. clean worktree / one writer / no active conflicting F1 authority;
5. current local + effective AppLocker XML exported to durable files;
6. hashes of exact snapshot bytes, not only string representations;
7. AppLocker module/cmdlets operational;
8. AppIDSvc present and exact start/status captured;
9. existing FOX2F1Authority service state reconciled, not blindly required absent;
10. existing `ProgramData\FOX2\F1Authority` state reconciled, not blindly required absent;
11. reviewed host compatibility baseline bound to immutable bytes;
12. baseline path roots checked for actual ownership/DACL/reparse-point safety on this host;
13. generated AuditOnly policy identity verified;
14. generated final Enforce policy identities verified:
    - `effective_policy_digest`;
    - `f1_control_digest`;
15. rollback script/file syntax validated;
16. rollback can run from a path that remains allowed after Enforce;
17. no policy/service/ACL mutation during PreExec itself;
18. exact STOP boundary before first mutation.

Entry verdict can only be `PASS_TO_EXECUTE_G3` after CHAT intake. PreExec PASS alone is not host mutation authority.

## C. G3 execution order — already determined

When authorized later, use this sequence:

1. **Snapshot**
   - local policy;
   - effective policy;
   - AppIDSvc start/status;
   - FOX2 service/root state;
   - accepted source/package identities.

2. **AuditOnly**
   - apply only the reviewed AuditOnly transition under explicit G3 authority;
   - collect compatibility evidence for Owner-required applications and FOX2 dependencies;
   - no positive F1 authority claim yet.

3. **Audit review**
   - no auto-generated broad allow rules from event logs;
   - every required exception must map to safe path/publisher/hash rationale.

4. **Enforce**
   - Exe + Script mandatory;
   - MSI/DLL only if Phase 2/current package evidence proves needed;
   - apply exact reviewed final policy;
   - enable/operate F1 service only within explicit G3 authority.

5. **Security tests**
   - current allowed identity;
   - retired/legacy identity denied;
   - copied identity denied;
   - alias/path-copy does not bypass;
   - forged caller denied;
   - service-only claim/spawn;
   - HostFence full-policy drift deny;
   - HostFence F1-subset drift deny;
   - revoke/crash/restart behavior;
   - no duplicate/replay after restart.

6. **Rollback**
   - deliberately test bounded rollback path;
   - prove prior policy/service state can be restored;
   - record whether G3 ends restored or leaves accepted temporary state.

No G4 adoption is inferred from G3 PASS.

## D. Phase 4 G4 adoption readiness

G4 should not be prepared as an executable task yet because its source/package identity depends on Phase 2 + G3 accepted results.

Its fixed acceptance requirements can be locked now:

- install only exact CHAT-accepted package;
- source/package manifest hashes match installed bytes;
- protected ProgramData root ownership/DACL verified;
- no user-writable/legacy executable path retains positive authority;
- accepted AppLocker policy identities match:
  - full effective digest;
  - F1 control digest;
- protected service identity/start behavior verified;
- one-shot activation;
- restart does not replay consumed Dispatches;
- revoke/crash is fail-closed;
- Tray/Worker/setup/startup still function on the installed package;
- rollback remains usable;
- installed runtime evidence is new/current, not reused from historical pre-F0 installation.

Exit:
`RUNTIME_ENFORCED=VERIFIED` for scoped Bridge runtime only.

## E. Final certification / Canary preparation

Historical Canary009 result `117812c1...` remains:
`CONSUMED_HISTORICAL_RESULT_NOT_CURRENT_ACCEPTANCE / NO_REPLAY`.

Final certification therefore requires a **new immutable final-canary identity after G4**, not a replay.

Before issuing that future identity CHAT will already have the acceptance matrix ready:

- current package lifecycle;
- current installed source/package provenance;
- real background Worker/Tray path;
- one real eligible FOX2 task;
- exact current Dispatch/Dictionary binding;
- result push + remote readback;
- usage snapshot;
- crash/restart/no-replay;
- security negative cases;
- G3/G4 receipts;
- C4/current-source final acceptance.

Only then can `INTERNAL_FOX2_BRIDGE_READY` move from `NOT_ATTESTED`.

## Critical dependency after CODEX quota returns

There is still one true critical path:

`Package Lifecycle A01 CODEX correction → CHAT result review → fresh current-package lifecycle host certification → physical-host G3 → G4 adoption → new final certification`.

Everything in this document is preparation only. It does not consume the published A01 Dispatch and does not authorize any host mutation.

## Safe work completed while waiting

- Phase 2 result-review criteria precomputed;
- current G3 source inspected;
- obsolete isolated-host G3 PreExec identified;
- same-host G3 replacement requirements locked;
- G3 execution order locked;
- G4 adoption acceptance locked;
- new-final-canary prerequisites locked.

## NEXT_SAFE_ACTION

While CODEX headroom is insufficient, preserve Dispatch `f6cf96be...` unconsumed. No additional Bridge code writer is needed.

When CODEX headroom is acceptable:
1. recheck exact task branch base `b224f029...`;
2. recheck Dispatch control head `f6cf96be...`;
3. verify no durable claim exists and one-writer is clean;
4. launch the existing A01 Dispatch exactly once;
5. CHAT immediately applies the prepared Phase 2 result-review checklist.
