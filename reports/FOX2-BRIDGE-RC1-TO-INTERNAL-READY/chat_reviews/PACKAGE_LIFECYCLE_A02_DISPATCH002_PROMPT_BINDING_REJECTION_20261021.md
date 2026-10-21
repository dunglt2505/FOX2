# FOX2 — A02 Dispatch002 Prompt-Binding Rejection

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02`

## Evidence

A02 immutable prompt:
- commit `3321d69a998e3279782476c9d52f7224095fb2d8`
- blob `23c821c9c27d2e46855539a1b2314b48a1abd1d2`

contains:

`Planned fresh Dispatch ID: FOX2-DISPATCH-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02-CODEX-001`

A02 Dispatch001:
- `e4a58760efba32c4f4da5f6d82b9421354ef349e`
- rejected pre-launch because it violated Dispatch Schema v3.

A02 Dispatch002:
- ID `FOX2-DISPATCH-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02-CODEX-002`
- commit `e05fdc99607fd7eceaa77ec2c35f34492a302bbb`
- blob `4c587595180fa55da893d4845035c678838e5721`
- Dispatch Schema v3 validation: PASS.

However the immutable prompt's planned Dispatch identity and Dispatch002 identity differ. Because the prompt also requires fresh A02 task/prompt/PreExec/Dispatch binding consistency, executing Dispatch002 would create a material ambiguity and may correctly trigger Agent STOP.

## State

- A02 implementation Agent started: false
- A02 Dispatch001 consumed: false
- A02 Dispatch002 consumed: false
- product code changed by A02: false
- host lifecycle mutation: false

## Verdict

`HOLD — A02 DISPATCH002 SCHEMA_VALID_BUT_PROMPT_BINDING_MISMATCH / NOT_EXECUTABLE`

Do not modify or rebind either published A02 Dispatch identity.

## Correction

Issue a fresh A03 assignment under the same Whole-WP:
- preserve technical objective and source baseline;
- prompt must not hard-code a future Dispatch sequence number;
- prompt must require the exact executable Dispatch identity supplied and verified by the launcher;
- fresh task/prompt, task-specific PreExec and fresh Dispatch required;
- preserve A01 consumed/no-replay and A02 non-consumed/non-executable history.
