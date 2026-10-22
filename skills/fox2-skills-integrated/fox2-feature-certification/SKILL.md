---
name: fox2-feature-certification
description: Verify feature acceptance with actual behavior, tests and operational risk at a material milestone.
---

# fox2-feature-certification

## Activate when
A materially changed feature, release gate or Owner-requested product acceptance requires certification.

## Work to perform
Trace BRD/TechSpec acceptance to code and observed unit/integration/negative/security tests. Distinguish TEST_EVIDENCED, PRODUCT_USABLE, CHAT_ACCEPTED and RELEASED/LIVE; do not treat passing a small mocked subset as deployed host proof. Reuse unchanged accepted PASS when tests remain valid. Bridge can establish Agent delivery, not business acceptance by itself; a `PUSHED_UNREVIEWED` branch remains pending CHAT review. Do not add a certificate or mandatory independent review for each routine bug fix.

## Completion / stop
Produce the concrete deliverable and actual proof with DONE/REWORK/BLOCKED or a precisely named lower execution state. Do not mark completed because a prompt, Dispatch, tool invocation or plan exists. CHAT owns the end-to-end result.

## Shared operating and Bridge applicability
Apply shared `../../shared/operating_rules.md`. A routine reversible independent native task needs no Bridge Dispatch, manual R0–R7 artifact or immutable prompt publication. When and only when the actual execution is Bridge-controlled, follow `../../shared/bridge_e2e_v041.md` and the **installed** runtime contract, not an assumed current version. All source/receipt/test evidence must be observed, not invented. Old consumed attempts remain immutable and non-replayable. Complete outcomes in the SAME logical task; do not create administrative micro-WPs.
