# FOX2 — CHAT Result Review — Presentation Lock Certifier Rework R4

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001`
Runtime base: `35aa18ccabcc6f7d4b889ed213c075fc314d45d0`
Observed remote result SHA: `d997756b5f4cfaa7e442dfc5d929093782b7a90f`

## Verdict

**CHAT_REWORK — bounded semantic gap in errno-13 differential proof**

The R4 result is real, remotely delivered and reviewable, but it is **not accepted** as the certifier correction source.

No A05/G3/G4/Canary unlock follows from R4.

## Remote delivery / provenance

CHAT independently observed:

- result branch is one commit ahead of runtime base;
- 20 changed paths;
- only two product/test paths changed:
  - `agent_bridge/scripts/certify_user_lifecycle.py`
  - `agent_bridge/tests/test_lifecycle_wpf_contract.py`
- remaining changed paths are report/manifest/R4 evidence;
- no unauthorized changed path was observed;
- committed report and evidence manifest are present;
- CODEX returned observed remote SHA outside the report;
- launcher observed local HEAD = remote HEAD = result SHA and worktree clean;
- Dispatch is consumed/no-replay.

## Valid evidence preserved

R4 produced useful evidence that remains reusable where inputs are unchanged:

- focused tests: **66 PASS**;
- full `agent_bridge/tests`: **683 PASS**;
- `git diff --check`: PASS;
- exact changed-path allowlist: PASS;
- bounded secret/privacy scan: PASS;
- K1: `UNEXPLAINED=0`;
- Result Contract v2 evidence was generated and self-checked;
- no real Host Lifecycle was run;
- no package build/install/update/uninstall/reinstall;
- no Worker/F1;
- no A05/G3/G4/Canary/main/merge/provider/broker/LIVE action.

Historical A04 PASS and R3 recovery evidence remain unchanged.

These green results do **not** override the semantic defect below.

## FIRST_FAILURE / semantic defect

Required R4 rule:

> `PermissionError(errno=EACCES/13, winerror absent/None)` is accepted only with differential ownership proof.

For a fresh or zero-WPF launch path, the required differential proof is **pre-live accessibility of the existing lock + exact live presentation identity**.

R4 code records:

- existing pre-live lock, openable → `pre_live.classification = OPENABLE`;
- no pre-live lock → `pre_live.classification = ABSENT`.

After the live denial, R4 uses the condition equivalent to:

`denial == SHARING_VIOLATION OR 'pre_live' in probes`

This checks for the **presence of the pre_live record**, not whether the pre-live lock was actually accessible.

Therefore:

1. lock absent before launch;
2. WPF later creates the lock;
3. live probe returns `PermissionError(errno=13, winerror=None)`;

can be accepted as held merely because the `pre_live` key exists with classification `ABSENT`.

That violates the task's fail-closed differential-proof rule.

## Why the tests did not catch it

The current `test_absent_pre_live_lock_allowed` removes the lock before launch but leaves the default denial mode as explicit sharing violation / winerror 32.

That correctly proves that **absence is allowed for winerror 32**, but does not exercise absent-pre-live + errno13.

The current differential-proof parametrization exercises errno13 with a pre-existing accessible lock, which is valid and therefore also does not expose the gap.

Missing negative coverage:

- fresh mode: pre-live lock ABSENT + live errno13/no-winerror → FAIL CLOSED;
- continuation mode with zero WPF: pre-live lock ABSENT + live errno13/no-winerror → FAIL CLOSED.

Existing-live continuation remains different: errno13 may stay provisional until graceful exit + zero WPF + same-lock post-exit openability proves differential ownership.

## DEFECT_SLICE

Affected code:
- `agent_bridge/scripts/certify_user_lifecycle.py`

Affected tests:
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

No third product/test file is required.

Minimum correction:

1. distinguish:
   - pre-live `OPENABLE`;
   - pre-live `ABSENT`;
   - existing-live continuation entered with one exact-current WPF.
2. live `SHARING_VIOLATION / winerror32` remains accepted.
3. live errno13/no-winerror:
   - fresh or zero-WPF launch path: accept only when pre-live classification was exactly `OPENABLE`;
   - pre-live `ABSENT`: fail closed;
   - existing-live continuation: keep provisional and finalize only after graceful exit, zero WPF and same-lock post-exit `OPENABLE`.
4. preserve same-file identity and lock bytes.
5. add explicit negative tests for ABSENT + errno13 in both fresh and continuation-zero-WPF modes.
6. rerun focused and full affected suite plus mandatory static/result checks.

## K1 review

The delivered R4 hunks are within requested scope, but the hunk implementing the live-denial decision is **REQUESTED_BUT_INCOMPLETE**, not accepted merely because the Agent K1 file labeled it REQUESTED.

No unrelated code change was identified.

## Evidence wording note

R4 report/source-binding text states that no fresh R4 Dispatch file was present in the starting tree. The task worktree indeed did not contain the control-branch Dispatch file, but the governed execution was actually bound to fresh Dispatch
`FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001`.

This wording is imprecise but not the primary rejection cause. The next result should bind the actual fresh attempt Dispatch explicitly in report/evidence provenance.

## Stage/status effect

Whole feature remains:

`TEST / IN_PROGRESS`

Residual certifier correction remains:

`BUILD / REWORK_REQUIRED`

Real Host Lifecycle remains:

`NOT_RUN`

A05 remains locked.

## No replay

R4 Dispatch is consumed and MUST NOT be replayed.

Any correction requires a fresh attempt identity under the same Whole-WP.

## Next safe action

Create one fresh bounded correction attempt from R4 result SHA as **unaccepted salvage input**, while keeping accepted product source `085cc8302e824dbccf9cbef80422ed48894b9cb4` distinct.

Reuse all unaffected PASS.

Recheck only mandatory new-attempt/time-dependent gates.

