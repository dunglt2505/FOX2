"""Verify only readback evidence and installed bytes; never calls the Vault service."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

out = Path(__file__).resolve().parent
root = out.parents[3]
def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def timestamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))
checks = {}
def check(name, condition):
    checks[name] = bool(condition)
    assert condition, name

attempt = load(out/'attempt.json')
ui = load(out/'ui_process_before.json')
ui_after = load(out/'ui_process_after.json')
before = load(out/'vault_index_before.json')
after = load(out/'vault_index_after.json')
vault = Path(attempt['vault_root'])
pointer_path = Path(os.environ['LOCALAPPDATA'])/'FOX2/AgentBridge/current.json'
pointer = load(pointer_path)
package = root/'reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_recovery_003/FOX2-Bridge-RC1.zip'
expected = 'a0516aed3d69564c657dc557b7b09cfaab549d6ab04ce4132e9399b50ce5b4ac'
check('package_archive_matches_installed_pointer', sha(package) == pointer['package_sha256'] == expected)
version = pointer_path.parent/'versions'/expected
receipt = load(version/'receipt.json')
payload_checks = {name: sha(version/'payload'/name) == digest for name, digest in receipt['manifest']['files'].items()}
check('installed_payload_all_manifest_hashes', all(payload_checks.values()))
check('current_ui_path_is_installed_package', Path(ui['path']).resolve() == (version/'payload/desktop/FOX2.Bridge.Desktop.exe').resolve())
check('same_ui_process_before_after', ui['pid'] == ui_after['pid'] and ui['start_utc'] == ui_after['start_utc'])
check('ui_exe_and_assembly_match_manifest', ui['exe_sha256'] == receipt['manifest']['files']['desktop/FOX2.Bridge.Desktop.exe'] and ui['assembly_sha256'] == receipt['manifest']['files']['desktop/FOX2.Bridge.Desktop.dll'])
source = Path(attempt['source_path'])
digest = sha(source)
check('selected_source_hash_unchanged', digest == attempt['source_sha256'])
check('fresh_hash_not_in_prior_index', not any(row['Sha256'] == digest for row in before))
check('exactly_one_new_record', len(after) == len(before)+1 and len([row for row in after if row['Sha256'] == digest]) == 1)
check('prior_records_unchanged', all(row in after for row in before))
record = next(row for row in after if row['Sha256'] == digest)
check('content_addressed_artifact_id', record['ArtifactId'] == 'sha256:'+digest)
check('content_addressed_object_path', record['VaultPath'] == 'objects\\'+digest+'\\file_'+source.name)
obj = vault/record['VaultPath']
check('object_hash_matches_selected_source', sha(obj) == record['Sha256'] == digest)
check('exact_source_object_bytes', obj.read_bytes() == source.read_bytes())
check('source_record_object_size_matches', source.stat().st_size == record['SizeBytes'] == obj.stat().st_size == attempt['source_size'])
check('exact_local_saved_state', record['State'] == 'LOCAL_SAVED')
# RC1 serializes one canonical State field; no raw boolean fields are invented.
check('not_git_synced', record['State'] != 'GIT_SYNCED' and record.get('git_synced', False) is False)
check('not_released', record['State'] != 'RELEASED' and record.get('released', False) is False)
saved = timestamp(record['SavedAtUtc'])
check('saved_after_ui_process_start', saved > timestamp(ui['start_utc']))
check('saved_after_final_closure_attempt_start', saved > timestamp(attempt['attempt_started_utc']))
check('saved_before_readback', saved < timestamp(ui_after['observed_utc']))
events = load(out/'atomic_index_events.json')['events']
old = [e for e in events if e['action'] == 'RENAMED_OLD_NAME' and e['name'].startswith('.index-')]
new = [e for e in events if e['action'] == 'RENAMED_NEW_NAME' and e['name'] == 'index.json']
check('native_temporary_to_index_rename_observed', len(old) == len(new) == 1 and events.index(old[0])+1 == events.index(new[0]))
check('atomic_rename_after_saved_record_timestamp', timestamp(new[0]['observed_utc']) > saved)
file_id_before = load(out/'observer_ready.json')['index_file_id_before']
file_id_after = (vault/'index.json').stat().st_ino
check('index_replaced_by_new_file_identity', file_id_before != file_id_after)
check('complete_live_index_equals_after_snapshot', (vault/'index.json').read_bytes() == (out/'vault_index_after.json').read_bytes())
check('no_pending_index_or_copy_files', not list(vault.glob('.index-*')) and not list((obj.parent).glob('.copy-*')))
ui_steps = load(out/'ui_action_receipt.json')
check('actual_installed_ui_picker_and_result', any(s['step']=='explicit_source_selected' and str(source) in s['proof'] for s in ui_steps) and any(s['step']=='after_native_open_ui_save' and digest in s['accessibility']['tree'] for s in ui_steps))
check('no_product_changes_since_certified_source', not subprocess.check_output(['git','diff','dbaefdf686e06ffdf78b277288515deca9011710','--','agent_bridge'],cwd=root).strip())
shutil.copyfile(obj, out/'saved_vault_object.txt')
result = dict(status='PASS', checks_passed=len(checks), checks=checks, package_sha256=expected, installed_payload_files_verified=len(payload_checks), ui=ui, ui_after=ui_after, attempt_started_utc=attempt['attempt_started_utc'], completed_utc=datetime.now(timezone.utc).isoformat(), source=dict(path=str(source),sha256=digest,bytes=source.stat().st_size), artifact=record, object_absolute_path=str(obj), object_sha256=sha(obj), index_before_sha256=sha(out/'vault_index_before.json'),index_after_sha256=sha(out/'vault_index_after.json'),index_counts=dict(before=len(before),after=len(after)),index_file_ids=dict(before=file_id_before,after=file_id_after), normalized_semantics=dict(state=record['State'],git_synced=False,released=False,basis='Raw RC1 record serializes canonical State only; LOCAL_SAVED is neither GIT_SYNCED nor RELEASED. Boolean values here are explicit semantic interpretation, not claimed persisted fields.',persisted_git_synced_field='git_synced' in record,persisted_released_field='released' in record), gates={gate:'PASS' for gate in ('ARTIFACT_LOCAL_SAVE','ARTIFACT_SHA256_VERIFY','ARTIFACT_ATOMIC_INDEX','LOCAL_SAVED_NOT_GIT_SYNCED','INSTALLED_UI_ARTIFACT_FRESHNESS')})
(out/'artifact_ui_certification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(status='PASS',checks_passed=len(checks),payload_files=len(payload_checks),sha256=digest,saved_at_utc=record['SavedAtUtc'])))
