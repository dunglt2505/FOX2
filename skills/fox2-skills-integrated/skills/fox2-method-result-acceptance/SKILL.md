---
name: fox2-method-result-acceptance
description: "Review Agent deliverables and verify feature acceptance proportionately; merge result-review and feature-certification."
---

# fox2-method-result-acceptance

**FOX2 Layer 2 — Domain methods — Agile Lite 0.5.0**

## Activate when
An Agent result, code change, test artifact or material feature milestone needs CHAT acceptance.

## Input
Task acceptance, observed diff/artifact and tests, risk, plus **authorized Git result branch and verified remote commit SHA** for delegated Agent work (native or Bridge).

## Work to perform
1. For ANY delegated Agent assignment (native CODEX/Copilot, Bridge or report-producing WORK whose result is required on Git), first verify an **actually pushed remote result commit on the assigned branch**, the observed SHA and its files. Missing/unreadable Git publication is `GIT_DELIVERY_PENDING`, not a successful result handoff or DONE. If Agent lacks Git permission, inspect only the authorized publisher's later push; preserve author/publisher provenance. Then compare **actual** diff/output to acceptance, changed-file allowlist, focused tests and relevant negative/security regressions. A plan, local edit, chat report or self-reported PASS is not Git/result evidence.
2. For Bridge transport, additionally verify actual ledger state, task/prompt/Dispatch reference and publication owner against the already verified remote result branch/SHA. `PUSHED_UNREVIEWED` is not CHAT acceptance; remote result must be reviewed. Do not require reports not present in the selected task's actual contract.
3. Conclude `DONE/CHAT_ACCEPTED`, `REWORK` (precise defect in SAME logical task), or `BLOCKED` (real prerequisite). Do not issue a fresh Agent prompt when merely receiving a result.
4. For milestone-level feature certification only, trace core BRD/TechSpec acceptance to unit/integration/negative tests and actual usable product evidence. Distinguish `TEST_EVIDENCED`, `PRODUCT_USABLE`, `CHAT_ACCEPTED`, `RELEASED` and `LIVE`.
5. Reuse accepted unchanged PASS; retest what changed or what independently needs fresh evidence. Do not demand independent audit for each small reversible patch.

**No-code result acceptance:** An explicitly `TEST_EVIDENCE_ONLY` assignment may be accepted without changes to **product code**, but only after independent inspection of the actual executed test/check command, exit status, relevant negative coverage, source/worktree identity and authorized remote Git evidence commit/report SHA. `NOT_RUN`, self-reported PASS, stale logs or merely clean `git diff` must NOT be accepted. The required remote delivery artifact still applies. A previously scoped code-change task cannot silently become evidence-only without CHAT reclassification based on real proof.

**Progress handoff:** When CHAT issues an evidence-backed acceptance, REWORK or BLOCKED verdict that changes tracked state, invoke `fox2-mgmt-delivery` to evaluate Board/Master Plan synchronization. A review verdict alone does not prove the Git docs were updated.

## Output
One evidence-based CHAT acceptance verdict referencing the **verified remote Git result branch and commit SHA**; otherwise `GIT_DELIVERY_PENDING` with one exact publication blocker. Rework/blocked does not create another logical task.

## Responsibility boundary
Owns quality verdict only. Does NOT route Agents, generate prompts, operate Bridge, grant deployment/LIVE authority or add a certificate for each fix.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
