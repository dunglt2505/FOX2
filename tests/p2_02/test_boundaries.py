import ast
from datetime import timedelta
import os
from pathlib import Path
import subprocess
import sys
import pytest
from fox2.ports.outcomes import Unavailable
from fox2.store import SQLiteStore, StoreError
from test_store import query, change


def test_changed_rights_are_not_a_market_revision(h):
    o=h.observation();first=h.ingest(o)
    h.now+=timedelta(minutes=1)
    refreshed=change(o,'rights.verified_until',h.now+timedelta(days=4))
    duplicate=h.ingest(refreshed)
    assert duplicate.status=='UNCHANGED' and duplicate.record_id==first.record_id
    assert query(h,'SELECT count(*) FROM observations')==[(1,)]
    # Repeated DTO claims do not extend the original registry authorization.
    h.now+=timedelta(days=3)
    assert h.store.get_observation('TEST:AAA','QUOTE',None)==Unavailable('RIGHTS_BLOCKED')


def test_blocked_candidate_cannot_displace_verified_projection(h):
    o=h.observation();first=h.ingest(o)
    h.now+=timedelta(minutes=1);h.order=2;h.parent=first.record_id
    changed=change(change(o,'payload.last_price',101.),'rights.retained_use','BLOCKED')
    result=h.ingest(changed)
    assert result.status=='COMMITTED' and not result.promoted
    assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==first.record_id


def test_unknown_basis_quarantine_not_merged(h):
    first=h.ingest(h.observation())
    unknown=h.ingest(h.observation(price_basis='UNKNOWN'))
    assert unknown.status=='COMMITTED' and not unknown.promoted
    assert query(h,'SELECT count(*) FROM series')==[(2,)]
    assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==first.record_id


def test_missing_amount_stays_null_and_real_zero_survives(h):
    o=change(h.observation(),'payload.cumulative_volume',0.)
    o=change(o,'payload.cumulative_turnover',None)
    o=change(o,'missing_fields',['payload.cumulative_turnover'])
    o=change(o,'completeness','PARTIAL')
    assert h.ingest(o).promoted
    result=h.store.get_observation('TEST:AAA','QUOTE',None)
    assert result.payload.cumulative_volume==0. and result.payload.cumulative_turnover is None


def test_missing_evidence_adapter_quarantines(h):
    h.store=h.open(evidence=lambda o:None)
    result=h.ingest(h.observation())
    assert result.status=='COMMITTED' and not result.promoted
    assert h.store.get_observation('TEST:AAA','QUOTE',None)==Unavailable('NOT_FOUND')


def test_read_cutoff_validation(h):
    h.ingest(h.observation())
    assert h.store.get_observation('TEST:AAA','QUOTE',h.now+timedelta(seconds=1))==Unavailable('UNKNOWN')
    assert h.store.get_observation('TEST:AAA','QUOTE',h.now.replace(tzinfo=None))==Unavailable('UNSAFE_STORE')
    assert h.store.get_observation('TEST:AAA','TICKS',None)==Unavailable('UNKNOWN')


def test_trusted_receipt_processing_lag_does_not_backdate_verification(h):
    receipt=h.now-timedelta(seconds=1)
    result=h.ingest(h.observation(),received=receipt)
    assert result.promoted
    observation=h.store.get_observation('TEST:AAA','QUOTE',None)
    assert observation.received_at==receipt and observation.first_available_at==h.now
    assert h.store.get_observation('TEST:AAA','QUOTE',receipt)==Unavailable('NOT_FOUND')


def test_read_investor_blocks_fixture_even_if_metadata_tampered(h):
    h.ingest(h.observation())
    # Simulate direct memory corruption/incorrect wiring, without editing DTO/DB.
    h.store.profile='INVESTOR'
    assert h.store.get_observation('TEST:AAA','QUOTE',None)==Unavailable('UNSAFE_STORE')


@pytest.mark.parametrize('timeout',[-1,5001,True])
def test_busy_timeout_is_bounded(h,timeout):
    with pytest.raises(StoreError):h.open(busy_timeout_ms=timeout)


def test_fresh_process_import_and_store_work_without_network_or_downstream(tmp_path):
    code=r'''
import builtins,socket,sys
from pathlib import Path
def denied(*a,**kw):raise AssertionError('zero-network proof')
socket.create_connection=socket.getaddrinfo=denied
for n in ('connect','connect_ex','bind','listen','sendto'):setattr(socket.socket,n,denied)
real_import=builtins.__import__
def guarded(name,*args,**kwargs):
    if name.split('.')[0] in ('fastapi','httpx','requests','aiohttp') or any(x in name for x in ('fox2.api','fox2.dsm','fox2.providers','fox2_agent_bridge')):
        raise AssertionError('forbidden downstream import')
    return real_import(name,*args,**kwargs)
builtins.__import__=guarded
from fox2.store import SQLiteStore
s=SQLiteStore(Path(sys.argv[1]),instrument_registry=lambda i:i=='TEST:AAA')
assert s.replace_if_version(0,['TEST:AAA']).version==1
assert s.integrity()['integrity_check']=='ok'
print('network_attempts=0; downstream imports=0; offline migration/CAS/read PASS')
'''
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(Path.cwd()/'backend/src'))
    run=subprocess.run([sys.executable,'-B','-c',code,str(tmp_path/'fox2-offline')],env=env,capture_output=True,text=True,timeout=10)
    assert run.returncode==0,run.stderr
    assert 'network_attempts=0' in run.stdout


def test_store_import_boundary_and_frozen_files():
    root=Path.cwd()
    for file in (root/'backend/src/fox2/store').glob('*.py'):
        tree=ast.parse(file.read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Import): names=[a.name for a in node.names]
            elif isinstance(node,ast.ImportFrom):names=[node.module or '']
            else:continue
            assert not any(n.startswith(('fastapi','httpx','requests','aiohttp','fox2.api','fox2.dsm','fox2.provider','tests.')) for n in names)
    for p in ('ports/store.py','ports/preferences.py','ports/outcomes.py','contracts/market.py',
              'validation/schema.py','validation/semantics.py'):
        path='backend/src/fox2/'+p
        expected=subprocess.check_output(['git','show','4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3:'+path])
        assert (root/path).read_bytes().replace(b'\r\n',b'\n')==expected


def test_domain_dependency_boundary_for_p2_02_stage():
    root=Path.cwd()/'backend/src/fox2'
    allowed={'typing','dataclasses','datetime','json','importlib','pydantic','jsonschema','fox2'}
    for group in ('contracts','validation','ports'):
        for file in (root/group).glob('*.py'):
            for node in ast.walk(ast.parse(file.read_text())):
                if isinstance(node,ast.Import):names=[a.name for a in node.names]
                elif isinstance(node,ast.ImportFrom):
                    if node.level:continue
                    names=[node.module or '']
                else:continue
                for name in names:
                    assert name.split('.')[0] in allowed,(file,name)
                    if name.startswith('fox2.'):
                        assert name.split('.')[1] in ('contracts','validation','ports'),(file,name)
    assert not (root/'provider').exists() and not (root/'dsm').exists()
    assert (root/'store').is_dir()
