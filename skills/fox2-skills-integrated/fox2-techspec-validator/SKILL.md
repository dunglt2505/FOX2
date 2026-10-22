---
name: fox2-techspec-validator
description: Check technical interfaces and consumer compatibility when real behavior changes.
---

# fox2-techspec-validator

## Activate when
API, data contract, concurrency, error or deployment technical design changes.

## Work to perform
Map BRD acceptance to producer/consumer APIs, types, units, timeout, retry idempotency, null semantics, timestamps/as-of, error handling and negative/security tests. For Bridge changes check Dispatch parser, adapter, ledger claim, publication owner and PreExec consistency with actual installed Schema and contract. Verify focused integration tests, do not assume source version equality. Preserve prior TechSpecs when only governance Policy/Dictionary version changes; update only impacted contract and consumer.

## Completion / stop
Produce the concrete deliverable and actual proof with DONE/REWORK/BLOCKED or a precisely named lower execution state. Do not mark completed because a prompt, Dispatch, tool invocation or plan exists. CHAT owns the end-to-end result.

## Shared operating and Bridge applicability
Apply shared `../../shared/operating_rules.md`. A routine reversible independent native task needs no Bridge Dispatch, manual R0–R7 artifact or immutable prompt publication. When and only when the actual execution is Bridge-controlled, follow `../../shared/bridge_e2e_v041.md` and the **installed** runtime contract, not an assumed current version. All source/receipt/test evidence must be observed, not invented. Old consumed attempts remain immutable and non-replayable. Complete outcomes in the SAME logical task; do not create administrative micro-WPs.
