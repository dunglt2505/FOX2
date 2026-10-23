# FOX2 — G3 Physical Windows Host Enforcement Test
Date: 2026-10-23
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Technical attempt: `FOX2-BRIDGE-RC1-G3-PHYSICAL-A01` (fresh source/identity under SAME Whole-WP)
Target: OWNER_SELECTED_PHYSICAL_WINDOWS
Actor: OWNER_MANUAL_HOST / CHAT oversight; no Agent or Dispatch
Stage: TEST; initial status: NOT_RUN

## Owner direction and accepted source
Owner directs use of the **physical Windows computer** for G3; no hardware-form-factor or additional machine-class gate applies.
G2 source `66e8f0a8b3a93140b5f908628b55ac965e15b96e`, result `ac1d1184255945b2c4304641360a1e661ff2d7bd`, CHAT BUILD acceptance `dcf42dd76c8f22e155d469d356e1f1219f3d7b14`. Reuse unchanged PASS.
R5 certifier code was CHAT accepted at `1ef5506d592cc7da9c93e61d86a158c12b9b27b3`. A04 lifecycle PASS_OBSERVED, restart failed and internal validation 001 CONSUMED/NO_REPLAY.
Original G3 task/preflight and its BLOCKED status remain historical at `c61ffd259a384e9c96b563968c6b7b98a0f156cd`. This source is a prospective new physical-host task and MUST NOT reuse any prior consumed attempt.
Current human Agile Lite governance applies to new management decisions; installed machine Policy/Dictionary pins are independently verified, never silently rebound.

## Required G3 readiness on the selected physical computer
Read-only capability checks may run without Administrator privileges. Verify Windows edition, PowerShell 7, AppLocker policy-query capability (including Windows PowerShell compatibility), AppIDSvc, currently installed F1 service/protected authority root, and OS policy ownership.
Before any privileged mutation, verify an elevated Administrator token, exact source/package identity, one-writer/no-active-Agent, no unresolved F1 collision or live claim, and actual ability to export and restore the current effective policy/AppIDSvc/service configuration. Digests alone are NOT restorable backups.
CHAT must read back fresh target-specific PreExec and authorize only actions within the existing bounded G3 scope. Read-only scan alone is not PASS_TO_EXECUTE.

## G3 technical evidence — do not cut safety tests
E1 protected F1 root/DACL/reparse boundaries; E2 exact SCM service image/identity/singleton; E3 AppLocker Enforce digest and AppIDSvc running; E4 deny copied/alternate-root legacy binaries/scripts/interpreters; E5 authenticated IPC peer and forged-peer denial; E6 one authorized synthetic service-owned spawn AFTER mandatory negatives; E7 same-ID concurrency creates exactly one child and one consumed identity; E8 restart/revoke/service/policy-loss/clock/rollback preserve no-replay; E9 source/package/plan drift DENY; E10 restore original host AppLocker/AppIDSvc/service configuration and finish F1 authority DENY.
Order: observe current state → preserve restore material → verify no-conflict → validate negative gates → single authorized synthetic positive → resilience tests → restore/compare.
No provider, broker, real-money, Canary, LIVE, protected-main merge or G4 adoption is authorized by this technical G3 task.

## STOP / acceptance
STOP before host mutation if policy restoration cannot be demonstrated, the selected host contains an unexplained F1 service/authority root, source or task identity drifts, a writer/claim is active, or privilege/capability is missing.
G3 is PASS only with actual E1–E10 Windows-host evidence, final restoration, source binding and CHAT review. G4 and INTERNAL_FOX2_BRIDGE_READY stay NOT_RUN/NOT_ATTESTED.
NEXT_SAFE_ACTION: physical Windows read-only capability observation, then fresh technical admission under this immutable new source. No replay.
