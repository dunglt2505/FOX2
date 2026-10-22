---
name: fox2-method-result-acceptance
description: "Review Agent deliverables and verify feature acceptance proportionately; merge result-review and feature-certification."
---

# fox2-method-result-acceptance

**FOX2 Layer 2 — Domain methods — Agile Lite 0.5.0**

## Activate when
An Agent result, code change, test artifact or material feature milestone needs CHAT acceptance.

## Input
Task acceptance, observed code diff/artifact, actual executed tests, risk and (if Bridge) verified remote result.

## Work to perform
1. Compare **actual** diff/output to acceptance, changed-file allowlist, focused tests and relevant negative/security regressions. A plan or self-reported PASS is not evidence.
2. For Bridge transport, read real result branch/remote SHA, ledger state, task/prompt/Dispatch reference and publication owner. `PUSHED_UNREVIEWED` is not CHAT acceptance; remote result must be reviewed. Do not require reports not present in the selected task's actual contract.
3. Conclude `DONE/CHAT_ACCEPTED`, `REWORK` (precise defect in SAME logical task), or `BLOCKED` (real prerequisite). Do not issue a fresh Agent prompt when merely receiving a result.
4. For milestone-level feature certification only, trace core BRD/TechSpec acceptance to unit/integration/negative tests and actual usable product evidence. Distinguish `TEST_EVIDENCED`, `PRODUCT_USABLE`, `CHAT_ACCEPTED`, `RELEASED` and `LIVE`.
5. Reuse accepted unchanged PASS; retest what changed or what independently needs fresh evidence. Do not demand independent audit for each small reversible patch.

## Output
One evidence-based CHAT acceptance verdict with exact rework or next action.

## Responsibility boundary
Owns quality verdict only. Does NOT route Agents, generate prompts, operate Bridge, grant deployment/LIVE authority or add a certificate for each fix.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
