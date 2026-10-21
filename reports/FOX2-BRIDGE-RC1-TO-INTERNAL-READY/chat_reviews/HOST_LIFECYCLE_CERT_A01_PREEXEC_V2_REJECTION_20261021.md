# FOX2 — Host Lifecycle Cert A01 PreExec v2 Rejection

Date: 2026-10-21
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`

Publication:
`69bc6fb7b61d4405d6db296a5b8211bddb6c13b2`

Path:
`docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/host_lifecycle_cert_a01_preexec_v2.ps1`

Blob:
`ee7b22338e4ce2e67e987587e8bb29f3dedc1075`

## Finding

Structural duplication from v1 was removed, but remote review found the inherited publication-lineage check still required:

`paths.Count == 1 && paths.Contains(ScriptPath)`.

At v2 publication, valid branch history after the immutable prompt already contains:
1. rejected historical v1 PreExec file; and
2. v2 PreExec file.

Therefore v2 would deterministically stop with `PREEXEC_PUBLICATION_NOT_SCRIPT_ONLY` even when source/task state is correct.

The artifact also lacks an explicit accepted-source ancestor gate independent from prompt lineage.

## State

- Owner execution: NOT_RUN
- receipt: ABSENT
- Dispatch: NOT_PUBLISHED
- Agent: NOT_STARTED
- host mutation: FALSE

## Verdict

`HOLD — PUBLISHED_INVALID_NOT_EXECUTABLE`

Do not run or rebind v2.

A fresh v3 must:
- allow exactly historical v1 + v2 + current v3 PreExec publication paths after the immutable prompt;
- verify exact v1/v2 blobs;
- require accepted source `2faa33f9...` is ancestor;
- require no `agent_bridge/**` drift from accepted source to publication head;
- preserve read-only host checks.
