# FOX2 Policy v2.1.0 — Outcome-First Project Operating Rules

**Project:** FOX2 (internal development)  
**Owner approval:** 2026-10-22, direct owner instruction to execute project-wide Agile Lite reform  
**Supersedes:** FOX2 Policy v2.0.0 for new/re-scoped project-management work; old immutable task/Dispatch source locks remain historical  
**Scope:** All FOX2 features, Agents, project governance, documentation and maintenance  
**Release status:** OWNER_APPROVED_SOURCE_CANDIDATE; publication/adoption recorded separately

## 1. Single management model

FOX2 operates by **Build → Test → Deliver** with ONE Kanban board: BACKLOG, DOING, BLOCKED, DONE. PLAN/DESIGN/BUILD/TEST/DEPLOY are technical activities, not approval stages. Limit to two independent material code writers, with disjoint writable scope.

Owner sets product outcome and priorities. CHAT owns delivery end-to-end, chooses Agent/model/thinking and coordinates execution within delegated task scope. CODEX/Copilot implement and test where host access is needed. WORK is exceptional for materially independent audit, not routine reviews. No repeated Owner approvals for ordinary tasks or bug corrections inside an approved outcome.

## 2. Outcome-first definition of DONE

Every task has ONE concise record: `ID · Goal · Scope · Owner/Agent · Acceptance · Status · Result pointer/blocker`. A separate prompt, Dispatch, preflight receipt, review receipt, certificate, report or WP is **not a project-management prerequisite** for normal internal work.

DONE means the requested output actually exists, necessary behavior is tested, result can be located, and serious relevant defects are known. Documentation and gate counts are not output metrics. Primary metrics: functional features done, open bugs, cycle time, aging blockers, and time to recover.

A failed test or incorrect report is repaired in the same task wherever safe. Preserve previously verified evidence unless a changed input invalidates it. No administrative micro-WPs.

## 3. Risk-based safety, without separate process lanes

CHAT makes a quick internal risk judgment and need not produce a formal classification artifact.

- **Ordinary reversible work:** scope, authorization, single writer and appropriate tests; proceed directly. No mandatory R0–R7 ceremony, separate Git prompt publication, PreExec receipt or multiple acceptance checkpoints.
- **Material contract/integration changes:** identify affected interfaces and consumers; perform focused regression and negative/security checks where relevant; review the resulting diff.
- **Consequential / irreversible actions:** broker orders, LIVE/provider writes, destructive data changes, credentials/security boundaries, host ownership/installer lifecycle, durable claims and no-replay require actual risk-specific checks, rights and, when applicable, explicit Owner authorization. Never infer permission from a routine DEV task.

These are **conditional safeguards**, not three boards, routes or approval chains.

## 4. Source and version hygiene

One authorized source selection governs each new task. Use the effective governance release decision and canonical registry; resolve BRD/TechSpec/contract only when relevant to the task. Do NOT create a new task because old immutable documents mention an old version, and do NOT blanket-bump Policy, Dictionary, BRD, TechSpec, manifest, prompt or generated binding.

Classify references:
1. Historical/locked/compatibility reference: preserve unchanged.
2. Stale descriptive text not used as authority: do not create work solely to fix it.
3. Wrong *active* source resolution: fix one canonical resolver/pointer, not all consumers.
4. Actual incompatible machine consumer: change the affected generator/validator and tests once, with compatibility retained.

The current human project operating policy and an older locked Bridge runtime contract may legitimately differ. Do not call that a conflict without observed incompatible behavior.

## 5. Agent task and delivery

Prefer CHAT direct action. For an eligible native Agent route, use a concise task instruction with goal, allowed scope, acceptance tests, result destination and STOP on material risk. Keep source commit/worktree/authorization where needed to avoid collisions, but avoid duplicating it across extra records. Agent may iterate fixes inside the SAME task, provided no consumed or irreversible operation is replayed. CHAT reviews only material diff/test/risk evidence and closes DONE / REWORK / BLOCKED.

Git evidence is preserved for code changes; Git prompt/Dispatch/receipt overhead is reserved for transport paths whose real runtime requires it or high-consequence operations. Existing Bridge Dispatches remain pinned, with unchanged state and no-replay semantics.

## 6. Standing Owner authorization and boundaries

The Owner's 2026-10-22 direction authorizes project-wide management simplification for future ordinary internal work, including removing project-internal administrative preflight/Dispatch/approval requirements from an independently usable native DEV workflow. This is a **standing internal management decision**, not a test PASS or a grant of external permissions.

**Not authorized by this policy alone:** push/merge to protected main, production deployment, broker/provider write, real-money order, exposure of secrets, destructive actions, consumption/replay of a previously locked Dispatch. Existing historic FAIL/BLOCKED/NOT_RUN are never rewritten.

## 7. Adoption and supersession

Apply to new or properly re-scoped work after approved publication. Do not rewrite active/consumed attempts. Preserve Policy v2.0.0 and prior immutable manifests as history. If the installed runtime or Skills plugin has not adopted this version, mark that consumer NOT_ADOPTED; continue other authorized work without fictional PASS.

One change package is sufficient for Policy/Skills/Task Protocol/board. Update only materially affected consumers and tests; no additional approval stages invented to activate this operating model.
