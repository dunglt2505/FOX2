# FOX2 Bridge — CHAT scoped intake of consumed Internal Validation 001

Date: 2026-10-23
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Source: Owner-provided PowerShell console output from `owner_integrated_validation.ps1` at `68c648fc0abcfa787a7f40cc96669fbd1715a144`.
A04 package: `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`.
R5 code source: `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf`, CHAT_ACCEPT `1ef5506d592cc7da9c93e61d86a158c12b9b27b3`.

## Observed result — no retcon / no replay

- `FOX2_PATCHED_RUNNER_IDENTITY=PASS`; `FOX2_INTERNAL_VALIDATION_PRECONSUME=PASS`.
- `FOX2_A04_PACKAGE_REUSE=VERIFIED`; entry WPF count 0.
- `FOX2_INTERNAL_ATTEMPT_CONSUMED=TRUE`, attempt `FOX2-BRIDGE-INTERNAL-VALIDATION-001`; permanently **NO_REPLAY**.
- The actual Owner-host stdout emitted `USER_LIFECYCLE=PASS` and `FOX2_INTEGRATED_LIFECYCLE=PASS` after the accepted certifier and same-package lifecycle checks. This is **PASS_OBSERVED**, not an independent Git readback of private `lifecycle_local.json`. Its local proof must still match when reused.
- `RESTART_PRESENTATION_TRIAL` was **STARTED and FAILED** (`RuntimeException`), NOT a pristine unattempted gate, notwithstanding the old summary field `presentation_restart=NOT_RUN`.
- Original attempt only recorded a generic exception class; it did not retain the first failed predicate. Exact causal operation remains **UNKNOWN**. Do not claim a product defect or PASS for restart.
- G3 isolated-host privileged enforcement, G4 adoption, F1 Worker, Canary and LIVE all remain `NOT_RUN` or `HOLD`; `INTERNAL_FOX2_BRIDGE_READY=NOT_ATTESTED`.

## Scoping decision

**CHAT_SCOPED_INTAKE:** Preserve prior accepted R5, applicable historical A04 PASS, and observed current host lifecycle PASS. Overall Bridge remains `TEST / IN_PROGRESS`. Do not replay consumed attempt 001, rebuild A04 package, or repeat uninstall/reinstall.

The smallest safe continuation is a fresh **restart-only** native attempt inside the **same Whole-WP**, with a new immutable one-shot identity and no new Agent/code task. It may execute only after checking real Owner-host current state, exact package/source, prior consumed claim and local lifecycle evidence. If a WPF is already live, verify exact image/session and reuse rather than blindly launch twice. Only presentation singleton, UI, graceful exit, lock release, safe control and logical consumption preservation are permitted; fail closed on drift.

Prepared source on non-main: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/internal_validation/owner_restart_continuation_once.ps1`, initial publication commit `17978dd11f9a5916e1f7c6532e96639f2dacfd24`. This **does not** assert execution, runtime readiness, package mutation, G3/G4 rights or a status of PASS.

## Source/authority/safety

- Owner directive: continue Bridge under the existing Agile Lite Whole-WP; no replay of consumed attempt.
- Current operating process: Fast Lane INTERNAL_ONLY; no protected main/merge/deploy, no provider/broker/LIVE.
- Required: source-contracts, execution-recovery, route-preflight, result-acceptance, delivery; all applied proportionately.
- Publication sync: applied to non-main Git readback. Agent prompt-builder: NOT_APPLICABLE (CHAT-direct bounded native recovery, no CODEX/WORK task).
- Stop at the first material host failure; retain consumed claim/evidence, return sanitized code and stage to CHAT.

Status: `IN_PROGRESS / BRIDGE_LIFECYCLE_PASS_OBSERVED / RESTART_FAILED_NEEDS_BOUNDED_CONTINUATION / G3_G4_NOT_RUN / INTERNAL_READY_NOT_ATTESTED`.
