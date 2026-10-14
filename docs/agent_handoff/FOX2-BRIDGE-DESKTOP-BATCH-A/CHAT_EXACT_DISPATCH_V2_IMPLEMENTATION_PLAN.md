# CHAT Exact Implementation Plan — Bridge Batch A Dispatch v2 Compatibility

**WP:** `BRIDGE-DESKTOP-BATCH-A`  
**State:** same-WP material rework; no new WP  
**Target result base:** `26fdc0af7317a675b618982575f3ee64429a991f` plus CHAT rework handoff commits  
**Governance:** Policy V1.8.6 + Routing V1.2.7 + Dispatch Schema v2 + Protocol v9  
**Goal:** make Bridge accept current FOX2 Dispatch v2 end-to-end while retaining legacy 0.6 compatibility, without duplicating the execution engine.

## 1. Root cause to fix once

Current Bridge Batch A implementation has four coupled compatibility gaps:

1. `BridgeE2ERunner._validate_dispatch` hard-requires `schema_version == "0.6"`.
2. `BridgeConfig.CONTROL_BRANCH` is fixed to legacy `work/FOX2-LOCAL-DISPATCH-chat`, while current v2 dispatches are published to the v2 control lane.
3. `dispatch_poller.CANDIDATE_PATH_PATTERN` only discovers legacy:
   `docs/agent_handoff/<WP>/dispatch/<file>.json`.
4. Existing v2 control files 001/002 used transitional filenames that do not equal the canonical `dispatch_id + ".json"`; they are historical and MUST NOT be made executable by relaxing dispatch-id path identity.

Fix these as one compatibility boundary. Do not add a second execution engine and do not fork behavior by schema after normalization.

## 2. Stable current control branch

Current v2 control branch for new Bridge execution is:

`work/FOX2-DISPATCH-chat`

CHAT created it from the prior v2 control history.

Legacy control branch remains:

`work/FOX2-LOCAL-DISPATCH-chat`

Required behavior:

- default Bridge config -> `work/FOX2-DISPATCH-chat`;
- legacy branch may be selected only explicitly for historical/compatibility use;
- arbitrary control branches remain rejected;
- do not scan both branches in one Worker loop.

Suggested constants in `config.py`:

```python
CONTROL_BRANCH = "work/FOX2-DISPATCH-chat"
LEGACY_CONTROL_BRANCH = "work/FOX2-LOCAL-DISPATCH-chat"
SUPPORTED_CONTROL_BRANCHES = frozenset({CONTROL_BRANCH, LEGACY_CONTROL_BRANCH})
```

Then change `BridgeConfig.__post_init__` from exact-equality-to-one-constant to membership in `SUPPORTED_CONTROL_BRANCHES`.

Do not make control branch unrestricted.

## 3. Candidate discovery

Keep legacy discovery and add current v2 discovery.

Accepted external paths:

```text
LEGACY:
docs/agent_handoff/<WP_SEGMENT>/dispatch/<DISPATCH_ID>.json

V2:
docs/agent_handoff/DISPATCH_V2/<DISPATCH_ID>.json
```

Canonical filename rule for BOTH:

`basename == dispatch_id + ".json"`

Do not relax this rule to support transitional 001/002 filenames. Those are evidence/history only.

Implementation option: replace the single bytes regex with either:

- two explicit regexes and `_candidate_path()` returns any-match; or
- one union regex.

Keep names constrained to existing safe character class.

Add direct poller parser tests for:
- legacy accepted;
- canonical v2 accepted;
- transitional v2 filename accepted by tree pattern only if syntactically safe but later rejected by dispatch-id identity OR preferably rejected at path convention if feasible;
- unrelated JSON rejected;
- nested arbitrary folders rejected.

## 4. Validation architecture

Refactor current `_validate_dispatch` into three conceptual stages:

```text
raw UTF-8 JSON
  -> identify external schema
  -> normalize external schema to ONE internal payload
  -> run ONE common normalized validator
  -> execution engine
```

Suggested functions:

```python
def _decode_dispatch(raw: bytes) -> dict[str, object]: ...
def _normalize_legacy_v06(self, external: dict[str, object]) -> dict[str, object]: ...
def _normalize_dispatch_v2(self, external: dict[str, object]) -> dict[str, object]: ...
def _validate_normalized_dispatch(
    self,
    payload: dict[str, object],
    *,
    dispatch_path: str,
    observed_blob_sha: str,
    raw: bytes,
) -> dict[str, object]: ...
```

`_validate_dispatch` should only dispatch on schema:

```python
schema = external.get("schema_version")
if schema == "0.6":
    normalized = self._normalize_legacy_v06(external)
elif schema == "2.0":
    normalized = self._normalize_dispatch_v2(external)
else:
    raise DispatchInvalid("unsupported dispatch schema_version")
return self._validate_normalized_dispatch(...)
```

Do not duplicate worktree/result/publication logic by schema.

## 5. Legacy 0.6 normalization

Legacy behavior must remain byte/semantic compatible with the currently passing suite.

The legacy normalizer may mostly copy the external payload and set:

```python
normalized["_external_schema_version"] = "0.6"
```

Existing default `delivery_owner=BRIDGE` for legacy dispatches may remain for historical compatibility where the field is absent.

Do not retroactively reinterpret old immutable dispatches as v2.

## 6. Dispatch v2 -> internal field mapping

For a Bridge-executed v2 dispatch, require:

```text
schema_version       = "2.0"
project              = "FOX2"
dispatch_action      = "EXECUTE_LOCAL_AGENT"
workspace_id         = "FOX2_LOCAL"
execution_path       = "BRIDGE"
max_runs             = 1
```

A v2 dispatch with `execution_path=MANUAL_LOCAL` or `VSCODE_ONE_CLICK` MUST NOT be auto-executed by Bridge.

Exact mapping:

| v2 external | normalized internal |
|---|---|
| `dispatch_id` | `dispatch_id` |
| `wp_id` | `wp_id` |
| `runtime_contract.repo` | `repository` |
| configured actual control branch | `control_ref = refs/heads/<control_branch>` |
| `target_agent` | `agent.product` |
| target Agent registry | `agent.interface` |
| `routing.model_policy` | `agent.model_policy` |
| `routing.auto_tier` | `agent.auto_tier` |
| `routing.model` | `agent.model` |
| `routing.reasoning_effort` | `agent.reasoning_effort` |
| `routing.permission_profile` | `agent.permission_profile` and normalized top-level `permission_profile` |
| `runtime_contract.worktree` | `worktree` |
| `runtime_contract.branch` | `branch` |
| `runtime_contract.base_sha` | `base_sha` |
| `prompt` | `prompt` |
| `runtime_contract.allowed_code_paths` | `allowed_code_paths` |
| `runtime_contract.allowed_report_paths` | `allowed_report_paths` |
| `permissions` | `permissions` |
| `delivery_owner` | `delivery_owner` |
| `runtime_contract` | preserve `runtime_contract` |
| `required_tests` | preserve `required_tests` |

For downstream adapter execution, normalize internal:

```python
execution_path = _AGENT_EXECUTION_PATHS[target_agent]
```

and preserve original external path separately, e.g.:

```python
normalized["_dispatch_execution_path"] = "BRIDGE"
normalized["_external_schema_version"] = "2.0"
```

This avoids confusing the Dispatch-v2 orchestration path enum with the internal Agent adapter path.

## 7. v2 governance/runtime fields to validate, not re-decide

Bridge must verify structural/technical consistency but MUST NOT rerun CHAT governance.

Validate at least:

### Policy
- object exists;
- `version == "1.8.6"` for current schema v2;
- `git_path == "docs/governance/FOX2_POLICY_V1.8.6.md"`;
- `git_commit_sha` = full SHA;
- `sha256` = 64 lowercase hex.

Do not fetch/re-approve Policy semantics.

### Task
- object exists;
- path under `docs/agent_handoff/**/task.md`;
- commit full SHA;
- sha256 64 hex.

### Prompt
Keep existing immutable prompt validation:
- path under `docs/agent_handoff/`;
- git commit full SHA;
- blob SHA1 40 hex;
- SHA256 64 hex.

### Source
- `commit_sha` full SHA;
- `git_source_ready == "YES"`.

### Decision receipt
Require current execution fields to be already authorized:

```text
policy_check             = PASS
task_state_check         = PASS
source_binding_check     = PASS
routing_r0_r7            = PASS
assignment_check         = PASS
material_capability_check in {PASS, PASS_NON_MATERIAL_DEVIATION}
execution_authorized     = YES
code_allowed             = YES
```

Bridge verifies these literal values only. It does not recompute them.

### Permissions
Reuse common validator:
- code_allowed true;
- git_code_push true;
- git_report_write true;
- git_report_push true;
- pr_create false;
- merge_allowed false;
- production_provider false;
- broker_write false;
- live false.

Also require:
`decision_receipt.code_allowed == "YES"` iff normalized `permissions.code_allowed is True`.

### Repository/runtime
- `runtime_contract.repo == "dunglt2505/FOX2"`;
- branch/worktree/base/path validation uses current common validator;
- allowed code/report lists preserve exact order/values;
- required_capabilities is a list of non-empty unique strings;
- stop_conditions is a list of non-empty unique strings.

Do not invent semantic capabilities not declared by CHAT.

## 8. Agent routing validation

Build v2 normalized Agent object:

```python
{
  "product": target_agent,
  "interface": _AGENT_INTERFACES[target_agent],
  "model_policy": routing["model_policy"],
  "auto_tier": routing.get("auto_tier"),
  "model": routing.get("model"),
  "reasoning_effort": routing.get("reasoning_effort"),
  "permission_profile": routing["permission_profile"],
}
```

Then pass through existing `validate_selection()`.

Mandatory fail-closed cases:
- CODEX + NATIVE_AUTO;
- PINNED without model;
- COPILOT Native Auto with non-auto explicit model;
- non-FULL_ACCESS permission for this current Bridge baseline;
- invalid reasoning for Copilot;
- target Agent mismatch with normalized interface;
- routing permission mismatch with permissions/Agent.

No Agent substitution.

## 9. Copilot shell compatibility

Do NOT reintroduce bounded-shell semantics as the v2 primary permission model.

Under current Policy V1.8.6, `FULL_ACCESS` Copilot uses:
- allow-all-tools;
- allow-all-paths;
- allow-all-urls.

Therefore for v2 normalized payload:
- preserve `runtime_contract.required_capabilities`;
- set legacy `_copilot_shell_tools=[]` unless a future schema explicitly adds a safe-catalog field;
- rely on Full Access preflight and task/test contract;
- do not infer a shell allowlist from arbitrary `required_capabilities` strings.

Legacy 0.6 `runtime_contract.dev_shell_capabilities` behavior remains unchanged.

## 10. Canonical dispatch path identity

Common validator must still require:

`dispatch_path.endswith("/" + dispatch_id + ".json")`

For current v2 execution publish canonical files like:

`docs/agent_handoff/DISPATCH_V2/FOX2-DISPATCH-...-003.json`

Do not weaken identity to accommodate transitional files with alternate filenames.

## 11. Tests to add

Prefer `agent_bridge/tests/test_dispatch_v2.py` for v2-specific coverage, plus minimal updates to poller/config tests.

Required tests:

### V2 positive
1. `test_v2_codex_dispatch_normalizes_exact_tuple`
   - BRIDGE execution path;
   - CODEX/PINNED/gpt-6.1-sol/high/FULL_ACCESS;
   - exact runtime branch/worktree/base/write paths;
   - AGENT owner.

2. `test_v2_copilot_native_auto_normalizes_exact_tuple`
   - COPILOT/NATIVE_AUTO/balance;
   - normalized model auto;
   - no reasoning;
   - FULL_ACCESS;
   - no inferred legacy shell tools.

3. `test_v2_bridge_owner_preserved`
4. `test_v2_agent_owner_preserved`

### V2 negative/fail closed
5. MANUAL_LOCAL rejected by Bridge.
6. VSCODE_ONE_CLICK rejected by Bridge.
7. repository mismatch rejected.
8. policy/task/source malformed identity rejected.
9. any decision receipt non-PASS rejected.
10. `code_allowed` receipt/permission mismatch rejected.
11. merge/provider/broker/live true rejected.
12. permission profile mismatch rejected.
13. PINNED missing model rejected.
14. target-agent/routing inconsistency rejected.
15. missing/duplicate invalid required capabilities/list shapes rejected.
16. filename does not equal dispatch_id rejected.
17. unsupported schema rejected before Agent spawn.

### Control/poller
18. default config uses `work/FOX2-DISPATCH-chat`.
19. explicit legacy control branch allowed.
20. arbitrary control branch rejected.
21. v2 canonical path discovered.
22. legacy canonical path still discovered.
23. unrelated JSON ignored.

### End-to-end normalized reuse
24. v2 AGENT owner uses only Agent publication path.
25. v2 BRIDGE owner uses only Bridge publication path.
26. v2 replay remains blocked.
27. v2 post-start quota/auth/capacity remains NEEDS_RECONCILIATION.
28. legacy 0.6 existing full suite remains PASS.

Do not duplicate every old execution test if normalized common-path coverage proves reuse.

## 12. Result/evidence update

Update existing Batch A report and manifest, not a new report tree.

Add:

```text
DISPATCH_V2_RUNTIME_COMPATIBILITY=PASS
V2_CONTROL_BRANCH=PASS
V2_DISPATCH_DISCOVERY=PASS
V2_NORMALIZATION_SINGLE_EXECUTION_PATH=PASS
LEGACY_V06_COMPATIBILITY=PASS
```

Evidence must include:
- focused v2 tests;
- full Bridge suite;
- exact final changed paths;
- secret scan;
- canonical text hygiene;
- `git diff --check`.

Keep pre-existing Batch A PASS evidence where still valid; regenerate manifest hashes for changed evidence/code.

## 13. Non-goals

Do NOT:
- redesign Policy;
- change Dispatch Schema v2;
- add another governance service;
- remove legacy 0.6 validator support;
- support arbitrary control branches;
- make transitional 001/002 filenames executable;
- add multi-branch polling;
- change main/merge/provider/broker/LIVE rights;
- start Batch B packaging.

## 14. Expected minimal implementation surface

Likely code files:
- `agent_bridge/src/fox2_agent_bridge/config.py`
- `agent_bridge/src/fox2_agent_bridge/dispatch_poller.py`
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`

Likely tests:
- new `agent_bridge/tests/test_dispatch_v2.py`
- small additions to existing config/poller/e2e tests if needed.

Evidence/report:
- existing `reports/BRIDGE-DESKTOP-BATCH-A/**`.

Avoid unrelated refactor.

## 15. Definition of done

```text
DISPATCH_V2_RUNTIME_COMPATIBILITY=PASS
V2_CONTROL_BRANCH=PASS
V2_DISPATCH_DISCOVERY=PASS
V2_NORMALIZATION_SINGLE_EXECUTION_PATH=PASS
LEGACY_V06_COMPATIBILITY=PASS
FULL_BRIDGE_TESTS=PASS
NO_REPLAY=PASS
NO_AGENT_SUBSTITUTION=PASS
GIT_DELIVERY_POLICY_ALIGNED=PASS
NO_DUPLICATE_PUBLICATION_PATH=PASS
PERMISSION_PREFLIGHT=PASS
CANONICAL_GENERATED_ARTIFACT_PIPELINE=PASS
TEXT_ARTIFACT_HYGIENE=PASS
CHANGED_PATH_ALLOWLIST=PASS
SECRET_SCAN=PASS
GIT_DIFF_CHECK=PASS
```

Then Agent commits/pushes exact same Batch A branch and returns one remote SHA for CHAT review.
