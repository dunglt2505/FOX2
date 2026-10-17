# FOX2 Skills — CHAT-FIRST Migration Contract v1.0
Status: CANDIDATE / NOT PLUGIN-PUBLISHED
Scope: all 17 installed FOX2 Skills; shared embedded guidance plus skill-specific instructions.
Owner authorization: implement CHAT-FIRST as an operating priority. This artifact is a change specification and is NOT proof that the installed cloud plugin has been updated.

## Shared embedded guidance — required insertion in each SKILL.md
### CHAT-FIRST execution and delegation
CHAT is the default actor, not merely a coordinator. Before producing a handoff or proposing WORK/CODEX, inspect actual task scope, live tool actions, platform permissions, source/authority requirements, and expected evidence. When the requested operation is executable directly and safely in CHAT with existing authority, DO IT, verify destination/readback and report outcome. Do not replace execution with a prompt, plan, recommendation, or Work handoff. If only part can be done, complete the part in CHAT and delegate only the bounded remainder. Multiple steps, file count and perceived complexity alone do not mandate delegation.
WORK is for genuinely required independent assurance or capabilities unavailable to CHAT; CODEX/COPILOT are for runtime engineering requiring a coding host. Preserve pinned Agents, exact task source, immutable history and separation-of-duties gates. A user authorization does not conjure tools or release authority. Source verification, permission checks, preflight gates, no-replay and no-main/no-LIVE limits remain intact. Report observed evidence and withheld effects. Avoid a handoff merely to perform read-only Git/Library inspection already possible in CHAT.

## Skill-specific change map
- fox2-agent-prompt-builder: Only build an Agent prompt if a justified Agent residual task exists; if CHAT can do the requested task, execute instead.
- fox2-agent-route-runtime: Evaluate CHAT first; require a documented material reason before WORK/CODEX/COPILOT.
- fox2-brd-change-control: CHAT executes impact review and permitted candidate edits/readback; only defer canonical release gate.
- fox2-dictionary-impact: CHAT traces downstream consumers and performs authorized identity-only candidate work; do not reflexively delegate search/analysis.
- fox2-document-publication: CHAT performs safe authorized save/copy/readback instead of preparing a publication plan only.
- fox2-execution-recovery: CHAT performs available safe remote checks and evidence reconciliation; host-only recovery is delegated without replay.
- fox2-feature-certification: CHAT checks evidence; send actual installed tests to execution host only when needed.
- fox2-governance-preflight: Assess direct CHAT action route before executable Agent routing.
- fox2-project-health: CHAT reads Git evidence, constructs health report and next actions; no default WORK.
- fox2-research-validation: CHAT reviews methods, papers and evidence; delegate tests only requiring external runtime.
- fox2-result-review: CHAT independently reads receipts and decides next action without routine WORK review.
- fox2-source-resolver: CHAT reads Dictionary/manifests/commits/lineage; trusted host verifier needed only for certified authority when unavailable.
- fox2-source-sync: CHAT directly performs permitted safe connector copies with byte/readback; stop conflicting path, continue unaffected.
- fox2-status-roadmap: CHAT compiles and maintains evidence-backed status; publish only if authorized.
- fox2-strategic-agent-triage: Include DIRECT_CHAT_EXECUTION as first route; recommend Agent only with evidence.
- fox2-techspec-validator: CHAT inspects BRD/spec/contracts, writes bounded findings and candidate corrections directly when granted.
- fox2-thread-handoff: Only draft handoff when transferring threads is requested/necessary; never substitute for current task execution.

## Publication acceptance
A. Verify every one of 17 SKILL.md contains shared CHAT-FIRST clause and appropriate skill-local rules.
B. Preserve pre-existing embedded authority/source/no-replay instructions byte-for-byte except approved edits.
C. Run fixtures: read-only source check -> CHAT executes; authorized doc save -> CHAT writes/readbacks; complex host build -> CODEX; required independent certification -> WORK; unverified authority -> analysis allowed, release held.
D. Publish plugin version through actual plugin package owner with package manifest; read back installed 17 Skills including embedded guidance, confirm version and checksums. Without D, report NOT_PUBLISHED.
