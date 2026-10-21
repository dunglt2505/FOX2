# FOX2 — Owner Directive — G3 Privileged Isolated-Host Test Authority

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`

## Exact Owner directive

> làm tiếp đi

## Context-bound interpretation

Immediately before this directive, CHAT stated that the only remaining blocker was explicit Owner authorization for the bounded G3 privileged isolated-host test scope already published in:

`docs/architecture/FOX2_BRIDGE_F1_G3_HOST_ENFORCEMENT_TEST_ENTRY_CANDIDATE_20261021.md`

at commit:

`f0fcc1bfefa682701f3d9a9f8e0a24d2ab33b071`.

Accordingly, this directive is recorded as Owner authorization to continue that exact G3 scope only.

## Authorized scope

- isolated/disposable Windows host or equivalently isolated test target;
- task-specific G3 host PreExec;
- elevated Administrator operations only within the bounded G3 test;
- protected ProgramData test authority root;
- AppIDSvc state/configuration required for isolated enforcement;
- AppLocker policy apply/verify for isolated G3;
- FOX2 F1 test service install/config/start/stop/remove;
- one bounded positive service-owned execution fixture only after required negatives pass;
- restart/revoke/policy-loss/service-loss/rollback tests;
- rollback/restoration required by the G3 entry contract.

## Not authorized

- G4 Owner daily-host adoption;
- Canary009;
- main/merge;
- provider/trading broker;
- LIVE;
- production release;
- declaring `INTERNAL_FOX2_BRIDGE_READY`;
- replaying G2 A01 or any consumed Dispatch.

## Evidence semantics

This Owner grant supplies authority for the named G3 scope. It does not convert any technical `NOT_RUN/BLOCKED/FAIL` to PASS. G3 execution still requires fresh exact source binding, isolated-target identification, task-specific host PreExec PASS, rollback proof, one-writer/no-replay checks and immutable Git evidence.

