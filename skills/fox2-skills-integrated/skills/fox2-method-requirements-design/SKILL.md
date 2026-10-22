---
name: fox2-method-requirements-design
description: "Assess real BRD behavior changes and technical API/spec design impact together; merge BRD change control and TechSpec validation."
---

# fox2-method-requirements-design

**FOX2 Layer 2 — Domain methods — Agile Lite 0.5.0**

## Activate when
Business behavior, acceptance, API, interface or technical design actually changes.

## Input
Old/new user behavior, BRD acceptance, current TechSpec/API, affected consumers and tests.

## Work to perform
1. Identify true business semantic differences: users, threshold, timing, product behavior, failure cases and what counts as acceptance. Editorial/Policy-version changes alone do not open BRD change control.
2. Trace accepted business behavior to changed interfaces: types, units, schema, nullable/unknown, as-of timestamps, timeout, idempotency/concurrency, security and error contracts.
3. Map only affected producer/consumer dependencies and focused tests, including negative/regression. A retention change from 30→90 days requires changes to API/tests if they depend on it.
4. Distinguish design defect from code defect; preserve prior approved BRD/TechSpec versions when semantics are unchanged. Never spin each consumer into a governance micro-WP.
5. Report minimal impact and actionable acceptance. Technical publication, if explicitly required, is owned by Publication & Sync.

## Output
One concise business→design→consumer→tests impact and acceptance specification.

## Responsibility boundary
Owns requirement semantics and technical design correctness. Does NOT select source authority, implement code, publish docs or certify final results.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
