# FOX2 — CODEX EXECUTION PROMPT — G2 Integrated F1 Build A01

Role: CODEX — implementation Agent  
Model: `gpt-6.1-sol`  
Reasoning: `high`  
Permission profile: `FULL_ACCESS` technical sandbox only, bounded by task scope  
Execution path: `MANUAL_LOCAL`  
Max implementation attempts: `1`

## Immutable pickup

Repository: `dunglt2505/FOX2`  
Branch: `work/FOX2-BRIDGE-F1-G2-INTEGRATED-BUILD-20261021`

Task publication:
- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/g2/task.md`
- task publication commit: `653e49fc0d0f15981bf230995925c89d6994723d`
- task blob SHA-1: `7f0b82e56f7bfa001e40bb176bb26b0ef918c609`

Read the complete task.md first. This prompt does not broaden it.

DO NOT START implementation unless the launcher/CHAT has verified a fresh task-specific PreExec receipt for this exact G2 branch/source chain with:
- overall `PASS`;
- CODEX as the pinned material route;
- requested model `gpt-6.1-sol`;
- reasoning `high`;
- no competing writer;
- exact non-main worktree;
- `executable_dispatch_published=false`;
- `dispatch_consumed=false`;
- `agent_execution_started=false`.

A historical PASS from another Bridge WP/profile is invalid.

## Mission

Implement the single integrated F1 BUILD defined by task.md and accepted G1 design.

The goal is not another design/report cycle. Deliver working source + tests for the trusted Windows execution-authority seam:

- trusted Windows service authority;
- authenticated local IPC with OS-derived caller identity;
- global service-owned consumed-ID / epoch / lease / revocation state;
- atomic service-owned claim + Agent spawn;
- deterministic AppLocker policy artifact support;
- all installed positive consumers converged onto that authority;
- fail-closed restart/revocation/clock/policy/service-drift semantics;
- G2 source/Windows-CI evidence.

F1 positive runtime on the Owner host remains DENY until G3/G4. Do not deploy policy/service or claim installed enforcement.

## Implementation principles

1. Reuse `f1_broker_store.py` and `f1_reconcile.py` safety primitives where valid; do not turn their current offline APIs into unprivileged positive authority.
2. Preserve `ledger.py` installed-root fail-closed behavior unless the positive path is explicitly mediated by the trusted service.
3. Remove/close installed direct Worker spawn authority from `launcher.py`; unprivileged caller-side `Popen` is not an F1 grant.
4. Keep tray/desktop interactive-user UX separate from the privileged authority service.
5. Service authenticates IPC peer and derives caller identity from Windows; never trust caller-supplied SID/user fields as authority.
6. Claim persistence occurs before spawn. Ambiguous spawn remains consumed.
7. No reusable bearer token enabling caller-controlled spawn.
8. Service restart/authority epoch rollover revokes leases; consumed identities survive.
9. AppLocker support is deterministic artifact generation/validation only in G2. Do not modify effective local policy.
10. Do not broaden dependencies casually. If a new dependency is necessary, justify it in K1/report and keep packaging deterministic/offline-compatible.
11. Prefer a small coherent F1 module boundary over duplicated execution engines.
12. Do not weaken F0 negatives, pause/resume/no-replay, source/package binding, or current installation safety.

## Allowed paths

Only task.md allowed write paths. New source files must match the allowed F1 patterns. No governance/BRD/TechSpec edits.

No main, PR merge, deployment, provider, broker, Canary or LIVE action.

## Required engineering evidence

Run, in order:

1. focused new F1 tests;
2. directly affected regression tests;
3. full supported `agent_bridge` suite;
4. packaging/static checks for changed scripts/artifacts;
5. any Windows-specific non-elevated build tests possible on this host.

For every command record bounded command identity, exit code and result summary. Do not paste secrets/raw credential-bearing output.

Host-elevated enforcement tests that belong to G3 must be `NOT_RUN_G3`, never PASS.

## Required negative coverage

At minimum prove:

- service absent => DENY;
- AppIDSvc/policy binding absent or drift => DENY;
- forged caller/task/source/package/nonce/epoch => DENY;
- same dispatch concurrency => one consumed identity;
- restart/revoke/lease expiry/clock rollback => no new spawn;
- launcher/desktop/ops/e2e cannot bypass service;
- ambiguous reconciliation/WAL/SHM/missing roots remains DENY/HOLD;
- copied legacy policy fixtures cannot escape via user-writable path-only trust;
- rollback preserves consumed/tombstone state and returns positive authority to DENY.

## K1 diff discipline

For every material changed hunk classify one of:

- `REQUESTED`
- `NECESSARY_DEPENDENCY`
- `JUSTIFIED_GENERATED`

No drive-by refactor. Any `UNEXPLAINED` hunk is a delivery defect.

## Result delivery

Commit/push only the authorized non-main branch.

Required result artifacts:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- bounded evidence under `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/**`.

Report must include:
- exact start SHA / final SHA;
- changed-path list and K1 classification;
- tests actually run, with PASS/FAIL/NOT_RUN;
- security/replay/concurrency results;
- known G3 host-only gaps;
- confirmation that no AppLocker policy/service was installed/started;
- confirmation no main/merge/Canary/LIVE action occurred.

After push, output the observed remote result commit SHA outside the committed report.

Git push is `PUSHED_UNREVIEWED`. Do not self-accept. CHAT performs independent `fox2-result-review`.

## STOP

STOP and return a bounded BLOCKED result if:
- fresh G2 PreExec is not PASS;
- exact branch/worktree/source/prompt identity differs;
- another material writer appears;
- `gpt-6.1-sol` / `high` / required permission mode cannot be honored exactly;
- a required change is outside allowed paths;
- implementation requires elevation, effective AppLocker mutation, service install/start or G3 enforcement;
- an old Dispatch/Attempt must be replayed;
- source/package/policy identity is ambiguous;
- safety regression cannot be fixed within scope.

Do not ask the Owner to expand scope. Do not silently switch Agent/model/reasoning. Do not bypass STOP.
