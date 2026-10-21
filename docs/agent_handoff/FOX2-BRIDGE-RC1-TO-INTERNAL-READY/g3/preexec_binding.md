# FOX2 — G3 Host PreExec Binding

Task ID: `FOX2-BRIDGE-RC1-G3-HOST-A01`

## Immutable task

- path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/g3/task.md`
- blob SHA-1: `005443a4ac0211450607b31cf71676f737f6f336`
- SHA-256: `1676ca5990d9c1808bae70dcaf885a13db04143ca563b61caa6bb43d744872b3`

## PreExec runner

- path: `agent_bridge/scripts/f1_g3_host_preexec.ps1`
- blob SHA-1: `2230b80f19071ef6f6a7e2729e9c5eadc3d9fb4c`
- SHA-256: `ac6fc899af2b667535b41230bbbd498c29db79547d68909486d45975030fe4f2`

## Receipt

`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/g3_host_preflight.json`

The runner performs read-only host/source checks and may write/commit/push only the durable PreExec receipt. It must not apply AppLocker, change AppIDSvc, create ACL-protected authority state, install/start a service, spawn an Agent, publish a Dispatch, or consume a Dispatch.

A PASS receipt still requires CHAT remote intake before any G3 host mutation.

