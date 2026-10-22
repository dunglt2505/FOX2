---
name: fox2-brd-change-control
description: Control real business requirement changes, not Policy/Dictionary version churn.
---

# fox2-brd-change-control

## Activate when
BRD business behavior, validation or acceptance conditions materially change.

## Work to perform
Identify semantics (who, behavior, threshold, timing, error), old/new acceptance, affected API/TechSpec/test consumers and migration. Example: retention 30→90 days requires actual API and test updates where dependent. Do not reopen BRD for Policy, routing or Dictionary version change that leaves business behavior unchanged. Preserve released prior bytes, approval and source with scoped new revision only when business semantics change. Report impacted tests and downstream owner, not an administrative micro-WP.

## Completion / stop
Produce the concrete deliverable and actual proof with DONE/REWORK/BLOCKED or a precisely named lower execution state. Do not mark completed because a prompt, Dispatch, tool invocation or plan exists. CHAT owns the end-to-end result.

## Shared operating and Bridge applicability
Apply shared `../../shared/operating_rules.md`. A routine reversible independent native task needs no Bridge Dispatch, manual R0–R7 artifact or immutable prompt publication. When and only when the actual execution is Bridge-controlled, follow `../../shared/bridge_e2e_v041.md` and the **installed** runtime contract, not an assumed current version. All source/receipt/test evidence must be observed, not invented. Old consumed attempts remain immutable and non-replayable. Complete outcomes in the SAME logical task; do not create administrative micro-WPs.
