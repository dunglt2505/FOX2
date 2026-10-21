# FOX2 Bridge F1 — G2 task-specific PreExec contract candidate
Date: 2026-10-21
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Class: NON-EXECUTABLE CANDIDATE / NO TASK ISSUE / NO AGENT START
Preparation base: 4d492e96cd18bc836a48aae7e76ae4ab4fa631a8

## Why a dedicated G2 binding is required
The shared PreExec engine is reusable, but the current `bridge` profile registration is not the G2 task identity. At the preparation base it is hard-coded to:
- WP `FOX2-BRIDGE-DESKTOP-BATCH-B`;
- branch `work/FOX2-BRIDGE-DESKTOP-BATCH-B`;
- task `docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-B/task.md`;
- receipt `reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json`;
- CODEX pinned `gpt-6.1-sol` with reasoning `medium`.

G2 requires the existing Whole-WP plus Owner-pinned GPT-6.1 Sol / HIGH. Therefore using `--profile bridge` unchanged would produce a false task/source binding and is forbidden.

## Code base provenance
Compare `804b2e21cd2f8793168ca24bc402e5cdcdb70b3e` -> `4d492e96cd18bc836a48aae7e76ae4ab4fa631a8` shows the design branch is 19 commits ahead and changes only G1/G2 docs, Feature Status and the read-only host probe. No `agent_bridge/src/**`, `agent_bridge/tests/**` or existing runtime script code changed after the accepted StrictMode/code snapshot.

Therefore the planned G2 implementation branch may fork from exact base:
`4d492e96cd18bc836a48aae7e76ae4ab4fa631a8`

without losing the accepted F1/StrictMode code state or the G1/G2 design evidence.

## Planned exact G2 identity
- branch: `work/FOX2-BRIDGE-F1-G2-INTEGRATED-BUILD-20261021`
- branch current existence at preparation time: NOT_CREATED
- base SHA: `4d492e96cd18bc836a48aae7e76ae4ab4fa631a8`
- WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
- task path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/g2/task.md`
- prompt path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/g2/prompt.md`
- preflight receipt path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/g2_preflight.json`
- Agent result report: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- evidence manifest: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`

These paths are reserved design inputs only. Their absence at this stage is correct and must not be treated as publication failure.

## Planned exact route tuple
```text
Role               = CODEX implementation agent
Product            = CODEX
Model policy       = PINNED
Model              = gpt-6.1-sol
Reasoning effort   = high
Permission profile = FULL_ACCESS (technical only, bounded by task paths/STOP)
Execution path     = MANUAL_LOCAL
Delivery owner     = AGENT
Max attempts       = 1
```

No main, merge, deployment, provider, broker, Canary or LIVE permission.

## Reuse versus change
REUSE unchanged shared components:
- `agent_bridge/src/fox2_agent_bridge/preexec/engine.py` lifecycle;
- `writer_lock`, competing-writer observation, worktree hygiene;
- Dictionary/contract drift validation;
- Codex readiness probe semantics;
- durable schema-v1 receipt validation/publication/readback.

DO NOT modify shared PreExec merely to register this task while coding HOLD remains.

After coding authority exists, Prompt Builder/preflight launcher may instantiate `Requirements` directly with the exact G2 identity and route above, or a separately reviewed generic registration mechanism may be implemented if genuinely necessary. No fake reuse of Batch-B identity.

## Material G2 checks
1. worktree exact branch/base ownership and clean WIP;
2. no competing writer + writer lock acquired;
3. task.md exists at exact task source head and is immutable for the preflight;
4. Dictionary 1.3 and current contracts match their pinned bytes;
5. Git, Python, PowerShell 7 and Windows service-development toolchain available;
6. CODEX CLI executable exists;
7. CODEX exact `gpt-6.1-sol` + `high` + FULL_ACCESS syntax/config accepted;
8. CODEX auth/capacity readiness probe returns the expected proof marker;
9. Git push permission to exact non-main G2 branch/result paths;
10. no old Dispatch/Attempt identity is used or consumed;
11. executable Dispatch remains unpublished and Agent implementation not started during PreExec.

Bridge-installed PAUSED/worker readiness is NOT a material prerequisite because this is native manual-local DEV and Bridge must not execute its own modification.

## PreExec state machine for this G2
```text
CODING_AUTHORITY_GRANTED
 -> create exact non-main G2 branch/worktree from 4d492e96...
 -> Prompt Builder prepares source-bound task contract
 -> publish/read back task.md as task source
 -> run task-specific PreExec with G2 Requirements
 -> publish/read back durable receipt
 -> CHAT intake
 -> PASS_TO_ASSIGN only if every material check PASS
 -> publish/read back exact prompt.md
 -> one CODEX attempt
```

If the exact task/prompt publication ordering required by the final Prompt Builder differs, the immutable task source used by PreExec must still be unambiguous and the final prompt cannot broaden it.

## STOP
Current Owner coding HOLD remains active. This document does not authorize creation of the planned branch/worktree, task.md, prompt.md, PreExec execution, Codex probe, Dispatch or Agent start.

Current verdict: `PREEXEC_CONTRACT_PREPARED / EXECUTION_HOLD`.
