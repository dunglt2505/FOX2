# FOX2 — Native Offline Manual Local Admission implementation: attempt 01

**Artifact:** executable assignment task (to be acted on ONLY after Prompt Builder prompt immutable Git readback and CHAT assignment publication); **existing supporting WP** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`, within existing Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. This is NOT a new WP or replay of any prior Dispatch.

**Agent**: CODEX, CLI local on FOXLE-PC. **Exact engine/model:** PINNED `gpt-6.1-sol`. **Thinking**: `medium`. **Permission**: `FULL_ACCESS` with `--sandbox danger-full-access`, approval policy `never`, inside exact Windows authorized coding worktree only; the prompt's exact allowed paths and STOP gates still apply. **One actual coding Agent invocation maximum** for this attempt. **Git delivery owner:** AGENT; CHAT owns independent acceptance.

**ATTEMPT_ID**: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-OFFLINE-ATTEMPT-01`.
**CODE_BRANCH**: `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`.
**CODE_WORKTREE**: `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`.
**EXACT_CODE_START_SHA**: `23afe56675b9b3698d47c192d4e22b62c82be435`.
**HANDOFF_BRANCH**: `work/FOX2-BRIDGE-NATIVE-OFFLINE-IMPL-HANDOFF-20261020`. Prompt path is `docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ATTEMPT_01/prompt.md`; authenticate its immutable commit/blob/SHA-256 from CHAT's dispatch acceptance before invocation.
**ROUTE**: `NATIVE_LOCAL_CODEX_CLI_OFFLINE_DEV`; not `BRIDGE`, not an existing immutable `MANUAL_LOCAL` Dispatch, and no installed Worker/ledger process is used.
**MAX_RUNS**: 1. No retry or reissue after an uncertain start/partial result.

## Source / authority

1. Scoped Owner code rights: `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json`. It authorizes the six primary code/test paths below and *conditionally* exact justified other paths; this assignment authorizes **only the six**. No wildcard/implicit conditional expansion.
2. Original infrastructure task, frozen: `482d26d71c5c95f028f9b4110349e4d318bcb342:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/task.md` (its unchanged bytes also in CODE_START_SHA). Original BRIDGE bootstrap preflight `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json` is historical `BLOCKED` and must never be rewritten/promoted.
3. **PreExec receipt actually PASS for new independent native route**, source SHA `9106e8d4465db5f313911394579da9d39f296f73`, published Git result `23afe56675b9b3698d47c192d4e22b62c82be435:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/native_offline_preflight_20261020.json`, blob `882661efc3d757de1121ec540aadfc1fa30f35ac`; one CODEX marker ran, NOT the coding task. Agent probe checked pinned `gpt-6.1-sol` Medium FULL_ACCESS; all material receipt capabilities PASS. Results are scoped point-in-time, **not** post-start evidence or quota telemetry.
4. Human governance for *new* scoped action: `d34da1e3b4918a902646621b487ca8ad3e05b0e0:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json`, human Policy v2.0.0 source `96175ac4f39197794a04e695f0046fa7ef9321fe:docs/governance/FOX2_POLICY_V2.0.0.md`, Dictionary v1.3 `b25f7f728de67cf8595bf24f22fcbd79ef50babc:docs/governance/FOX2_PROJECT_DICTIONARY_v1.3.json`, Routing Index v1.4.0 `bcd008983b61349646a5198ff243069f81484fae`, Git-first Protocol v12 `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`. Human authority does **not** modify installed Bridge or old task source locks.
5. Frozen installed Bridge implementation source: `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`; all six target files at CODE_START_SHA verified same Git blobs as frozen baseline. Source impact candidate `060beb6fdfb741d99a6ec8730f6e76ad2d873fd7:docs/roadmap/FOX2_BRIDGE_RC1_Q1_SELECTIVE_ADMISSION_SOURCE_IMPACT_CANDIDATE_20261020.md`; offline route decision `2c130ce37f15ad32f987d5616ada561fed076f1d:docs/roadmap/FOX2_BRIDGE_OFFLINE_DEV_ROUTE_DECISION_20261020.md`; native addendum `9106e8d4465db5f313911394579da9d39f296f73:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ROUTE_ADDENDUM_CANDIDATE_20261020.md`.
6. Current Bridge/Canary source status: Canary009 `work/FOX2-BRIDGE-FINAL-CANARY-009@501822a33ef08c7365154913bbc677544856eee5` HOLD; Control `work/FOX2-DISPATCH-chat@3f885b2d24cb131b5e96dfdb67a44677599197e2` frozen; existing COMPAT001 is published/HOLD/no replay. `INTERNAL_FOX2_BRIDGE_READY=NOT_ATTESTED`. No source adoption claim.

## Exact allowed changed paths

**Code/test** (only these six):
- `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
- `agent_bridge/src/fox2_agent_bridge/app.py`
- `agent_bridge/src/fox2_agent_bridge/__main__.py`
- `agent_bridge/tests/test_project_dictionary.py`
- `agent_bridge/tests/test_e2e_runner.py`

**Report/evidence** (only):
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/test_summary.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/diff_trace.json`

If a meaningful change genuinely requires `ledger.py`, `desktop.py`, `ops_runner.py`, config, schema, generated files, or other code/test paths: **STOP the implementation at that boundary**. Report evidence and the proposed exact dependency+K1 justification, but do not modify or stage it. No implicit expansion.

## Implementation objective and acceptance

Implement a **real, explicit operator-started MANUAL_LOCAL entrypoint** on the shared Bridge validation/adapter/checkpoint path, **for offline synthetic tests only** at this stage. Do not build a second cloned execution engine. Preserve `BRIDGE` automatic path and its rejection of `MANUAL_LOCAL` from normal auto selection. Fail closed on failed/unknown authority, WRONG schema/route/model/effort, source/prompt/branch/worktree hash drift, missing permissions, busy Worker lock, `PAUSED`/`stop_requested`, ledger claim previously seen in current/legacy/marker, non-atomic pre-spawn claim or ambiguous recovery. `stop_requested=true` always denies new Agent. Preserve paused semantics; never bypass by calling `honor_controls=False`, editing SQLite, resetting pause, or running installed Worker. If the existing ledger's atomicity cannot achieve these guarantees within the six-file scope, STOP and report the exact missing contract rather than shipping an unsafe partial path.

**Tests**: synthetic fixture/disposable remote, no actual published COMPAT001 or Canary009 IDs; positive one-shot manual path; negative BRIDGE auto-selection; pause/stop; persisted no-replay, legacy marker and candidate discovery; source hash/model/Owner drift; two concurrent claims; crash-before/after claim and after spawn; no silent retry; report/path K1 changed-file controls. Run scoped `pytest` and applicable wider regression tests without mutating installed Bridge. No pre-existing PASS counts may substitute. Preserve old PreExec v1, Dictionary v1.2/v1.3 scoped semantics and Canary v0.6 compatibility. If unavailable or failed, report true status not PASS.

**K1**: each material diff hunk classified `REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED` in `diff_trace.json`, exact path, reason, consumer/test. No drive-by refactor.

**Delivery**: AGENT stages/commits/pushes **only** exact allowed paths to CODE_BRANCH, verifies origin remote commit, changed path allowlist, test outcomes and remote report bytes; presents observed result remote SHA **outside committed file** to CHAT. Include `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md` and `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json`, even if blocked, truthfully recording missing evidence. No self-referential result commit hash in the committed manifest. No direct acceptance or git merge.

## STOP / no-op / no-replay

Before any implementation: verify exact CODE_BRANCH/HEAD/worktree clean, no competing writer, no previously started matching native attempt in allowed worktree/evidence, current origin remote SHA same exact CODE_START_SHA, correct CLI exact model/effort/sandbox and granted permissions, exact Git prompt SHA/commit. **DO NOT execute** if any check unknown/mismatched. Never run `fox2-bridge worker`, `control resume`, `e2e-once`, `run-next`, `manual-once` on installed runtime, Git push to main, merge, Canary, live provider or broker, secrets/auth output, destructive reset, auto retry, or operate beyond isolated code/tests. Treat host CLI access as one coding Agent attempt; if uncertain, no second run without CHAT reconciliation.
