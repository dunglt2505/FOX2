# FOX2 — R3 CODEX A01 Recovery Probe 1 — Partial Result

Date: 2026-10-22
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001`

## Read-only observations before probe script error

Owner-host reconciliation probe observed:

- Dispatch already declared consumed / no-replay by the execution launcher.
- task branch: `work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-20261022`
- runtime base: `7fcdfd19e0d9177b4d85e39fd249b5e65ccc0d49`
- local HEAD: exactly runtime base
- remote HEAD: exactly runtime base
- durable claim at the probed common-dir path: not found
- task-scoped CODEX process count: 0
- local git status count: 0 / clean worktree

The read-only probe then failed in its own reporting logic because an empty/scalar PowerShell value did not expose a `.Count` property.

## Meaning

The failure is in the recovery probe reporting code, not in product code and not a new Agent execution.

The observed Git/process facts strongly indicate no local code/result and no active writer, but claim-path ambiguity and CODEX last-message remain unresolved.

## Verdict

`PARTIAL_RECOVERY_EVIDENCE / NO_REPLAY`

Do not replay the consumed Dispatch.

Run only one corrected read-only discriminating probe that:
- wraps all potentially empty results in arrays;
- checks both worktree git-dir and common-dir attempt-claim locations;
- inspects any recent R3 CODEX last-message;
- confirms local commits/WIP/result paths remain absent.

No CODEX invocation, Git write, reset, clean, commit, push, package or host lifecycle action is authorized by this probe.
