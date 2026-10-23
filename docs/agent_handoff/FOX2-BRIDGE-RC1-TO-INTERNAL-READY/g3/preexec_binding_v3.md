> **HISTORICAL ONLY — DO NOT USE FOR CURRENT G3 PHYSICAL HOST.** This v3 source binding pins an older task and runner. The Owner's current physical-host task/preflight source is different; never use the old task SHA-256 or runner blob to launch a fresh G3 test. The existing historical receipt remains BLOCKED. This file is retained for provenance, not executable handoff.

# FOX2 — G3 Host PreExec Binding v3

Task ID: FOX2-BRIDGE-RC1-G3-HOST-A01

Task path: docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/g3/task.md
Task blob SHA-1: 005443a4ac0211450607b31cf71676f737f6f336
Task SHA-256: 1676ca5990d9c1808bae70dcaf885a13db04143ca563b61caa6bb43d744872b3

PreExec runner path: agent_bridge/scripts/f1_g3_host_preexec.ps1
PreExec runner blob SHA-1: ea9322aa62c693a8ba695aa0412143a69528928b
PreExec runner SHA-256: 0cbf4e61746acf155844e0f62526c28fc62df52281037e4500a1ae11b326c336

Receipt path: reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/g3_host_preflight.json

v3 supersedes earlier G3 PreExec bindings for runner identity only. It preserves the same task and scope, adds portable sanitized receipt output for CHAT publication if isolated-host Git push authentication is unavailable, and performs no Windows policy/service mutation.
