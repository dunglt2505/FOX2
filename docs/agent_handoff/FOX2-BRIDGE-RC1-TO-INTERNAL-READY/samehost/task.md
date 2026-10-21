# FOX2 — Same-Host Guarded Policy BUILD Task

Task ID: `FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`
Stage: BUILD REWORK
Role: CODEX — Primary implementation
Model: `gpt-6.1-sol`
Thinking: HIGH
Execution: MANUAL_LOCAL / PowerShell 7+ / one attempt after fresh PreExec PASS

## Owner target decision

Owner statement:
> máy của ông chủ physical Lenovo Windows 11 Pro và chỉ chạy trên máy này

Recorded at:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/owner_directives/G3_PHYSICAL_HOST_ONLY_TARGET_20261021.md`
commit `438169d5728a4b5b5da19b737e79db3fc6515ce0`.

Meaning: the only intended runtime target is the Owner's physical Lenovo Windows 11 Pro host. No isolated VM is available.

## Accepted design source

Same-host design candidate:
`docs/architecture/FOX2_BRIDGE_F1_G3_SAME_HOST_GUARDED_ENFORCEMENT_CANDIDATE_20261021.md`
commit `c8307980362a1ab64b93ba7d7e020d979017c849`.

CHAT design acceptance:
`docs/architecture/FOX2_BRIDGE_F1_G3_SAME_HOST_DESIGN_ACCEPTANCE_20261021.md`
commit `0837361aa97f5d7f2116868cb2273eeac3acd0dc`.

## Accepted predecessor

- G2 implementation code: `66e8f0a8b3a93140b5f908628b55ac965e15b96e`.
- G2 result/evidence: `ac1d1184255945b2c4304641360a1e661ff2d7bd`.
- G2 CHAT verdict: BUILD accepted for isolated-host design.
- Historical G3 PreExec: `14a02ab5f42a7659efd2b1e60324c49ff70695b5`, BLOCKED and preserved.
- Current code lineage base for this branch: `c61ffd259a384e9c96b563968c6b7b98a0f156cd`.

Do not replay or rewrite those historical attempts/receipts.

## Governance source set

Live governance branch:
`work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019`
observed head `d34da1e3b4918a902646621b487ca8ad3e05b0e0`.

Resolved governing sources remain:
- Policy 2.0.0 source commit `96175ac4f39197794a04e695f0046fa7ef9321fe`;
- Dictionary 1.3 source commit `b25f7f728de67cf8595bf24f22fcbd79ef50babc`;
- Routing 1.4.0 source commit `bcd008983b61349646a5198ff243069f81484fae`;
- Git-first Protocol 12 source commit `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`;
- PreExec Evidence Protocol 1.1 / Receipt Schema 1 / Result Contract v2 remain the machine contracts.

BRD-09 REV3 and Bridge TechSpec REV10 remain globally CANDIDATE; task-specific G1/G2 acceptance plus the same-host design acceptance govern this scoped rework. No global promotion is implied.

## Objective

Replace the isolated-host-only AppLocker policy assumption with a **same-host guarded composite-policy model** that can be tested later on the Owner's only physical Windows 11 Pro host without creating an implicit machine-wide deny policy for unrelated required applications.

BUILD only. Do not mutate the Windows host policy/service state.

## Required implementation

### A. Composite policy model

Update `f1_policy.py` so the policy model can represent:
- mandatory F1 Exe and Script enforcement;
- Msi/Dll as conditional surfaces rather than always-Enforced;
- a reviewed host-safe baseline;
- no broad user-writable path trust.

Supported baseline rule classes may include:
- Windows/SystemApps coverage;
- restricted non-user-writable Windows / Program Files paths;
- reviewed publisher rules;
- exact hash rules.

Reject:
- unrestricted user-writable path allow rules;
- broad allow-all for the interactive user;
- unsupported rule types/XML;
- baseline rules that override an explicit F1 deny.

### B. Dual policy identities

Add and bind:
- `effective_policy_digest`: canonical digest of the complete expected effective AppLocker policy;
- `f1_control_digest`: canonical digest of the deterministic FOX2 F1 control subset.

The F1 subset must include:
- mandatory Exe/Script collection modes;
- deterministic F1 rule identities;
- expected principals/actions/hashes;
- legacy/current control identities;
- service/SystemApps extension semantics where relied upon.

### C. HostFence

Update `f1_service.py` so positive authority denies unless:
1. effective AppLocker policy matches the expected full digest; and
2. F1 control subset matches the expected F1 digest.

Policy drift in either identity must fail closed.

### D. Same-host collection semantics

Final positive G3 contract:
- Exe = Enforce;
- Script = Enforce;
- Msi = conditional;
- Dll = conditional.

Msi/Dll must not silently become Enforce merely because the package contains MSI/DLL/native dependencies.

Protected ProgramData ownership/DACL and runtime SHA-256 sealing remain mandatory.

### E. Audit-to-enforce support

Provide source-level support/evidence format for:
- pre-enforcement policy snapshot identity;
- AuditOnly compatibility phase;
- final expected Enforce policy identity;
- rollback artifact identity.

This BUILD must not apply a policy or start/stop services.

### F. Compatibility

Preserve accepted F0/G2 behavior where not superseded by this same-host design:
- no-replay;
- consumer convergence;
- protected root;
- service identity/pipe authentication;
- source/package binding;
- direct installed claim denial;
- copied legacy identity closure.

Do not keep an unsafe isolated-host invariant merely to satisfy an old unit test; update tests to the accepted same-host contract while preserving historical evidence.

## Allowed write paths

Product/code:
- `agent_bridge/src/fox2_agent_bridge/f1_policy.py`
- `agent_bridge/src/fox2_agent_bridge/f1_service.py`
- `agent_bridge/src/fox2_agent_bridge/f1_protocol.py` only if required for adoption-plan contract
- `agent_bridge/src/fox2_agent_bridge/f1_authority.py` only if required by dual-digest contract
- `agent_bridge/scripts/f1_policy_artifact.py`
- `agent_bridge/scripts/f1_inventory.ps1`
- `agent_bridge/scripts/f1_*.py`
- `agent_bridge/scripts/f1_*.ps1`

Tests:
- `agent_bridge/tests/test_f1_policy.py`
- `agent_bridge/tests/test_f1_authority.py`
- `agent_bridge/tests/test_f1_host_fence.py`
- `agent_bridge/tests/test_f1_windows.py`
- `agent_bridge/tests/test_f1_consumers.py`
- other `agent_bridge/tests/test_f1_*.py` only when directly necessary
- existing Bridge regression tests only when needed to preserve compatibility

Result/evidence:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/samehost/**`

No governance/BRD/TechSpec/global roadmap edits by CODEX.

## K1

Every material diff hunk must be classified:
- REQUESTED;
- NECESSARY_DEPENDENCY; or
- JUSTIFIED_GENERATED.

`UNEXPLAINED=0` required. No drive-by refactor.

## Acceptance

1. Composite parser/canonicalizer supports reviewed safe baseline rule types.
2. Broad user-writable path allow is rejected.
3. F1 rule subset has a deterministic `f1_control_digest`.
4. Complete expected policy has deterministic `effective_policy_digest`.
5. Changing host baseline changes only/at least the effective digest as expected.
6. Removing/changing a mandatory F1 control changes F1 digest and HostFence denies.
7. Exe/Script cannot be AuditOnly/NotConfigured at final positive-G3 contract.
8. Msi/Dll can remain AuditOnly/NotConfigured when not explicitly required.
9. No direct policy/service/ACL host mutation code path is executed during BUILD/tests.
10. Existing protected-root/runtime/source/package/no-replay boundaries remain green.
11. Focused same-host policy/service tests PASS.
12. Full `agent_bridge/tests` regression PASS.
13. Secret scan / changed-path allowlist / diff check PASS.
14. Result Contract v2 report + evidence manifest are produced and pushed.
15. Historical G2/G3 FAIL/BLOCKED/NOT_RUN receipts are not rewritten.

## Permissions

Technical permission profile: FULL_ACCESS within the dedicated worktree for code/build/test only.

Explicitly forbidden:
- Set-AppLockerPolicy / effective AppLocker mutation;
- AppIDSvc mutation;
- Windows service install/start/stop/delete;
- ProgramData F1 authority-root ACL mutation;
- reboot;
- G4 adoption;
- Canary009;
- main/merge;
- provider/trading broker;
- LIVE.

## STOP

STOP and report BLOCKED/REWORK if:
- exact source/task/prompt binding is not what was issued;
- worktree has unrelated WIP or competing writer;
- route/model/thinking differs;
- implementation requires host mutation to prove BUILD correctness;
- a safe same-host baseline cannot be represented without broad user-writable trust;
- full regression fails and cannot be resolved within allowed scope;
- any requested change exceeds allowed paths.

## Result delivery

Agent must push to the exact non-main task branch:
- code/tests;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- bounded evidence under `evidence/samehost/`.

Outside the committed report, return the observed remote result SHA to CHAT.

Git push is `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.
