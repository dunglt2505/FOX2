---
name: fox2-project-health
description: Assess overall FOX2 project health using current evidence.
---

# fox2-project-health

## Agile Lite Owner-approved precedence

Current project management: Policy v2.1.0 and `../shared/operating_rules.md`. Ordinary internal task: goal, implementation, proportionate tests, CHAT review, DONE or REWORK. Mandatory old source lock/PreExec/Dispatch/extra review applies only to the actual Bridge or consequential execution path that requires it; do not impose Bridge gates on unrelated DEV. Preserve real security, no-replay, existing task pins and domain-specific assessment.

## Activate when
User asks FOX2 health, blockers, real progress or risks.

## Work to perform
Use bound source and actual commits, Dispatches, CI, evidence; separate confirmed completed vs in progress vs blocked vs not evaluated. Surface repeated failures for retrospective without inventing closure.

## Completion / stop
Evidence-cited health picture with next priority and owner, no stale summary claimed as live.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** Health/status/blocker/progress report for FOX2 overall or named scope.
- **PRECONDITIONS:** Target scope, as-of time and actual accessible Git/CI/task/result sources.
- **REQUIRED_ACTIONS:** Reconcile outcomes by CODE_IMPLEMENTED, TEST_EVIDENCED, PRODUCT_USABLE, ACCEPTED and RELEASED; identify blockers and critical path.
- **REQUIRED_EVIDENCE:** Observed commits, receipts, test status, source references and freshness/coverage limits.
- **DELIVERABLES:** Dated progress summary with evidence, real blockers, next priorities and named owner where known.
- **VALIDATION:** Independently check last reviewed commit and whether reported states reflect current task/result, not stale summary.
- **FAILURE_STATE:** `STATUS_NOT_VERIFIED` / `SOURCE_STALE` / `PARTIAL_COVERAGE` if current evidence missing.
- **COMPLETION_GATE:** Honest dated health report bounded by observation, no historic PASS presented as current state.
## Outcome-based reporting
Resolve real latest authorized operating references before asserting progress. Separate CODE_IMPLEMENTED, BUILD/TEST_EVIDENCED, PRODUCT_USABLE, ACCEPTED, and RELEASED from Git-document-only publication. Track Agent lifecycle: prompt Git published, Agent picked up, result Git pushed, CHAT reviewed. Missing result commit = no accepted implementation. CODE-FIRST priority from Owner's current decision; never show Bridge readiness as a blanket offline coding gate.


## v0.3.7 — Domain-specific bounded recovery
Preserve accepted work and separately report historical PASS, current reusable PASS and pending gates. One lifecycle FAIL is not broad product FAIL.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
