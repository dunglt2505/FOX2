---
name: fox2-feature-certification
description: Certify a FOX2 feature, not only Bridge, against independent requirements and evidence.
---

# fox2-feature-certification

## Agile Lite Owner-approved precedence

Current project management: Policy v2.1.0 and `../shared/operating_rules.md`. Ordinary internal task: goal, implementation, proportionate tests, CHAT review, DONE or REWORK. Mandatory old source lock/PreExec/Dispatch/extra review applies only to the actual Bridge or consequential execution path that requires it; do not impose Bridge gates on unrelated DEV. Preserve real security, no-replay, existing task pins and domain-specific assessment.

## Activate when
Task requests acceptance/readiness/certification of one feature.

## Work to perform
Trace approved BRD→TechSpec→contracts→tests→fixtures and actual installed/E2E results. Check negative, regression, security and state/time semantics; distinguish skipped/unrun/failed. Independent reviewer only when required.

## Completion / stop
Per-gate evidence matrix and acceptance verdict; partial success never passes whole feature.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** Feature acceptance/readiness certification, or evidence-based transition across SDLC gates.
- **PRECONDITIONS:** Feature ID, authorized BRD/TechSpec/contracts and applicable acceptance matrix/source binding.
- **REQUIRED_ACTIONS:** Trace each requirement to code/tests/evidence and runtime stage; validate negative, regression, security and skipped/unrun cases.
- **REQUIRED_EVIDENCE:** Immutable source/results, actual CI/tests and CHAT acceptance receipts with coverage of required acceptance gates.
- **DELIVERABLES:** Feature gate matrix, uncovered tests, stage transition verdict (`ACCEPT`/`PARTIAL`/`HOLD`) and references.
- **VALIDATION:** Check every required gate independently; no inference from code existence, partial tests, self-report or offline runtime.
- **FAILURE_STATE:** `FEATURE_NOT_VERIFIED` / `GATE_NOT_RUN` / `ACCEPTANCE_HOLD` for missing coverage.
- **COMPLETION_GATE:** All applicable acceptance gates evidenced or explicit bounded HOLD; do not promote TEST/DEPLOY/LIVE without authority.
## Source and result provenance
Bind feature requirements to Dictionary-selected effective BRD, TechSpec, contracts, acceptance and source commits. Require CHAT's actual Git result intake/ACCEPT or bounded Owner waiver, never Agent self-acceptance or unrun test PASS. Distinguish offline DEV, integration test and installed/Canary/release stages. Product feature completion is measured by working code, real test outputs and acceptance evidence rather than Dispatch/receipt count.

## Feature SDLC stage transition evidence rules (v0.3.5)
Independently determine exit gates: PLAN→DESIGN needs authorized objective/scope; DESIGN→BUILD needs approved requirements/TechSpec/contracts and acceptance applicable to feature; BUILD→TEST needs source/code delivery, integrity, required build evidence and CHAT intake; TEST→DEPLOY needs feature-specific tests and actual acceptance, with `NOT_RUN` preserved; DEPLOY→MAINTAIN needs actual authorized target-environment adoption and stage-specific receipt. A feature may have concurrent tests during BUILD without prematurely promoting its Stage. Do not equate offline localhost with Canary/LIVE, CI with owner approval, or no result with fail/pass. When invoked on an unlabelled feature, route to status-roadmap for evidence-based initialization, only commit if expressly authorized to write.


## v0.3.7 — Domain-specific bounded recovery
Maintain gate-level status and dependency links. Preserve immutable historical PASS, label current applicability separately, and keep final certification HOLD if mandatory stage gates remain FAIL/NOT_RUN. Test only affected and freshness-required gates, including full suite when independently mandated.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
