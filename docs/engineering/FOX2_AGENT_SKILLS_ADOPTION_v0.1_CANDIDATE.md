# FOX2 — Selective Addy Agent Skills adoption matrix v0.1

**State:** CANDIDATE / NOT EFFECTIVE. **Applies to:** all FOX2 project workstreams when eventually accepted, not only Bridge and not just 17 FOX2 Skills. **Upstream pin:** \`aeac41d4d005999432bb7312f7ff06383a91d59d\` / release 0.6.13. **Target/source base:** \`09dc4051e6a308f72a103e879489d275770a8761\`. Verify actual newest, trusted FOX2 sources again at execution-time; these pins are evidence snapshots only.

## Method → FOX2 owner mapping

| External method | Owning FOX2 entry point / mechanism | Engineering delta | Forbidden import |
|---|---|---|---|
| \`constraint-driven-development\` | \`fox2-techspec-validator\`, \`fox2-feature-certification\`, \`fox2-governance-preflight\`, future CI checks | Measured baseline, ratchet, suppressions/deleted-tests diff checks | External thresholds override governance; auto-block L0 document analysis |
| \`test-driven-development\` | Copilot/Codex executable task contract, \`fox2-feature-certification\`, \`fox2-result-review\` | Red/green/characterization evidence and domain-negative cases | blanket coverage claim; replay failed/consumed Dispatch |
| \`code-review-and-quality\` | \`fox2-result-review\`, \`fox2-feature-certification\` | five-axis review with severity, tests-first and changed-scope evidence | claim Code Review PASS = CHAT intake/release PASS |
| \`doubt-driven-development\` | \`fox2-strategic-agent-triage\`, \`fox2-techspec-validator\`, \`fox2-result-review\`, \`fox2-research-validation\` | Risk-triggered fresh-context falsification and reconciliation | automatic cross-model spend/agent spawn; fake approval signature |
| \`context-engineering\` | \`fox2-source-resolver\`, \`fox2-agent-prompt-builder\`, \`fox2-agent-route-runtime\`, \`fox2-thread-handoff\` | concise immutable source slice, on-demand references, router collision tests | preload all 25 Skills; trust static version string as authority |
| \`api-and-interface-design\` | \`fox2-brd-change-control\`, \`fox2-dictionary-impact\`, \`fox2-techspec-validator\`, feature acceptance | provider/consumer contract, compatibility and negative schema tests | autonomous BRD rewrite, unapproved new semantics |

## Coverage of other 17 native Skills

- \`fox2-document-publication\` and \`fox2-source-sync\`: E5/E6 improve lineage/consumer handling only; publication and byte-readback authority unchanged.
- \`fox2-execution-recovery\`: E2/E4 introduce additional no-replay/unknown-outcome tests only; never convert timeout to retry.
- \`fox2-project-health\` and \`fox2-status-roadmap\`: E3 evidence quality and E5 provenance; never infer completion from workflow names.
- \`fox2-research-validation\`: E2/E4 focus on out-of-sample, survivorship, lookahead and provenance.
- \`fox2-agent-prompt-builder\`: selectable Skill methods by task, not permanently appended boilerplate.
- The six owners in the matrix above are *interfaces*, not authority transfers or commands to edit their currently installed cloud plugin.

## Detect and resolve conflicts

1. **Owner approvals:** upstream \`spec-driven-development\` suggests repeated approval stops. FOX2 reuses the exact unchanged Owner approval and opens review only for material change; no additional arbitrary approvals.
2. **Automated build:** upstream \`/build auto\` is NOT enabled; all FOX2 executable work still needs R0–R7, current permission/PreExec and exact Dispatch assignment.
3. **Git style:** upstream trunk/auto-commit guidance cannot override FOX2 non-main one-writer and delivery_owner/branch safeguards.
4. **Review:** independent review is risk-selected; avoid unconditional multi-agent multiplication that wastes credit. Required regulated/risk gates remain applicable.
5. **Tooling:** upstream Codex/Copilot skill installation procedures are optional reference only, not execution authority; check tool version and real capabilities.
6. **Security:** do not install or activate upstream \`sdd-cache-pre.sh\`, \`sdd-cache-post.sh\`, \`simplify-ignore.sh\` or any shell lifecycle hooks. Upstream issue #295 documents unresolved SSRF/cache/file mutation hazards as of this pin; do not use a global \`npx skills add\` to alter FOX2.
7. **Portability:** individual upstream Skills may rely on repo-root \`references/\`; when later adapting, bundle needed reference text or a verified link, and test actual resolver.
8. **Behavioral routing:** no guaranteed automatic Skill trigger. Run positive and must-not-fire cases on the **actual** Copilot/Codex host with pinned model and version.

## State and adoption decisions

- \`ADAPT_CANDIDATE\`: all six methods, in the limited way described.
- \`REJECT\`: wholesale 25-Skill install; default shell hooks; replacing FOX2 Governance; auto \`/ship\`; unconditional cross-model loops.
- \`DEFER\`: enforceable CI ratchets and runtime agent bindings pending full source/PreExec approval; performance/coverage thresholds pending actual baseline.
- \`NOT_RUN\`: comparative live Agent evaluations, Windows tests and security canary.
- \`NO_EFFECT\`: no current source-lock rewrite, no BRD semantic changes, no Dispatch replay, no publication/merge/deploy/LIVE.

## Delivery and promotion

The dedicated candidate branch contains read-only source evidence, docs and root \`AGENTS.md\` candidate. Promote only through the current FOX2 source/authority and affected-consumer change process. The root file provides immediate guidance **only to a tool reading this branch** and must not be misreported as an installed Skill update or project-wide effective instruction in other branches.
