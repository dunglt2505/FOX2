# FOX2 — R4 Owner Launcher Transport Recovery

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001`

## FIRST_FAILURE

The Owner copied a very large PowerShell launcher from CHAT into the interactive shell.

Observed behavior shows the launcher was not preserved as one script scope: later statements were interpreted individually after the enclosing block had already terminated. Functions and variables that existed only inside the original scope became unavailable/null, including launcher helpers and runtime variables.

Therefore any later `Write-Output` marker emitted by isolated lines is not sufficient evidence that the governed launcher crossed its durable consume boundary.

## Remote reconciliation

CHAT independently checked the authorized R4 task branch after the transport failure:

- runtime base: `35aa18ccabcc6f7d4b889ed213c075fc314d45d0`
- current remote R4 head: `35aa18ccabcc6f7d4b889ed213c075fc314d45d0`
- comparison: identical
- commits ahead: 0
- changed paths: 0

Therefore there is no remote Agent result and no evidence of product/result mutation.

## Dispatch interpretation

R4 Dispatch:
`4655d1c2505ab4feb425efc9a09ceb0820631d3c`

The Dispatch is **not authorized for blind replay**.

However the malformed console output alone does not prove durable consumption. Before any execution, the new immutable launcher MUST check the R4 durable claim path on the Owner host:

- claim exists => STOP / NO_REPLAY / reconcile;
- claim absent, R4 task branch still exact runtime base, worktree clean, no task writer, and all immutable bindings still valid => classify the prior event as `LAUNCH_TRANSPORT_NOT_STARTED` and allow the same still-unconsumed R4 Dispatch to execute once.

This is a discriminating recovery check, not a replay waiver.

## Correct delivery mechanism

CHAT must not ask Owner to paste the large launcher body into an interactive shell.

Publish the complete launcher as an immutable Git `.ps1` artifact on a non-product control branch.

Owner-visible PowerShell must:
1. require PowerShell 7+;
2. fetch/read the exact launcher commit/path;
3. verify Git blob and SHA-256 before execution;
4. PowerShell-parse the downloaded bytes;
5. write them to a temporary `.ps1` file;
6. execute the file with `pwsh -NoProfile -File`;
7. leave the product R4 branch untouched until the governed Agent execution itself;
8. remove the temporary launcher afterward.

The immutable launcher itself retains all task/source/route/one-writer/no-replay/result-pickup guards.

## Reusable PASS

Preserve:
- accepted Bridge source;
- A04 reusable PASS;
- R4 task/prompt;
- schema-valid R4 PreExec PASS;
- R4 PASS_TO_ASSIGN;
- R4 Dispatch schema/readback;
- selected route CODEX / gpt-6.1-sol / medium.

No package build/install or Host Lifecycle rerun is required.

## Verdict

`RECOVERED / LAUNCH_TRANSPORT_FAILURE / REMOTE_RESULT_ABSENT / CONSUMPTION_REQUIRES_HOST_CLAIM_CHECK`

## Next safe action

Publish and read back an immutable R4 Owner launcher.

Then Owner runs only the short verified bootstrap.

The bootstrap/launcher must STOP if the durable R4 claim already exists.

If the claim is absent and all immutable checks still pass, execution may proceed once under the existing R4 Dispatch.

A05/G3/G4/Canary remain locked.
