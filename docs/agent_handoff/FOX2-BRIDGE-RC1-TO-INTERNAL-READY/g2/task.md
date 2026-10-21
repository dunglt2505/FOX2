# FOX2 — G2 Integrated F1 Build Task

Task ID: `FOX2-BRIDGE-RC1-G2-A01`  
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
Stage: BUILD  
Attempt: NEW A01 — never reuse/replay any prior Dispatch/Attempt  
Task branch: `work/FOX2-BRIDGE-F1-G2-INTEGRATED-BUILD-20261021`  
Task base: `fe926ad24d89231e5cf80f0f48ea44eb36887834`

## Owner authorization

Owner directive on 2026-10-21: `Tiếp tục làm đi, ko cần dừng lại`.

Scoped record:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/owner_directives/G2_CODING_HOLD_LIFT_20261021.md`
at commit `fe926ad24d89231e5cf80f0f48ea44eb36887834`.

This supersedes the earlier G2 coding HOLD for this integrated DEV attempt only. Historical HOLD evidence remains factual. This task grants no main/merge/deploy/provider/broker/Canary/LIVE authority.

## Controlling source set

Governance / routing:
- Projectwide Registry: commit `1f04d62fb7039646c9a213f04a1f1eb17e0f2cc5`, blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`.
- Current Source Resolution: commit `b04ded4b9d7fb241dc69ad25097eb474807cf68c`, blob `186fdbc72dc1b22e97330895142d68600591ac21`.
- Policy 2.0.0: commit `96175ac4f39197794a04e695f0046fa7ef9321fe`, blob `2d373f374f906bf7959062050bbeae5350b0c482`, SHA-256 `281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e`.
- Dictionary 1.3: commit `b25f7f728de67cf8595bf24f22fcbd79ef50babc`, blob `6c8f30e2e6b07f2e65e45c14faab99672d036083`, SHA-256 `8a64771916d9e3d447f560658e20b307b5945a5d6b3820ea61cd0298636abe1d`.
- Routing 1.4.0: commit `bcd008983b61349646a5198ff243069f81484fae`, blob `14d2e95e419cc67c3e0cf851cc806a96cf885b7e`, SHA-256 `5759b9a8d63ef165ef63c60ecc601198e39296518c5a1eb91db54555ccd07205`.
- Git-first Protocol 12: commit `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`, blob `d34a022f2bda39a167a404c8530e57b30f337cb9`.

Bridge semantics:
- BRD-09 v0.1 REV3 remains CANDIDATE / NO_DEV_GRANT globally; task input commit `e13820c05ec0c7e97853daa61f6f5fb6b73391cc`, blob `99971d65ccb90874e75ace54e6a4f8ec21ba0188`.
- Bridge TechSpec v0.7 REV10 remains CANDIDATE globally; task input commit `e13820c05ec0c7e97853daa61f6f5fb6b73391cc`, blob `5a82bd74b30f71f7b46652f67a70cd7768f68143`.
- G1 task-specific accepted design: `docs/architecture/FOX2_BRIDGE_F1_G1_DESIGN_ACCEPTANCE_20261021.md` @ `9c27e7c7104facdb7f083350f38d2451939b6c2a`.
- G2 integrated build scope: `docs/architecture/FOX2_BRIDGE_F1_G2_INTEGRATED_BUILD_SCOPE_CANDIDATE_20261021.md` @ `9410edb0d88631c33ffda8494b238ec9f4446dc1`.
- G2 source/route entry: `docs/architecture/FOX2_BRIDGE_F1_G2_SOURCE_ROUTE_PREEXEC_ENTRY_20261021.md` @ `0feff4223746a48e449bb961eecabb1d86388e41`.
- G2 PreExec contract: `docs/architecture/FOX2_BRIDGE_F1_G2_PREEXEC_CONTRACT_CANDIDATE_20261021.md` @ `2f8fa342613ec7f64204d8e192559847581235e6`.

G1 acceptance is task-specific design authority for the F1 delta. Do not relabel BRD-09 or TechSpec v0.7 globally EFFECTIVE.

## Role / engine / execution

- Role: implementation Agent.
- Product: CODEX.
- Model policy: PINNED.
- Model: `gpt-6.1-sol`.
- Reasoning effort: `high`.
- Permission profile: `FULL_ACCESS` technical capability, bounded by this task and STOP conditions.
- Execution path: MANUAL_LOCAL/native CLI in one dedicated non-main worktree.
- Delivery owner: AGENT.
- Max implementation attempts: 1 after task-specific PreExec PASS.

## Objective

Implement the single integrated F1 BUILD scope required by accepted G1 design:

1. trusted Windows execution-authority service boundary;
2. authenticated local IPC with server-derived caller identity;
3. service-owned global consumed-ID / epoch / lease / revocation state;
4. service-owned atomic claim-and-Agent-spawn path;
5. deterministic AppLocker policy artifact generation/validation support;
6. convergence of all installed positive execution consumers onto the trusted service gate;
7. fail-closed recovery/restart/clock/policy/service drift semantics;
8. source-level and Windows-CI tests sufficient for G2 BUILD acceptance.

G2 does NOT deploy AppLocker to the Owner host and does NOT certify runtime enforcement. F1 positive installed authority remains DENY until G3/G4.

## Required behavior

### Trusted authority

- Ordinary Bridge desktop/worker/requester cannot mint positive authority.
- Service derives Windows caller identity from authenticated IPC/token; caller-supplied identity is advisory only.
- Global claim identity is unique across roots.
- Persisted claim precedes actual spawn. Ambiguous/failed spawn leaves the dispatch consumed.
- Service restart increments/fences authority epoch and invalidates old leases without replay.
- Policy/AppIDSvc/source/package/epoch/lease/time uncertainty denies new spawn.
- No reusable bearer authorization enabling an unprivileged caller to spawn independently.

### Spawn

Service owns authorization + creation of the Agent process. Preserving interactive user credentials may use an authenticated user token / CreateProcessAsUser-equivalent implementation, but falling back to caller `Popen` for installed positive execution is forbidden.

### AppLocker

Build policy artifact support only; do not apply host policy in G2.

- relied-upon collections use Enforce mode;
- executable + script legacy surfaces are mandatory;
- MSI/DLL included when inventory shows an executable/bypass dependency;
- copied legacy artifacts are closed by publisher/hash identity as applicable, not user-writable path-only trust;
- current approved package/source/policy identities are exact and deterministic;
- AppIDSvc absent/stopped/policy mismatch is runtime DENY;
- no broad allow of user-writable directories.

### Consumer convergence

At minimum inspect/change as required:
- `f1_broker_store.py`
- `f1_reconcile.py`
- `ledger.py`
- `launcher.py`
- `desktop.py`
- `app.py`
- `ops_runner.py`
- `e2e_runner.py`
- `installation.py`
- `startup.py`

Installed direct SQLite claim or unprivileged launcher spawn must not become a positive F1 bypass.

## Allowed write paths

Product code:
- `agent_bridge/src/fox2_agent_bridge/f1_*.py`
- `agent_bridge/src/fox2_agent_bridge/ledger.py`
- `agent_bridge/src/fox2_agent_bridge/launcher.py`
- `agent_bridge/src/fox2_agent_bridge/desktop.py`
- `agent_bridge/src/fox2_agent_bridge/app.py`
- `agent_bridge/src/fox2_agent_bridge/ops_runner.py`
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
- `agent_bridge/src/fox2_agent_bridge/installation.py`
- `agent_bridge/src/fox2_agent_bridge/startup.py`
- `agent_bridge/scripts/f1_*.py`
- `agent_bridge/scripts/f1_*.ps1`
- `agent_bridge/scripts/build_user_package.py`
- `agent_bridge/scripts/install_user.ps1`
- `agent_bridge/pyproject.toml` ONLY if a new dependency is strictly necessary and justified.

Tests:
- `agent_bridge/tests/test_f1_*.py`
- `agent_bridge/tests/test_runtime_ledger.py`
- `agent_bridge/tests/test_rc1_launcher.py`
- `agent_bridge/tests/test_desktop.py`
- `agent_bridge/tests/test_ops_runner.py`
- `agent_bridge/tests/test_e2e_runner.py`
- `agent_bridge/tests/test_installation.py`
- `agent_bridge/tests/test_rc1_package.py`

Result delivery:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- bounded supporting evidence under `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/**`.

No other path may change without STOP and CHAT re-scope.

## Acceptance

G2 result must demonstrate, with real tests/evidence:

1. service unavailable or OS-fence/AppIDSvc/policy binding unavailable => installed positive claim/spawn denied;
2. forged caller/task/source/package/nonce/epoch rejected;
3. concurrent same-dispatch attempts yield one global consumed result;
4. restart/revocation/lease expiry/clock rollback prevents new spawn and does not replay;
5. launcher/desktop/ops/e2e installed paths cannot bypass service;
6. policy model closes copied legacy fixtures by deterministic publisher/hash identity rules;
7. approved-current fixture can be represented without broad user-writable path trust;
8. reconciliation ambiguity/WAL/SHM/missing root/manual overlap remains HOLD/DENY;
9. frozen F0 cross-root negatives remain green;
10. full existing Bridge regression suite remains green;
11. package/service/policy support does not silently install/activate host policy during build/tests;
12. rollback returns to DENY and preserves consumed/tombstone state;
13. no host AppLocker mutation, service install/start, admin elevation, scheduled-task mutation or Canary execution occurs in G2;
14. material diff hunks are classified `REQUESTED`, `NECESSARY_DEPENDENCY`, or `JUSTIFIED_GENERATED`; unexplained changes are unacceptable.

A unit/mock test is not G3 enforcement certification. Clearly label host-only/elevated tests NOT_RUN where applicable.

## Tests

Run the narrow new F1 tests first, then all directly affected regression tests, then the full `agent_bridge` test suite supported by the host. Run packaging/static checks required by changed scripts. Preserve actual command, exit status and bounded logs in evidence; no historical CI substituted for new code.

## Result contract

Resolve and obey Dictionary 1.3:
- Result Schema v2: `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`
- Result Template v4: `docs/agent_handoff/FOX2_AGENT_RESULT_TEMPLATE_v4.md`
- CHAT Intake v9: `docs/agent_handoff/FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v9.md`

Agent must commit/push actual code plus:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`

Supply the observed remote result SHA outside committed report. Git push is `PUSHED_UNREVIEWED` until CHAT result review.

## STOP

STOP without broadening scope if any of these occurs:
- task-specific PreExec is not PASS;
- worktree/branch/source head differs from immutable binding;
- competing writer exists;
- exact CODEX model/reasoning/permission is unsupported;
- implementation would require writing outside allowed paths;
- implementation would need actual AppLocker deployment, service installation/start, elevation or host policy mutation;
- an old Dispatch/Attempt would need replay;
- source/package/policy authority is ambiguous;
- tests reveal a safety regression that cannot be fixed within allowed scope;
- main/merge/deploy/provider/broker/Canary/LIVE becomes necessary.

Do not self-authorize around STOP. Return a bounded BLOCKED result when code/result delivery is possible.
