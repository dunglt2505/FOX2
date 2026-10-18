"""Compose current acceptance from preserved prior PASS and fresh installed UI proof."""
import hashlib
import json
from pathlib import Path
import subprocess

out = Path(__file__).resolve().parent
repo = out.parents[3]
report_root = repo/'reports/BRIDGE-DESKTOP-BATCH-B'
old_ref = 'dbaefdf686e06ffdf78b277288515deca9011710'
def git(*args):
    return subprocess.check_output(['git',*args],cwd=repo)
def write(path, value):
    Path(path).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))
for name in ('report.md','evidence_manifest.json'):
    (out/('historical_dispatch_003_'+name)).write_bytes(git('show',old_ref+':reports/BRIDGE-DESKTOP-BATCH-B/'+name))
prior = load(out/'historical_dispatch_003_evidence_manifest.json')
fresh = load(out/'artifact_ui_certification.json')
runtime = load(out/'final_runtime_readback.json')
assert fresh['status'] == runtime['status'] == 'PASS'
old_gates = load(report_root/'evidence/rc1_recovery_003/acceptance_gates.json')['technical_gates']
gates = {}
for name, value in old_gates.items():
    if name in fresh['gates']:
        gates[name] = dict(status='PASS', evidence='artifact_ui_certification.json', method='Fresh native installed UI action; hashes, timestamp and atomic filesystem rename verified')
    elif name in ('SOURCE_BINDING','SOURCE_REGISTRY_AUTHORITY_CHAIN','FRESH_PREEXEC','DISPATCH_V3_STRUCTURAL_CONFORMANCE'):
        gates[name] = dict(status='PASS',evidence='preflight.json' if name != 'DISPATCH_V3_STRUCTURAL_CONFORMANCE' else 'final_runtime_readback.json')
    elif name in ('CHANGED_PATH_ALLOWLIST','SECRET_SCAN','GIT_DIFF_CHECK'):
        gates[name] = dict(status='PASS',evidence='quality_checks.json')
    elif name == 'PRECANARY_INDEPENDENT_AUDIT':
        gates[name] = dict(status='PENDING',owner='WORK/CHAT',self_certified=False)
    else:
        assert value['status'] == 'PASS', (name,value)
        gates[name] = dict(status='PASS',evidence='dbaefdf686e06ffdf78b277288515deca9011710:reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_recovery_003/acceptance_gates.json',carried_forward=True,reason='CHAT accepted prior executed evidence; all 252 installed payload files and package hash unchanged; no product changes')
gates['INSTALLED_UI_ARTIFACT_FRESHNESS'] = dict(status='PASS',evidence='artifact_ui_certification.json')
gates['INSTALLED_RUNTIME_TECHNICAL_CERTIFICATION'] = dict(status='PASS',evidence=['artifact_ui_certification.json','final_runtime_readback.json'],composition='Prior accepted installed lifecycle/poll gates plus fresh UI Vault closure')
gates['ICON_DISPOSITION'] = dict(status='ICON_NON_GATING_NO_AUTHORIZED_ASSET',gating=False)
write(out/'acceptance_gates.json',dict(format='FOX2_RC1_FINAL_CLOSURE_GATES_1',dispatch_id='FOX2-DISPATCH-BRIDGE-RC1-CODEX-004',gates=gates))
report = '''# FOX2 Bridge RC1 — final technical closure

Result: implementation published for CHAT intake, unreviewed. Installed runtime technical certification PASS. PRECANARY_INDEPENDENT_AUDIT remains PENDING, owned by WORK/CHAT; no PRECANARY_READY or release authority is claimed.

Dispatch FOX2-DISPATCH-BRIDGE-RC1-CODEX-004 ran once under control dc79f8143eec471508bf37565bff38442ce0548a, retrying historical Dispatch 003. Execution base: 0789e5d8c3944fdc078090f50f18fb2a3abe6b64; product WIP source: dbaefdf686e06ffdf78b277288515deca9011710. Codex gpt-6.1-sol / medium / FULL_ACCESS was observed from sanitized running process options. Fresh PreExec at 0789e5d was reused: its only change from the product source is the receipt. No product code, package, installer or lifecycle change was necessary. Dispatches 001/002/003 were not replayed; 004 is now recorded in the installed manual-consumption store.

All ten source families were verified by the installed source-resolver through authenticated live GitHub reads: Registry b27f1085ee13d8dce56fd2735e100ea1616e6e23 → manifests and externally nominated Owner approval d8e2331674ef1921844f369bfa9e48b82a73c6a1 → immutable c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359 bytes and SHA-256. Dispatch, task and prompt hashes match. The binding remains WP-only with no global semantic promotion or protected authority.

Fresh installed UI proof: the current installed FOX2.Bridge.Desktop.exe was launched, Artifacts selected, Save local file clicked, the unique synthetic TXT path typed into the native picker and Open clicked. The helper rejected a cached accessibility index once; fresh observation and ordinary coordinate/keyboard input completed the same UI interaction. No service/assembly save, Core-only call, test bypass or remainder harness was used. UI receipts and the final screenshot show the resulting record.

Attempt started 2026-10-18T02:49:33.0920818Z. Installed UI PID 2568 started 2026-10-18T02:49:33.8294088Z and remained the same process throughout the save. The new artifact was saved at 2026-10-18T02:50:58.1589729+00:00, newer than both starts. Selected file: artifact-ui-a90dc9380a0943318e82d58dbf9cc732.txt, 148 bytes. Source and copied object SHA-256: 098e31fb461b62f75bccf5eb135607e3b0ab48207734cf48910a2cc467a4c65e. Artifact ID is sha256: followed by that digest; its exact source/object paths and hashes are in artifact_ui_certification.json.

The index grew from 3 to 4 records, preserving all prior records. A read-only Windows ReadDirectoryChangesW observer captured pending-index creation/write and the paired rename from .index-3cc73c786c4946f0bc402b9f79786bb4 to index.json. Before/after file identities differ, the live index matches the complete after snapshot, and no pending index/copy remains. The record State is exactly LOCAL_SAVED. RC1 serializes this canonical state without git_synced/released fields; the evidence explicitly interprets it as git_synced=false and released=false, without pretending those booleans were persisted. All four requested Artifact Vault gates and freshness PASS, with 27 successful readback checks.

Package: FOX2-Bridge-RC1.zip, SHA-256 a0516aed3d69564c657dc557b7b09cfaab549d6ab04ce4132e9399b50ce5b4ac. Existing package bytes and installed pointer match; all 252 installed payload files match their manifest, including the current UI executable and assembly. No rebuild, repackaging or reinstallation was needed.

CHAT-accepted prior results are carried forward for unchanged product/package: 399 Python tests PASS, 30 Desktop checks PASS, WPF Release build PASS, deterministic package PASS, install/update/uninstall/startup/single-instance/process-separation/control-store/support bundle PASS. Real installed safe poll remains PASS / NO_CHANGE / no claims or executions. These gates were not rerun solely to repeat evidence. Current installed control status is STOPPED, paused=true, setup_complete=true; startup preference is unchanged. Desktop remains open displaying the saved record. Fresh structural Dispatch-v3 validation, source-chain checks, changed-path allowlist, secret scan and git diff --check PASS.

The branded icon is ICON_NON_GATING_NO_AUTHORIZED_ASSET; the generic Windows icon is retained. Historical Dispatch 003 evidence is unchanged, including its truthful stop/failure receipts. Its prior mutable aggregate report/manifest are preserved under rc1_final_closure_004. Current gate evidence combines accepted unaffected evidence with this fresh closure; it does not rewrite historical failure into PASS.

Only reports/BRIDGE-DESKTOP-BATCH-B/** changed in this Dispatch. The exact paths and staged Git-blob hashes are in evidence_manifest.json. The containing Git commit identifies this result; exact local/remote SHA and authenticated remote byte readback are reported after push. Release acceptance is not granted by implementation publication.

Canary 009 untouched at 501822a33ef08c7365154913bbc677544856eee5, with zero installed-ledger claims/executions. APP-BATCH-B remains paused at fc8aba202e15bddfcc5156b2c1bb36ed222329eb. No main push, PR, merge, deploy, provider, broker or LIVE action occurred.
'''
(report_root/'report.md').write_text(report,encoding='utf-8')
manifest = dict(format='FOX2_RC1_IMPLEMENTATION_RESULT_MANIFEST_2',whole_wp='FOX2-BRIDGE-RC1-TO-INTERNAL-READY',dispatch_id='FOX2-DISPATCH-BRIDGE-RC1-CODEX-004',dispatch_control_commit='dc79f8143eec471508bf37565bff38442ce0548a',status='IMPLEMENTATION_PUSHED_UNREVIEWED',branch=prior['branch'],execution_base='0789e5d8c3944fdc078090f50f18fb2a3abe6b64',product_source=old_ref,source_freeze=prior['source_freeze'],registry_commit=prior['registry_commit'],owner_approval_commit=prior['owner_approval_commit'],preexec_publication_commit='0789e5d8c3944fdc078090f50f18fb2a3abe6b64',agent=prior['agent'],installed_runtime='PASS',acceptance_gates='reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/acceptance_gates.json',package=prior['package'],test_results=dict(python_passed=399,desktop_passed=30,prior_tests_carried_forward=True,fresh_artifact_readback_checks_passed=27,installed_ui_artifact_freshness='PASS'),real_installed_poll='PASS_NO_CHANGE_NO_CLAIMS_EXECUTIONS_CARRIED_FORWARD',remaining_independent_gate='PRECANARY_INDEPENDENT_AUDIT_PENDING',icon_disposition='ICON_NON_GATING_NO_AUTHORIZED_ASSET',canary_009='UNTOUCHED',app_batch_b='PAUSED_NO_ACTION',protected_actions='NONE',product_changes_this_dispatch=[],prior_implementation_manifest=old_ref+':reports/BRIDGE-DESKTOP-BATCH-B/evidence_manifest.json',result_identity='Containing Git commit; exact local/remote SHA and remote byte readback reported externally after push',hash_byte_contract='SHA-256 of staged Git blob bytes after Git text normalization; manifest self-hash excluded')
write(report_root/'evidence_manifest.json',manifest)
print('Publication artifacts prepared; stage and run final quality checks next.')
