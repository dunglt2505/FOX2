# FOX2 — CODEX Execution Prompt — Same-Host Guarded Policy BUILD A01

Role: CODEX — Primary implementation owner
Model: gpt-6.1-sol
Thinking: high
Project: FOX2 only
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Task ID: FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01
Mode: MANUAL_LOCAL / FULL_ACCESS in dedicated worktree
Attempt: A01 / max 1 after fresh PreExec PASS

## Immutable task

Task path:
`docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/task.md`

Task publication commit:
`2a46a456bae3ea83ca236d210e3a0c9901a4b31d`

Task raw Git-blob SHA-256:
`71c4e1c0401c429878fabb95859f64c568c43dbe02f2ffab7b8c0de41b0837fa`

Read the task in full before editing. The task is authoritative for scope, acceptance, allowed paths and STOP rules.

## Source authority

Use exactly the source set stated in task.md, including:
- Owner physical-host-only directive commit `438169d5728a4b5b5da19b737e79db3fc6515ce0`;
- same-host design candidate `c8307980362a1ab64b93ba7d7e020d979017c849`;
- CHAT design acceptance `0837361aa97f5d7f2116868cb2273eeac3acd0dc`;
- accepted G2 code `66e8f0a8b3a93140b5f908628b55ac965e15b96e`;
- current task branch lineage base `c61ffd259a384e9c96b563968c6b7b98a0f156cd`;
- live governance head `d34da1e3b4918a902646621b487ca8ad3e05b0e0`.

Do not substitute main, another branch, a later unreviewed document, or historical isolated-host assumptions.

## Objective

Implement the accepted same-host guarded AppLocker model so FOX2 can later be tested on the Owner's only physical Windows 11 Pro host without turning the current isolated-host exact-hash policy into an unsafe machine-wide implicit deny policy.

BUILD/test only. Do not mutate effective AppLocker policy, AppIDSvc, Windows services, ProgramData authority ACL/state or reboot the host.

## Required implementation behavior

1. Rework the policy model for a reviewed composite host policy.
2. Exe + Script are mandatory final F1 enforcement surfaces.
3. Msi + Dll are conditional and must not silently be forced to Enforce.
4. Preserve/reject baseline rule types exactly as task.md requires.
5. Broad user-writable path trust must fail validation.
6. Introduce deterministic:
   - `effective_policy_digest`;
   - `f1_control_digest`.
7. HostFence must validate both and deny on drift.
8. Keep protected-root/runtime hash sealing and existing no-replay/source/package/service boundaries.
9. Add audit-to-enforce/rollback identity support as source/evidence contracts, without applying policy.
10. Keep historical receipts/results immutable.

## Engineering constraints

- Make the smallest coherent implementation satisfying the accepted design.
- No drive-by refactor.
- Preserve backward compatibility only where it does not reintroduce the unsafe isolated-host assumption.
- If an old unit test encodes the superseded isolated-host requirement, update that test to the accepted same-host contract and explain it in K1.
- Do not weaken fail-closed behavior merely to make tests pass.
- Do not add a broad `allow *` or user-writable path rule as a shortcut.

## Allowed paths

Only paths authorized by task.md may be written.

Any material diff outside the allowlist => STOP and report.

## Tests

At minimum:
- focused policy canonicalization tests;
- HostFence dual-digest tests;
- mandatory Exe/Script / conditional Msi/Dll tests;
- user-writable baseline rejection tests;
- F1 subset drift tests;
- current no-replay/consumer/security regression tests affected by the change;
- full `agent_bridge/tests` regression.

Also run:
- changed-path allowlist;
- `git diff --check`;
- bounded secret scan;
- any existing static/package checks applicable to changed files.

Do not use a host policy mutation as a test.

## K1

Produce evidence showing every material hunk classified as one of:
- REQUESTED
- NECESSARY_DEPENDENCY
- JUSTIFIED_GENERATED

Required: `UNEXPLAINED=0`.

## Result Contract

Before completion, create/update:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- bounded evidence under `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/samehost/`.

Result manifest must conform to the current FOX2 Result Contract resolved by task.md.

Report must clearly identify:
- task ID;
- CODEX / gpt-6.1-sol / high;
- exact source/task identity;
- tests, including any FAIL/BLOCKED/NOT_RUN;
- K1;
- no host mutation;
- remaining physical-host G3 gates.

Push all permitted result bytes to:
`work/FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021`.

After push, print the observed remote result SHA outside committed artifacts.

Git push is not CHAT acceptance.

## Forbidden

Do not:
- call Set-AppLockerPolicy;
- change AppIDSvc;
- install/start/stop/delete FOX2F1Authority;
- alter ProgramData F1Authority ACL/state;
- reboot;
- merge/main;
- run Canary009;
- access provider/trading broker/LIVE;
- replay G2 A01 or G3 host attempts;
- rewrite historical G2/G3 evidence.

## STOP

STOP without improvising if:
- source/task/prompt binding differs;
- worktree/writer or PreExec is not valid;
- model/role/thinking differs;
- a safe same-host design cannot be implemented within allowed paths;
- implementation would require real host enforcement to complete BUILD;
- tests reveal a security contradiction needing design re-review.

Return a truthful result: PASS candidate, REWORK/BLOCKED, or DELIVERY_BLOCKED. Never convert FAIL/BLOCKED/NOT_RUN to PASS.
