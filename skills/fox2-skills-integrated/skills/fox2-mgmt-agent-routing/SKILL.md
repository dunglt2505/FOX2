---
name: fox2-mgmt-agent-routing
description: "Choose one capable CHAT/CODEX/Copilot/WORK actor, model, thinking effort and transport from the residual task."
---

# fox2-mgmt-agent-routing

**FOX2 Layer 1 — Project management — Agile Lite 0.5.0**

## Activate when
A task needs an actor/model/effort/transport decision or a materially changed route.

## Input
Residual task complexity, context uncertainty, code/host access, observed Agent capability, quota and risk.

## Work to perform
1. Work CHAT-direct when the needed tools and permission are available. Use CODEX/Copilot for host-dependent coding; WORK only for genuinely independent judgment. Do not delegate ordinary analysis to create an extra gate.
2. Choose the least costly *capable* `Actor · Model/Engine · Thinking · Transport(native|Bridge) · Scope · STOP`. Separate implementation difficulty from execution/financial/security risk. Never default all tasks to High.
3. For native reversible DEV, record route briefly in existing task; no formal R0–R7 artifact or PreExec certificate.
4. For an actual Bridge route, choose route BEFORE PreExec. Verify which model/effort/mode is supported using observed host evidence; passing the tuple to Bridge is not claiming it was verified. Maintain exact pin for ongoing/consumed attempts; neither Prompt Builder nor PreExec may silently replace it.
5. If capability/authorization is unknown, select safe independent work or return ROUTE_UNKNOWN for the blocked action only.

## Output
One chosen route tuple and evidence/rationale, or one precise capability blocker.

## Responsibility boundary
Owns *selection* only. Does not set priorities, draft prompts, perform PreExec, grant permissions or dispatch Agent.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
