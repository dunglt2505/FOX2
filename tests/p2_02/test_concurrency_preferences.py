from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
import time
import pytest
from fox2.ports.outcomes import PreferenceConflict, PreferenceFailure, Unavailable
from fox2.contracts.watchlist import WatchlistPreference
from test_store import query, change


def test_watchlist_atomic_cas_and_restart(h):
    assert h.store.get_preferences().version==0
    result=h.store.replace_if_version(0,['TEST:AAA','TEST:BBB'])
    assert isinstance(result,WatchlistPreference) and result.version==1 and result.updated_at==h.now
    assert h.store.replace_if_version(0,['TEST:CCC'])==PreferenceConflict(1)
    h.store=h.open()
    assert h.store.get_preferences()==result
    assert h.store.replace_if_version(1,[]).version==2


@pytest.mark.parametrize('version,items,reason',[(0,['TEST:AAA','TEST:AAA'],'INVALID_ITEMS'),
    (0,['TEST:UNKNOWN'],'UNKNOWN_INSTRUMENT'),(0,[f'TEST:{i}' for i in range(101)],'INVALID_ITEMS'),
    (-1,[],'INVALID_ITEMS'),(True,[],'INVALID_ITEMS'),(0,'TEST:AAA','INVALID_ITEMS'),
    (0,[''],'INVALID_ITEMS'),(0,[1],'INVALID_ITEMS'),(0,None,'INVALID_ITEMS')])
def test_watchlist_invalid_never_mutates(h,version,items,reason):
    before=h.store.get_preferences()
    assert h.store.replace_if_version(version,items)==PreferenceFailure(reason)
    assert h.store.get_preferences()==before


@pytest.mark.parametrize('stage',['preference_begin','preference_validated','preference_updated','preference_commit'])
def test_watchlist_failure_rolls_back(h,stage):
    before=h.store.replace_if_version(0,['TEST:AAA'])
    def fault(s):
        if s==stage:raise OSError('injected storage error')
    h.hook=fault
    assert h.store.replace_if_version(1,['TEST:BBB'])==PreferenceFailure('UNSAFE_STORE')
    h.hook=lambda s:None;h.store=h.open()
    assert h.store.get_preferences()==before


def test_writer_lock_timeout_and_no_partial_mutation(h):
    first=h.ingest(h.observation());h.now+=timedelta(minutes=1)
    with sqlite3.connect(h.store.path,isolation_level=None) as blocker:
        blocker.execute('BEGIN IMMEDIATE')
        start=time.monotonic()
        result=h.ingest(h.observation(record_id='writer-two'))
        elapsed=time.monotonic()-start
        assert result.status=='UNAVAILABLE' and result.reason=='UNSAFE_STORE'
        assert .15<=elapsed<2.
        assert h.store.replace_if_version(0,['TEST:AAA'])==PreferenceFailure('UNSAFE_STORE')
        blocker.rollback()
    assert query(h,'SELECT count(*) FROM observations')==[(1,)]
    assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==first.record_id
    assert h.store.integrity()['foreign_key_check']==[]


def test_two_writers_serialize_one_revision_and_two_receipts(h):
    o=h.observation()
    barrier=threading.Barrier(2)
    from fox2.ports.outcomes import IngestAudit
    def write(n):
        barrier.wait(timeout=3)
        return h.store.append_and_promote(o,IngestAudit(f'concurrent-{n}',h.now,f'{n:064x}'))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(write,[1,2]))
    assert sorted(r.status for r in results)==['COMMITTED','UNCHANGED']
    assert query(h,'SELECT count(*) FROM observations')==[(1,)]
    assert query(h,'SELECT count(*) FROM ingest_receipts')==[(2,)]


def test_two_watchlist_cas_writers_only_one_wins(h):
    barrier=threading.Barrier(2)
    def write(item):
        barrier.wait(timeout=3)
        return h.store.replace_if_version(0,[item])
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(write,['TEST:AAA','TEST:BBB']))
    assert sum(isinstance(r,WatchlistPreference) for r in results)==1
    assert sum(isinstance(r,PreferenceConflict) for r in results)==1
    assert h.store.get_preferences().version==1


def test_reader_snapshot_is_old_until_writer_commits(h):
    o=h.observation();first=h.ingest(o)
    h.now+=timedelta(minutes=1);h.parent=first.record_id;h.order=2
    changed=change(o,'payload.last_price',101.)
    inserted=threading.Event();release=threading.Event()
    def fault(stage):
        if stage=='ingest_projection':
            inserted.set();assert release.wait(3)
    h.hook=fault
    with ThreadPoolExecutor(max_workers=1) as pool:
        writer=pool.submit(h.ingest,changed)
        assert inserted.wait(3)
        # Separate reader sees old pointer while new projection/audit are uncommitted.
        assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==first.record_id
        assert query(h,'SELECT count(*) FROM observations')==[(1,)]
        assert query(h,'SELECT count(*) FROM ingest_receipts')==[(1,)]
        release.set();result=writer.result(timeout=3)
    assert result.promoted
    assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==result.record_id
    assert query(h,'SELECT count(*) FROM ingest_receipts')==[(2,)]


def test_rights_and_observation_share_reader_snapshot(h):
    h.ingest(h.observation())
    series=query(h,'SELECT series_key FROM series')[0][0]
    reading=threading.Event();revoke_written=threading.Event();release=threading.Event()
    def hook(stage):
        if stage=='read_snapshot':
            reading.set();assert revoke_written.wait(3)
        elif stage=='unused':assert release.wait(3)
    h.hook=hook
    # A second SQLite writer can stage revocation; COMMIT waits for the reader.
    def revoke():
        assert reading.wait(3)
        with sqlite3.connect(h.store.path,isolation_level=None,timeout=2) as c:
            c.execute('PRAGMA foreign_keys=ON');c.execute('BEGIN IMMEDIATE')
            c.execute("INSERT INTO rights_registry(series_key,read_state,retained_state,evidence_ref,verified_until,observed_at,revoked) VALUES(?,?,?,?,?,?,1)",
                (series,'BLOCKED','BLOCKED','snapshot-test',None,h.now.isoformat()))
            revoke_written.set();c.commit()
    with ThreadPoolExecutor(max_workers=1) as pool:
        writer=pool.submit(revoke)
        result=h.store.get_observation('TEST:AAA','QUOTE',None)
        assert not isinstance(result,Unavailable)
        writer.result(timeout=3)
    h.hook=lambda stage:None
    assert h.store.get_observation('TEST:AAA','QUOTE',None)==Unavailable('RIGHTS_BLOCKED')


CHILD = r'''
import os,socket,sys,json
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tests/p2_02'))
from conftest import Harness
def denied(*args,**kwargs): raise AssertionError('network forbidden in crash subprocess')
socket.create_connection=socket.getaddrinfo=denied
for n in ('connect','connect_ex','bind','listen','sendto'):setattr(socket.socket,n,denied)
h=Harness(Path(sys.argv[1]))
o=h.observation()
from fox2.contracts.market import MarketObservation
o=MarketObservation.model_validate_json(sys.argv[3])
from datetime import datetime
h.now=datetime.fromisoformat(sys.argv[4]);h.order=2;h.parent=sys.argv[5] or None
def hook(stage):
    if stage==sys.argv[2]:os._exit(73)
h.hook=hook
h.ingest(o,audit_id='child-crash')
os._exit(0)
'''


@pytest.mark.parametrize('stage',['ingest_observation','ingest_projection','ingest_receipt','ingest_commit'])
def test_process_crash_rolls_back_hot_journal(h,stage):
    original=h.observation();first=h.ingest(original)
    h.now+=timedelta(minutes=1)
    changed=change(original,'payload.last_price',101.)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(Path.cwd()/'backend/src'))
    run=subprocess.run([sys.executable,'-B','-c',CHILD,str(h.root),stage,changed.model_dump_json(),h.now.isoformat(),first.record_id],env=env,capture_output=True,text=True,timeout=10)
    assert run.returncode==73,run.stderr
    h.store=h.open()
    assert query(h,'SELECT count(*) FROM observations')==[(1,)]
    assert query(h,'SELECT count(*) FROM ingest_receipts')==[(1,)]
    assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==first.record_id
    assert h.store.integrity()['integrity_check']=='ok'


def test_committed_ingest_survives_process_restart(h):
    o=h.observation()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(Path.cwd()/'backend/src'))
    run=subprocess.run([sys.executable,'-B','-c',CHILD,str(h.root),'no-failure',o.model_dump_json(),h.now.isoformat(),''],env=env,capture_output=True,text=True,timeout=10)
    assert run.returncode==0,run.stderr
    h.store=h.open()
    observed=h.store.get_observation('TEST:AAA','QUOTE',None)
    assert observed.payload.last_price==100. and observed.first_available_at==h.now
    assert query(h,'SELECT audit_id FROM ingest_receipts')==[('child-crash',)]
