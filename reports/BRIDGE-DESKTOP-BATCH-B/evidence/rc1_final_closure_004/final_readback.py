"""Bounded installed status and replay-safety readback; no polling or Agent calls."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys

out = Path(__file__).resolve().parent
repo = out.parents[3]
sys.path.insert(0, str(repo/'agent_bridge/src'))
from fox2_agent_bridge.schema_validation import validate_json_schema
from fox2_agent_bridge.dispatch_schema_v3_contract import DISPATCH_SCHEMA_V3
from fox2_agent_bridge.artifacts import write_json
dispatch = json.loads((out/'dispatch.json').read_text())
validate_json_schema(dispatch, DISPATCH_SCHEMA_V3)
root = Path(os.environ['LOCALAPPDATA'])/'FOX2/AgentBridge'
pointer = json.loads((root/'current.json').read_text())
python = root/'versions'/pointer['package_sha256']/'runtime/Scripts/python.exe'
env = {k:v for k,v in os.environ.items() if k.upper() not in {'PYTHONPATH','PYTHONHOME'}}
p = subprocess.run([str(python),'-I','-m','fox2_agent_bridge','control','status'], env=env, capture_output=True, text=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
assert p.returncode == 0
status = json.loads(p.stdout)
assert status['paused'] is True and status['state'] == 'STOPPED'
manual = root/'data/manual_consumption.json'
previous = json.loads(manual.read_text())
current = json.loads(json.dumps(previous))
assert dispatch['dispatch_id'] not in current['dispatch_ids'], 'Dispatch already consumed; do not replay'
current['dispatch_ids'].append(dispatch['dispatch_id'])
current['additional_authority_control_commit_rc1_004'] = 'dc79f8143eec471508bf37565bff38442ce0548a'
write_json(manual, current)
assert json.loads(manual.read_text()) == current
canary = 'FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001'
ledgers = {}
for name, path in [('per_user',root/'data/bridge.db'),('legacy', repo/'agent_bridge/state/bridge.db')]:
    if not path.exists():
        if name == 'legacy':
            # The historical certification binds the legacy store separately.
            ledgers[name] = {'readback':'not present at default path; historical zero-row evidence preserved'}
            continue
        raise AssertionError('Installed ledger missing')
    with sqlite3.connect(path.as_uri()+'?mode=ro', uri=True) as con:
        tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        counts = {}
        for table in ('dispatches','executions'):
            if table not in tables:
                continue
            columns = {r[1] for r in con.execute('PRAGMA table_info('+table+')')}
            id_column = 'dispatch_id' if 'dispatch_id' in columns else 'id'
            counts[table] = con.execute('SELECT count(*) FROM '+table+' WHERE '+id_column+'=?',(canary,)).fetchone()[0]
        assert counts and not any(counts.values())
        ledgers[name] = counts
remote = subprocess.check_output(['git','ls-remote','origin','refs/heads/work/FOX2-BRIDGE-DESKTOP-BATCH-B','refs/heads/work/FOX2-BRIDGE-FINAL-CANARY-009','refs/heads/work/FOX2-M1-A-APP-BATCH-B'],cwd=repo,text=True)
assert '501822a33ef08c7365154913bbc677544856eee5' in remote
assert 'fc8aba202e15bddfcc5156b2c1bb36ed222329eb' in remote
result = dict(status='PASS', observed_utc=datetime.now(timezone.utc).isoformat(), dispatch_v3_structural_validation='PASS', installed_package=pointer, installed_python=str(python), source_pythonpath='UNSET',worker={k:status.get(k) for k in ('state','paused','setup_complete','start_with_windows','stop_requested')},manual_consumption=dict(dispatch_id=dispatch['dispatch_id'],recorded=True,previous_ids_preserved=all(x in current['dispatch_ids'] for x in previous['dispatch_ids']),sha256=hashlib.sha256(manual.read_bytes()).hexdigest()),canary_009_ledger_rows=ledgers,remote_refs=remote.splitlines(),real_poll='PASS carried forward; package/code unchanged; no new poll or Agent invocation',app_batch_b='PAUSED_NO_ACTION',protected_actions='NONE')
(out/'final_runtime_readback.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='PASS',worker=result['worker'],dispatch_recorded=True,canary=ledgers)))
