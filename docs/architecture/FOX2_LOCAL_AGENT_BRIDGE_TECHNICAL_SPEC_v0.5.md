# FOX2 — Local Agent Bridge Technical Specification v0.5

**Document ID:** `FOX2-LOCAL-AGENT-BRIDGE-SPEC`  
**Version:** `0.5`  
**Project:** `FOX2 ONLY`  
**Status:** `RELEASED_EFFECTIVE / BOOTSTRAP_TRUST_ENABLED / HARDENED_TRUST_DEFERRED`  
**Date:** 2026-10-13  
**Purpose:** Enable the FOX2 Local Agent Bridge to progress through the current build/bootstrap stage without requiring production-grade GitHub App publisher provenance, while preserving the stronger v0.4 trust design as the mandatory hardening target before confidential/private or Production/LIVE operation.  
**Released predecessor:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4.md` — immutable historical release. v0.5 supersedes v0.4 for **new Bridge handoffs** after verified Library publication/manifest and exact Git mirror readback. Existing accepted evidence remains immutable and is reused unless a changed assumption materially affects it.  
**Governance authority:** FOX2 Policy **V1.8.4 RELEASED_EFFECTIVE**.  
**Owner decision:** 2026-10-13 — simplify Bridge bootstrap trust so the project can run during the current build stage; do not require dedicated GitHub App publisher proof as a prerequisite to bootstrap execution.  
**Authority boundary:** This Technical Specification changes execution mechanics only. It does not grant DEV, Git code push, merge, provider production, broker write, deployment or LIVE rights.

---

## 1. Incorporation rule

All sections of Bridge Technical Spec v0.4 remain effective **except where this v0.5 explicitly supersedes them**.

This v0.5 supersedes:

- v0.4 §6.3 `TrustAnchorVerifier` trust-mode selection;
- v0.4 Gate A interpretation in §25;
- v0.4 readiness/disposition statements that made dedicated `GITHUB_APP + ENFORCED_CONTROL_REF` a prerequisite for any automated Bridge bootstrap execution;
- any v0.4 text that would block the infrastructure-building bootstrap solely because hardened publisher provenance is not yet installed.

The v0.4 component model, schema validation, replay protection, runtime attestation, worktree isolation, Agent routing, result inspection, delivery verification, review outbox/queue/receipt lifecycle and Gates B–F remain unchanged unless separately revised.

---

## 2. Architecture–Stage Alignment

```yaml
architecture_stage_alignment:
  applicable_policy: FOX2 Policy V1.8.4 RELEASED_EFFECTIVE
  business_requirement_source: NOT_APPLICABLE_FOR_BRIDGE_TRUST_MECHANISM
  technical_source: FOX2 Local Agent Bridge Technical Spec v0.5
  target_architecture: CHAT -> Git dispatch -> Local Bridge -> Copilot/Codex -> Git result -> CHAT review
  actual_stage: BOOTSTRAP
  observed_capabilities:
    - repository dunglt2505/FOX2 is PUBLIC
    - CHAT has authenticated GitHub repository write access
    - control branch work/FOX2-LOCAL-DISPATCH-chat exists
    - exact commit/path/blob readback is available
    - Bridge source/runtime is not yet fully operational/certified
  unmet_dependencies_or_gates:
    - BRG-003 source baseline acceptance
    - BRG-010..040 implementation/runtime acceptance
    - hardened trust before private/proprietary/Production/LIVE stage
  execution_path_class: BOOTSTRAP_PATH
  path_reason: Bridge is currently building the infrastructure that will later enforce the target trust model; requiring that completed hardening to build itself is a bootstrap paradox
  target_transition: BOOTSTRAP_GATE_A -> Gate B -> HARDENED_GATE_A before confidential/private/Production-LIVE operation
  fallback_retirement_condition: BOOTSTRAP_TRUST retires before confidential/proprietary code or private production operation
  alignment_verdict: PASS_BOOTSTRAP
```

---

## 3. Two trust levels

### 3.1 `BOOTSTRAP_TRUST` — active for current FOX2 build stage

Selected mechanism:

```text
CHAT_PINNED_CONTROL_REF + IMMUTABLE_COMMIT + HASH_BINDING + REPLAY_GUARD
```

Trust anchor for the current public bootstrap stage is the combination of:

1. exact repository `dunglt2505/FOX2`;
2. exact control branch `work/FOX2-LOCAL-DISPATCH-chat`;
3. authenticated CHAT GitHub publication through the currently connected repository write channel;
4. immutable remote commit SHA containing the dispatch artifact;
5. exact task, prompt, Policy, Technical Spec and source hashes bound inside the dispatch;
6. Owner decision/selection receipt identifier bound to the task/dispatch;
7. durable single-use `dispatch_id` replay protection;
8. runtime revalidation immediately before Agent launch;
9. allowlist/denylist and exact worktree/base/writer checks;
10. independent CHAT remote readback after result publication.

For `BOOTSTRAP_TRUST`, **dedicated GitHub App provenance and enforced control-ref ruleset are NOT prerequisites**.

Repository visibility being public does not grant arbitrary users write access. However, because this mode does not cryptographically distinguish CHAT from every other possible repository writer, it is intentionally classified as **bootstrap assurance**, not hardened production provenance.

### 3.2 `HARDENED_TRUST` — mandatory later

The v0.4 selected target remains the hardening target:

```text
GITHUB_APP + ENFORCED_CONTROL_REF
```

`HARDENED_TRUST` becomes mandatory before the earliest of:

- FOX2 returns from Public Bootstrap to Private and automated Bridge dispatch is expected to continue;
- proprietary/confidential strategy, risk, decision, exit/profit-protection or other sensitive IP is placed in the automated execution path;
- provider-restricted/non-public operational data is handled;
- broker/account/order-write capability is introduced;
- Production or LIVE operation is considered.

Hardening may use GitHub App + ruleset as in v0.4, or a future independently released equivalent/stronger mechanism. It must be objectively evidenced at that time.

---

## 4. Superseding TrustAnchorVerifier behavior

For the current bootstrap mode, `TrustAnchorVerifier` MUST verify before launch:

- `project == FOX2`;
- repository exactly `dunglt2505/FOX2`;
- configured control ref exactly `refs/heads/work/FOX2-LOCAL-DISPATCH-chat`;
- dispatch file is read from a concrete immutable commit SHA, never mutable branch-tip content alone;
- the immutable commit is reachable from the configured control branch when claimed;
- task/prompt/Policy/Technical Spec/source hashes match the dispatch binding;
- Owner decision/selection receipt ID/hash matches the task record;
- `max_runs == 1`;
- `dispatch_id` has not been previously claimed or executed;
- base/branch/worktree/allowlist exactly match the authorized WP;
- no conflicting writer or dirty/WIP condition exists immediately before launch;
- no scope expansion occurred after CHAT's decision.

It MUST reject:

- dispatch from another repository/ref;
- dispatch read only by mutable branch name without immutable commit identity;
- hash mismatch;
- stale/superseded task source where the handoff requires a newer released source;
- duplicate/replayed `dispatch_id`;
- moving-base mismatch;
- altered Owner decision binding;
- unauthorized paths;
- runtime writer collision;
- any Production/LIVE permission not separately granted.

Bootstrap rejection code:

```text
LOCAL_RUNTIME_BLOCKED / BOOTSTRAP_TRUST_VALIDATION_FAILED
```

---

## 5. BOOTSTRAP Gate A

### 5.1 Gate definition

```text
CHAT authenticated Git publication
    -> exact FOX2 control branch
    -> immutable dispatch commit
    -> Bridge fetch/read
    -> schema/hash/source/decision/replay validation
```

No Agent launch is permitted until all validation steps above pass.

### 5.2 Required bootstrap evidence

`BOOTSTRAP_GATE_A` requires:

1. CHAT can publish an inert dispatch canary to the exact control branch;
2. remote commit SHA and dispatch blob are independently read back;
3. branch ancestry confirms the canary commit belongs to the configured control ref;
4. Bridge `DispatchPoller` discovers only the configured path/ref;
5. `DispatchValidator` validates schema + project + repo + hashes + `max_runs`;
6. `TrustAnchorVerifier` validates immutable commit + source/decision binding;
7. `ReplayGuard` accepts once and rejects replay;
8. malformed repo/ref/hash/decision fixtures fail closed;
9. RuntimeAttestor rechecks actual local branch/base/worktree/writer facts before launch.

`BOOTSTRAP_GATE_A=PASS` means the build-stage dispatch path is operational. It does **not** mean production-grade publisher provenance exists.

### 5.3 Hardened Gate A status

Track separately:

```text
BOOTSTRAP_GATE_A = PASS | BLOCKED | NOT_RUN
HARDENED_GATE_A  = PASS | BLOCKED | NOT_RUN
```

Do not collapse them into one ambiguous flag.

---

## 6. Public Bootstrap risk boundary

The Owner accepts the following limited risk for speed during the current build stage:

- a repository writer with sufficient Git permission could potentially attempt to publish a forged dispatch;
- bootstrap trust therefore relies on repository write access plus exact commit/hash/decision/replay controls rather than dedicated service identity provenance;
- all bootstrap execution remains bounded to development WPs and non-sensitive source;
- no broker write, no Production, no LIVE and no confidential/proprietary execution path is authorized by this choice.

This risk acceptance is **stage-bounded**. It does not waive future hardening.

---

## 7. Existing public Ruleset 24990489

Observed ruleset `24990489 / FOX2 Dispatch Control Trust` is **not part of BOOTSTRAP_TRUST acceptance** because its current configuration does not match the exact real control branch and uses a DeployKey bypass rather than the intended App/Integration identity.

Therefore:

- it MUST NOT be cited as Gate A proof;
- it does not block bootstrap execution;
- it may be corrected, replaced or removed later during `HARDENED_TRUST` work;
- no further Owner action on that ruleset is required for current bootstrap progress.

---

## 8. BRG work-package effect

### BRG-003

Purpose remains sanitized source-baseline import into `agent_bridge/**`, preserving all previously accepted inventory/hash/security evidence. No App/ruleset proof required.

### BRG-010

Bridge Core + config must expose a trust-mode setting:

```text
trust_mode = BOOTSTRAP_PINNED_GIT
```

Future hardened value:

```text
trust_mode = HARDENED_PUBLISHER
```

Default during current public bootstrap release:

```text
BOOTSTRAP_PINNED_GIT
```

### BRG-020

Poll exact control branch/ref and dispatch path only.

### BRG-030

Implement schema/hash/decision/replay validation and the superseding Bootstrap TrustAnchorVerifier behavior above.

### BRG-040

RuntimeAttestor verifies actual local runtime/worktree/writer/tool/Agent facts immediately before launch.

BRG-010..040 may be accepted into `BOOTSTRAP_GATE_A` without dedicated GitHub App provenance.

### BRG-050..080

Remain Gate B and continue only after `BOOTSTRAP_GATE_A=PASS`.

### Later hardening WP

Before the hardening deadline, create a separately tracked Bridge trust-hardening WP to implement/certify `HARDENED_TRUST` without rewriting accepted bootstrap history.

---

## 9. Acceptance additions

Add the following current-stage acceptance cases:

- `AC-BRG-BTA-01`: correct repo/ref + immutable commit + all hashes valid -> accept once.
- `AC-BRG-BTA-02`: same `dispatch_id` replay -> reject.
- `AC-BRG-BTA-03`: same ID with different payload -> reject/conflict.
- `AC-BRG-BTA-04`: wrong repository -> reject.
- `AC-BRG-BTA-05`: wrong control ref -> reject.
- `AC-BRG-BTA-06`: mutable tip differs after claim but claimed commit remains immutable -> continue only from claimed commit; never silently switch.
- `AC-BRG-BTA-07`: task/prompt/source/Policy hash mismatch -> reject.
- `AC-BRG-BTA-08`: Owner decision receipt mismatch -> reject.
- `AC-BRG-BTA-09`: branch/base/worktree drift -> runtime block before launch.
- `AC-BRG-BTA-10`: path allowlist expansion -> reject.
- `AC-BRG-BTA-11`: Production/LIVE fields self-declared without separate grant -> reject.
- `AC-BRG-BTA-12`: inert CHAT canary remote SHA/blob/ancestry readback -> pass transport publication only, no Agent launch.

Hardening acceptance from v0.4 remains deferred, not deleted.

---

## 10. Release / readiness disposition

```text
POLICY_V1.8.4=RELEASED_EFFECTIVE
BRIDGE_SPEC_V0.4=SUPERSEDED_FOR_NEW_BRIDGE_HANDOFFS_AFTER_V0.5_RELEASE
BRIDGE_SPEC_V0.5=RELEASED_EFFECTIVE_AFTER_LIBRARY+MANIFEST+GIT_READBACK
REPO_VISIBILITY=PUBLIC
CONTROL_BRANCH=EXISTS
BOOTSTRAP_TRUST_MODE=ENABLED
DEDICATED_GITHUB_APP_PROVENANCE=DEFERRED_HARDENING
RULESET_24990489=NON_AUTHORITATIVE_FOR_BOOTSTRAP
BOOTSTRAP_GATE_A=NOT_RUN_PENDING_BRG010_040_RUNTIME_VALIDATION
HARDENED_GATE_A=NOT_RUN_DEFERRED
GATE_B=NOT_RUN
MERGE=NO
PROVIDER_PRODUCTION=NO
BROKER_WRITE=NO
LIVE=NO
```

STOP on source/hash/decision mismatch, replay/conflict, wrong repo/ref, moving base, worktree/writer collision, secret exposure, unauthorized path, failed remote readback, or any attempted Production/LIVE escalation.

---

## 11. Why v0.5 exists

v0.4 correctly described the stronger end-state but made its production-grade publisher proof a prerequisite too early in the lifecycle. Under Policy V1.8.4's Architecture–Stage Alignment and bootstrap-paradox rule, the current task is to **build the Bridge that will later enforce the stronger trust path**. v0.5 therefore separates build-stage trust from production hardening instead of blocking the build on infrastructure that does not yet exist.