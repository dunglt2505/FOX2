"""Run current checks and construct P2-02 result evidence, before submission."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[3]
os.chdir(ROOT)
OUT=Path('reports/FOX2-M1-P2-02'); EV=OUT/'evidence'
BASE='a99d50dd76af29deaf21e9a1a6a882b7e8047ca6'
UPSTREAM='4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3'
BRANCH='work/FOX2-M1-P2-02-store-codex'
LOCK='docs/agent_handoff/M1/P2-02/FOX2_M1_P2_02_SQLITE_STORE_PREDEV_SOURCE_LOCK_20261014.md'
HANDOFF='docs/agent_handoff/M1/P2-02/FOX2_M1_P2_02_CODEX_EXECUTE_20261014.md'
started=datetime.now(timezone.utc).isoformat()
def git(*args):return subprocess.check_output(['git',*args])
def hash_bytes(value):return hashlib.sha256(value).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
def changed_paths():
    return sorted(set(git('ls-files','--others','--exclude-standard').decode().splitlines()
                      +git('diff','HEAD','--name-only').decode().splitlines()))
assert git('branch','--show-current').decode().strip()==BRANCH
assert git('rev-parse','HEAD').decode().strip()==BASE
assert git('rev-parse','e9e5749fbcebd392facfd06c96e38bf02a4b4e8c:'+LOCK).decode().strip()=='55e8ebf6d09b02d1dc3d3b73ceb4c2c1333d348e'
assert not Path(git('rev-parse','--git-path','index.lock').decode().strip()).exists()
sources=[]
for commit,path in [(BASE,LOCK),(BASE,HANDOFF),
 ('63c9c0e86ba8892f96566189def63cb8afe33cf2','docs/governance/FOX2_POLICY_V1.8.5.md'),
 ('63c9c0e86ba8892f96566189def63cb8afe33cf2','docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_6_EFFECTIVE_ROUTING_INDEX_20261013.md')]:
    data=git('show',commit+':'+path)
    sources.append(dict(commit=commit,path=path,blob=git('rev-parse',commit+':'+path).decode().strip(),sha256=hash_bytes(data)))
for path in ['docs/architecture/FOX2_M1_TECHNICAL_SPEC_v0.1.md','docs/roadmap/FOX2_M1_P2_WP_PLAN_v0.1.md',
 'docs/data_contracts/FOX2_MARKET_DATA_CONTRACT_v0.4.md','docs/data_contracts/FOX2_MARKET_DATA_v0.4.schema.json',
 'docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv','docs/brd_mirror/FOX2-BRD-06_v0.5.md']:
    data=git('show',BASE+':'+path)
    sources.append(dict(commit=BASE,path=path,blob=git('rev-parse',BASE+':'+path).decode().strip(),sha256=hash_bytes(data)))
for part in ['ports/store.py','ports/preferences.py','ports/outcomes.py','contracts/market.py','validation/schema.py','validation/semantics.py']:
    path='backend/src/fox2/'+part
    assert git('rev-parse',BASE+':'+path)==git('rev-parse',UPSTREAM+':'+path)
    assert Path(path).read_bytes().replace(b'\r\n',b'\n')==git('show',UPSTREAM+':'+path)
write(EV/'source_readback.json',dict(observed_at_utc=started,sources=sources,frozen_interfaces='PASS unchanged six accepted files',
    writer='Race-sensitive check: exact remote HEAD; target absent; branch unattached; no observable active P2-02 process or Bridge execution. Generic Agent sessions not exhaustively observable.',
    grant='Exact executable handoff section 0 and user execution instruction; task-bound code/report writes and own branch push only.'))
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT/'backend/src'))
tests=[]
for name,args in [('p2_02',['tests/p2_02']),('p2_01_regression',['tests/p2_01','-k','not test_domain_dependency_boundary'])]:
    cmd=[sys.executable,'-B','-m','pytest',*args,'-p','no:cacheprovider','-q','--tb=short',
         '--junitxml='+str(EV/(name+'.xml'))]
    run=subprocess.run(cmd,env=env,capture_output=True,text=True)
    (EV/(name+'.txt')).write_text(run.stdout+run.stderr,encoding='utf-8',newline='\n')
    assert run.returncode==0,run.stdout+run.stderr
    tree=ET.parse(EV/(name+'.xml'))
    suites=tree.getroot().findall('testsuite')
    tests.append(dict(id=name,kind='OTHER',status='PASS',command_or_method=' '.join(cmd),environment='Windows; installed Python/pytest/SQLite; offline socket/DNS denial',
        run_at_utc=datetime.now(timezone.utc).isoformat(),evidence_ids=[name],notes=run.stdout.strip(),counts=[s.attrib for s in suites]))
sys.path.insert(0,str(ROOT/'backend/src'))
from fox2.store import SQLiteStore
from fox2.store.migrations import VERSION,CHECKSUM
import sqlite3,pytest,fastapi,pydantic,jsonschema
with tempfile.TemporaryDirectory(prefix='FOX2-P2-02-evidence-') as folder:
    store=SQLiteStore(Path(folder)/'fox2-integrity',instrument_registry=lambda i:False)
    integrity=store.integrity()
assert integrity['integrity_check']=='ok' and integrity['foreign_key_check']==[]
write(EV/'integrity.json',dict(run_at_utc=started,source_commit=BASE,sqlite_runtime=sqlite3.sqlite_version,migration_version=VERSION,
    migration_checksum=CHECKSUM,checks=integrity,temporary_database='outside Git; removed by TemporaryDirectory',
    network_provider_activity=0,network_proof='autouse socket/DNS attempt assertions; fresh-process forbidden-import/socket tests; crash subprocess denial. No provider/broker implementation.'))
paths=changed_paths()
allowed=lambda p:p.startswith(('backend/src/fox2/store/','tests/p2_02/','reports/FOX2-M1-P2-02/'))
assert all(allowed(p) for p in paths)
assert all(allowed(p) for p in git('diff','HEAD','--name-only').decode().splitlines())
syntax=[]
for path in paths:
    if path.endswith('.py'):
        compile(Path(path).read_bytes(),path,'exec');syntax.append(path)
    assert not Path(path).suffix.lower() in ('.db','.sqlite','.sqlite3','.pyc')
    assert not any(x in Path(path).parts for x in ('__pycache__','.venv','.pytest_cache'))
patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{30,}',r'AKIA[A-Z0-9]{16}',
          r'(?i)(?:password|api_key|access_token)\s*[:=]\s*[\"\x27][A-Za-z0-9_/-]{20,}']
for path in paths:
    content=Path(path).read_text(encoding='utf-8')
    assert not any(re.search(pattern,content) for pattern in patterns),'Secret pattern: '+path
assert subprocess.run(['git','diff','--check']).returncode==0
write(EV/'quality.json',dict(run_at_utc=started,syntax='PASS',syntax_files=syntax,scope='PASS',secret_scan='PASS obvious patterns plus synthetic-fixture review',
    frozen_files='PASS; entire preexisting tracked tree unchanged',git_diff_check='PASS; staged additions checked again before commit',
    versions=dict(python=sys.version.split()[0],pytest=pytest.__version__,sqlite=sqlite3.sqlite_version,fastapi=fastapi.__version__,pydantic=pydantic.__version__,git=git('--version').decode().strip()),
    failures_resolved=['Initial run: 43 failed/16 passed; frozen DTO assignments and test datetime serialization corrected using immutable copies.',
    'Next run: 1 failed/58 passed; same-batch chronological bars could not advance with equal verified source order; bar ordering rule corrected.',
    'Combined run: 2 failed/173 passed; missing adapter now quarantines contextual evidence gaps; obsolete P2-01 no-store stage assertion remains unchanged and is deselected with a P2-02 replacement dependency test.',
    'Default shell temporarily missing during execution; explicit installed Windows PowerShell ran successfully; no security refusal or bypass.'],
    model='GPT-6 session identity; exact variant NOT_EXPOSED',thinking='NOT_EXPOSED',quota='NOT_EXPOSED'))
mapping={
 'FOX2-06-T10':'test_poll_idempotency_receipt_identity_and_restart; test_correction_lineage_pit_replacement_and_exact_history; test_out_of_order_and_same_time_events_do_not_choose_arrival; test_series_isolation_and_ambiguous_read',
 'FOX2-06-T11':'test_correction_lineage_pit_replacement_and_exact_history; test_backdated_or_future_availability_rejected; test_trusted_receipt_processing_lag_does_not_backdate_verification',
 'FOX2-06-T12':'test_migration_reopen_and_integrity; test_committed_ingest_survives_process_restart; test_process_crash_rolls_back_hot_journal',
 'FOX2-06-T17':'test_each_ingest_stage_failure_rolls_back; test_reader_snapshot_is_old_until_writer_commits; test_second_bar_failure_rolls_back_entire_batch',
 'FOX2-06-T21':'test_correction_lineage_pit_replacement_and_exact_history; test_provisional_to_final_requires_lineage; test_ambiguous_finality_or_order_quarantines',
 'FOX2-06-T23':'test_rights_expiry_revocation_restart_and_no_fallback; test_changed_rights_are_not_a_market_revision',
 'FOX2-N1-T05':'test_series_isolation_and_ambiguous_read; test_cross_series_predecessor_rejected_atomically; test_unknown_basis_quarantine_not_merged',
 'FOX2-N1-T06':'test_backdated_receipt_and_clock_regression_rejected; test_correction_lineage_pit_replacement_and_exact_history',
 'FOX2-N1-T07':'test_rights_expiry_revocation_restart_and_no_fallback; test_blocked_candidate_cannot_displace_verified_projection'}
csv=git('show',BASE+':docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv').decode()
assert all(i in csv for i in mapping)
summary='\n'.join(f'- {t["id"]}: {t["notes"].splitlines()[-1]}' for t in tests)
rows='\n'.join(f'| {key} | PASS offline subcase / PARTIAL canonical | {value} |' for key,value in mapping.items())
report=f'''# FOX2 M1-P2-02 delivery result

Prepared for PUSHED_UNREVIEWED; successful push and exact remote SHA are reported separately. CHAT owns independent review and acceptance. No self-referencing commit SHA appears in this manifest.

## Task and authority

- Worktree: `{ROOT}`; created this run, clean at creation, CODEX-only task scope.
- Branch: `{BRANCH}`; initial local/remote HEAD `{BASE}`.
- Executable handoff: `{BASE}:{HANDOFF}`.
- Source/design lock: `e9e5749fbcebd392facfd06c96e38bf02a4b4e8c:{LOCK}`; blob `55e8ebf6d09b02d1dc3d3b73ceb4c2c1333d348e`.
- Accepted P2-01 `{UPSTREAM}` reused without implementation changes. Policy V1.8.5, Routing V1.2.6, Technical v0.1, P2 Plan v0.1, BRD-06 v0.5, Contract/schema and Acceptance v0.4 pinned in source_readback.json.
- Race check reused the preceding local precheck: exact branch HEAD, absent destination, no attached branch, no observable P2-02 writer/Bridge execution. Generic Agent runtime session targets remain incompletely observable; no collision observed. No package install.
- Agent: CODEX / operational; GPT-6 session identity, exact model variant/thinking/numeric quota NOT_EXPOSED. No model switch claimed; usage NOT_MEASURED.

## Delivered behavior

The stdlib SQLite repository implements the three frozen ports in store-owned files. Migration version {VERSION}, checksum `{CHECKSUM}`. Ordered SQL statements execute in one transaction with schema/profile identity and checksum checks. Tampered, future or unrelated databases are refused. DELETE rollback journal, FULL synchronization, foreign keys, immutable-history triggers, series-scoped projection constraints and bounded busy timeout (default 250 ms) are explicit choices tested under close/reopen, concurrency and hard subprocess exits.

Receipt IDs/raw hashes and market IDs/fingerprints are separate. Canonical fingerprints exclude receipt/local revision, selection and rights metadata. Duplicate polls append receipt linkage without another market revision. Source revision labels remain original provenance. Per-bar batch revisions commit atomically, retain cumulative replacements and preserve RAW/ADJUSTED/source identity. The frozen singular batch CommitResult identifies the first input item and indicates whether any item promoted; receipt_records/selection_audit retain every item.

Trusted clock verification sets first_available_at; no provider/event/bar/envelope timestamp establishes availability. Trusted receipts have a bounded 0–5 second verification delay; original availability claims must be absent/current, except known duplicate availability. PIT reads use immutable promotion history and hide future-known corrections across restart. Current retained-use rights remain independent from the historical cutoff. Expiry/revocation blocks reads, polling cannot re-grant, and no unauthorized source fallback occurs.

Promotion requires explicit trusted local identity/lifecycle/calendar/context evidence and verified integer ordering; no provider ordering is inferred. Corrections require exact same-series/logical predecessor with increasing verified order; final-to-provisional cannot displace current. Newer same-series daily bars advance on verified chronology and nondecreasing evidenced order; quote events require newer market time and increasing order. Same-time events remain distinct and ambiguous. Missing evidence quarantines; invalid candidates reject; both preserve current. Multiple eligible series use Unavailable(UNKNOWN), as required by the frozen selector-free read port.

Watchlist compare-and-replace validates trusted instrument IDs, duplicates, size and version, then commits list/version/time atomically. Conflict/failure does not mutate; tests cover competing CAS writers and restart.

Paths are explicit FOX2-only roots outside Git, with legacy Data/Fox, symlink and junction rejection on each connection. Isolated-test and investor store profiles cannot mix. All tests use synthetic values and temporary DBs outside Git. No API/DSM/provider/Bridge/SFR/frontend implementation, credentials, real feed, private account information, PR, main merge, deployment or LIVE.

## Current validation

{summary}

Executed commands and UTC/environment are in the manifest and JUnit/log evidence. Delivery runner: `python -B reports/FOX2-M1-P2-02/evidence/verify_delivery.py`. P2-02 command: `python -B -m pytest tests/p2_02 -p no:cacheprovider -q --tb=short --junitxml=reports/FOX2-M1-P2-02/evidence/p2_02.xml`. P2-01 command: `python -B -m pytest tests/p2_01 -k "not test_domain_dependency_boundary" -p no:cacheprovider -q --tb=short --junitxml=reports/FOX2-M1-P2-02/evidence/p2_01_regression.xml`.

One frozen P2-01 test asserts the store directory does not yet exist. Its expected P2-01-stage assertion fails at P2-02 and remains untouched; the relevant 79-test regression subset excludes it. P2-02 `test_domain_dependency_boundary_for_p2_02_stage` repeats its full domain import rules and provider/DSM exclusion while permitting the now-authorized store. Fresh-process network/import denial also passes. This exclusion does not claim the unchanged complete P2-01 suite passes at P2-02.

Failure history is explicit in quality.json: initial frozen DTO assignment/fixture serialization mistakes, same-batch ordering, contextual missing evidence and the obsolete stage assertion were resolved inside this scope. Required current suites pass. Temporary default-shell startup failure was resolved using installed explicit PowerShell; no platform security refusal occurred.

Integrity/FK/migration/syntax/allowlist/obvious-secret checks PASS. Network/provider/broker construction and socket/DNS attempts measured as zero in test denial regions. Git readback/push are the only authorized remote operations. All preexisting tracked files, including P2-01 code/tests and pyproject, are unchanged. Final staged whitespace/scope/secret/hash checks run before commit.

## Acceptance mapping

| ID | Status | Executed evidence |
| --- | --- | --- |
{rows}

All nine official IDs remain PARTIAL for full canonical scenarios; only listed offline subcases PASS. The schema has no PARTIAL acceptance enum, so manifest entries conservatively use NOT_RUN for the remaining canonical integrated obligations, with the local PASS reason/evidence.

## Limits and remaining gates

Trusted registry/clock/evidence are local injected dependencies, not provider certification. No source-selection adapter, rights re-grant workflow or application wiring is delivered. SQLITE FULL/DELETE durability is tested through forced process exit/reopen; physical power loss, real disk exhaustion and real provider timing/finality are NOT_RUN. Disk failures are injected deterministically. Rights and observations share a consistent transaction snapshot; later requests observe committed revocation.

CHAT immutable-SHA review and acceptance remain open. Integrated provider/store/DSM/API/frontend behavior, real licensing/LIVE, broker/account operations and deployment are NOT_RUN/outside scope. Commit command: `git commit -m "feat(p2-02): add atomic SQLite versioned store and offline evidence"`. Push: `git push origin HEAD:refs/heads/{BRANCH}`; readback: `git ls-remote origin refs/heads/{BRANCH}`. STOP after successful verified PUSHED_UNREVIEWED.
'''
(OUT/'report.md').write_text(report,encoding='utf-8',newline='\n')
manifest=json.loads(Path('reports/FOX2-M1-P2-01/evidence_manifest.json').read_text())
finished=datetime.now(timezone.utc).isoformat()
manifest.update(wp_id='FOX2-M1-P2-02',task_id='M1-P2-02',change_id='P2-02-SQLite-store',submission_state='READY_FOR_CHAT_REVIEW',submitted_at_utc=finished)
manifest['agent'].update(model='GPT-6; exact variant NOT_EXPOSED',mode='MANUAL_LOCAL / bounded task execution',started_at_utc=started,finished_at_utc=finished)
manifest['routing']={**{k:'PASS' for k in manifest['routing'] if k!='routing_evidence'},'routing_evidence':'P2-02 precheck PASS reused; exact handoff task grant; immediate race checks PASS; no observed writer collision.'}
manifest['source']=dict(policy_sha256=sources[2]['sha256'],policy_version='V1.8.5',task_commit_sha=BASE,source_manifest_sha256=hash_bytes((EV/'source_readback.json').read_bytes()),approved_base_commit_sha=BASE,
    source_readback_status='PASS',brd_revisions=['BRD-06 v0.5; Market/Acceptance v0.4; M1 Technical v0.1'],previous_evidence_reused=['P2-01 accepted '+UPSTREAM,'Read-only P2-02 precheck PASS'])
manifest['permissions'].update(grant_evidence='P2-02 executable handoff '+BASE+' section 0 plus user execution authorization; race check PASS; no PR/merge/deployment/provider/broker/LIVE.')
manifest['git'].update(branch=BRANCH,worktree=str(ROOT),writer_lease='CODEX-only task lane; no material P2-02 collision observed',report_path=(OUT/'report.md').as_posix(),local_head_before_submission=BASE,delivery_status='PUSHED_UNREVIEWED')
paths=changed_paths()
manifest['scope']=dict(requested=['Complete bounded P2-02 SQLite store and result delivery'],completed=['Versioned checked migration','Immutable receipt/market lineage and idempotency','Trusted availability and PIT','Deterministic promotion/quarantine','Atomic rollback/restart/concurrency','Rights retained-use boundary','Watchlist CAS','Offline tests and P2-01 regression subset'],partial=['Canonical integrated acceptance'],not_done=['Independent CHAT review','Integrated provider/API/DSM/frontend acceptance'],explicit_exclusions=['Frozen P2-01 files and pyproject','API/DSM/provider/frontend/Bridge/SFR/docs/.github','PR/main/merge/deployment/Production/broker/LIVE'],changed_paths=[dict(path=p,operation='ADD',intent='P2-02 SQLite store, isolated offline tests or authorized result evidence',within_allowed_paths=True,new_sha256=hash_bytes(Path(p).read_bytes())) for p in paths if not p.endswith('/evidence_manifest.json')],forbidden_paths_touched=False)
manifest['tests']=[{k:v for k,v in t.items() if k!='counts'} for t in tests]
manifest['acceptance']=[dict(id=i,status='NOT_RUN',evidence_ids=['p2_02'],reason='Offline subcase PASS: '+mapping[i]+'. Canonical integrated/provider scenario PARTIAL/NOT_RUN; no schema PARTIAL enum.') for i in mapping]
manifest['evidence']=[dict(id=p.stem,path=p.as_posix(),sha256=hash_bytes(p.read_bytes()),kind='TEST_LOG' if p.suffix in ('.txt','.xml') else 'OTHER',observed_at_utc=finished,description=p.name,supports_ids=[t['id'] for t in tests],sanitized=True) for p in sorted(EV.iterdir()) if p.is_file()]
# Log and XML have the same stem; evidence IDs must be unique.
for item in manifest['evidence']:
    if item['path'].endswith('.xml'):item['id']+='_junit'
manifest['risks']=[dict(id='integration',severity='MEDIUM',state='OPEN',impact='Offline foundation only; provider ordering and integrated acceptance remain unverified',next_action='CHAT independent SHA review before downstream WP',owner_role='CHAT')]
manifest['security'].update(check_notes='Obvious-pattern changed-file scan and synthetic-fixture review; no private/licensed/credential material.')
manifest['usage'].update(attempts=1,retries=0,escalation_reason='None; development failures corrected in scope, recorded in quality evidence')
manifest['next_step'].update(action='Independently read remote SHA and review P2-02 result before acceptance',prerequisite_gate='Successful designated-branch push and exact remote SHA readback')
schema=json.loads(Path('docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json').read_text())
jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(manifest)
write(OUT/'evidence_manifest.json',manifest)
print(summary)
print('Source/frozen files, SQLite integrity/migration, syntax, scope, secret scan and result schema PASS')
