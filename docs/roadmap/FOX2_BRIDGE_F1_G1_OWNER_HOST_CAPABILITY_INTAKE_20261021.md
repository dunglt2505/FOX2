# FOX2 Bridge F1 G1 — Owner host capability intake
Date: 2026-10-21
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Feature: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION
Mode: CHAT intake of Owner-pasted redacted output from g1_host_capability_readonly_20261021.ps1
Design source: f15f8efba214d0f5a3ca51304ff5127d293356cc
Probe source: 74d83520ae8dda4ff89534d6d746bc06f9fcd428

## Provenance and limitations
The Owner pasted the JSON result in the active CHAT thread. It is host-reported read-only evidence, not cryptographic machine attestation and not an Agent Result. The published intake deliberately excludes the shell prompt/user name and contains no SID, credentials, rule bodies or command lines.

## Observed values
| Field | Observation | CHAT interpretation |
|---|---|---|
| OS | Windows 11 Pro, 64-bit, version 10.0.26300, build 26300, display 26H2, UBR 9711 | Host class is compatible with Windows application-control design; registry ProductName reported Windows 10 Pro and is not used to override Win32_OperatingSystem caption |
| Current token | current_token_is_admin=false | Probe session is not elevated; ordinary requester boundary remains non-admin for this observation |
| SCM | scm_readable=true | Read-only service inspection available |
| Secure Boot | null; failed_probes=[secure_boot] | UNKNOWN, not false; the cmdlet requires elevation on supported systems |
| Device Guard kernel CI | code_integrity_enforcement=2 | ENFORCED |
| Device Guard UMCI | user_mode_code_integrity_enforcement=0 | OFF |
| VBS | virtualization_based_security_status=2 | ENABLED_AND_RUNNING |
| AppLocker cmdlet | available=true | Capability surface present |
| Effective AppLocker policy | returned=true; collections=[] | No effective rule collection observed; no current enforcement claim |
| Application Identity | present=true; state=Stopped; start_mode=Manual | Current AppLocker enforcement is not active; activation is a future authorized host step, not G1 evidence |
| CiTool | available=true | App Control management tooling is discoverable; no policy mutation performed |
| Policy issuer independence | NOT_ATTESTED_BY_LOCAL_READONLY_PROBE | Runtime issuer/administrative authority remains an operational gate |
| Durable legacy retirement | false | NOT_VERIFIED |
| Privileged F1 service | false | NOT_VERIFIED / NOT_IMPLEMENTED |
| Positive authority | DENY | Preserved |
| Canary | HOLD | Preserved |

## External interpretation basis
Microsoft documentation defines CodeIntegrityPolicyEnforcementStatus/UsermodeCodeIntegrityPolicyEnforcementStatus values 0=Off, 1=Audit, 2=Enforced and VirtualizationBasedSecurityStatus 2=enabled/running. Microsoft also documents Confirm-SecureBootUEFI as requiring an administrator PowerShell session; therefore this probe's Secure Boot failure is insufficient to classify Secure Boot disabled.

Microsoft documents AppLocker enforcement through Application Identity/AppID and notes that stopping Application Identity prevents AppLocker policy enforcement. Empty effective collections plus stopped AppIDSvc are therefore evidence of no current AppLocker enforcement, not evidence that AppLocker is unsupported.

## Intake verdict
ACCEPT_SCOPED_HOST_CAPABILITY_EVIDENCE. The host is sufficient to choose an AppLocker-based F1 design baseline for BUILD because AppLocker policy tooling and Application Identity exist and the observed interactive token is non-admin. This does NOT attest a deployed policy, complete legacy coverage, independent issuer, Secure Boot, service implementation or positive F1 runtime authority.

F1=DENY; CANARY009=HOLD; INTERNAL_FOX2_BRIDGE_READY=NOT_ATTESTED.
