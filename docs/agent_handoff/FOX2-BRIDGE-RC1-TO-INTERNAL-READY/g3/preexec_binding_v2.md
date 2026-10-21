# FOX2 — G3 Host PreExec Binding v2

Task ID: FOX2-BRIDGE-RC1-G3-HOST-A01

Task path: docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/g3/task.md
Task blob SHA-1: 005443a4ac0211450607b31cf71676f737f6f336
Task SHA-256: 1676ca5990d9c1808bae70dcaf885a13db04143ca563b61caa6bb43d744872b3

PreExec runner path: agent_bridge/scripts/f1_g3_host_preexec.ps1
PreExec runner blob SHA-1: a45e3ddc883d92da3a83d5cacea8ef18324a279a
PreExec runner SHA-256: ec4bc4430405c13e7ceb48378a4de76032b89027ce3f80dafc188b63700a28d9

Receipt path: reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/g3_host_preflight.json

This v2 binding supersedes the earlier G3 PreExec binding only for the runner identity. The task identity and G3 scope are unchanged. The runner is read-only with respect to Windows policy/service state and may publish only its durable PreExec receipt. Host execution remains blocked until CHAT remote intake of a PASS receipt.
