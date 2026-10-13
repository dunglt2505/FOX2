from dataclasses import asdict
from datetime import timedelta
import json
import sqlite3
import pytest
from pathlib import Path
from fox2.ports.outcomes import Unavailable
from fox2.store import SQLiteStore, StoreError
from fox2.store.migrations import MigrationError, VERSION, CHECKSUM


def change(model, path, value):
    """Copy frozen DTO trees; negative tests may deliberately create invalid copies."""
    keys=path.split('.')
    def copy(node, keys):
        key=keys[0]
        if isinstance(node,list):
            result=list(node); index=int(key)
            result[index]=copy(result[index],keys[1:]) if len(keys)>1 else value
            return result
        child=copy(getattr(node,key),keys[1:]) if len(keys)>1 else value
        return node.model_copy(update={key:child},deep=True)
    return copy(model,keys)


def query(h, sql, args=()):
    with sqlite3.connect(h.store.path) as c:
        c.execute('PRAGMA foreign_keys=ON')
        return c.execute(sql, args).fetchall()


def test_migration_reopen_and_integrity(h):
    assert h.store.integrity() == {'integrity_check':'ok','foreign_key_check':[],
        'migration':[(VERSION,CHECKSUM)],'journal_mode':'delete','synchronous':2}
    h.store.close(); reopened = h.open()
    assert reopened.integrity() == h.store.integrity()
    tables = {r[0] for r in query(h,"select name from sqlite_master where type='table'")}
    assert {'observations','bar_revisions','current_projection','gaps','selection_audit',
            'rights_registry','watchlist_preferences','instruments','schema_migrations','ingest_receipts'} <= tables


@pytest.mark.parametrize('sql', ["UPDATE schema_migrations SET checksum='tampered'", 'PRAGMA user_version=99',
    'DELETE FROM schema_migrations', 'DROP TRIGGER immutable_observations_update', 'PRAGMA application_id=123'])
def test_migration_refuses_tamper_or_future(h, sql):
    query(h,sql)
    with pytest.raises(MigrationError): h.open()


@pytest.mark.parametrize('stage',['migration_before','migration_statement_0','migration_statement_8',
    'migration_statement_25','migration_after','migration_commit'])
def test_interrupted_migration_atomic(tmp_path,stage):
    root = tmp_path/'fox2-interrupted'
    def fault(s):
        if s==stage: raise OSError('injected disk failure')
    with pytest.raises(OSError):
        SQLiteStore(root, instrument_registry=lambda i: True, fault_hook=fault)
    with sqlite3.connect(root/'fox2.sqlite3') as c:
        assert c.execute("select name from sqlite_master where type='table'").fetchall()==[]
        assert c.execute('pragma user_version').fetchone()[0]==0
    restored=SQLiteStore(root,instrument_registry=lambda i: True)
    assert restored.integrity()['integrity_check']=='ok'


def test_unknown_database_untouched(tmp_path):
    root=tmp_path/'fox2-existing'; root.mkdir()
    with sqlite3.connect(root/'fox2.sqlite3') as c:
        c.execute('create table unrelated(value text)'); c.execute("insert into unrelated values('retain')")
    before=(root/'fox2.sqlite3').read_bytes()
    with pytest.raises(MigrationError): SQLiteStore(root,instrument_registry=lambda i: True)
    assert (root/'fox2.sqlite3').read_bytes()==before


def test_poll_idempotency_receipt_identity_and_restart(h):
    original=h.observation()
    result=h.ingest(original,audit_id='one',raw='a'*64)
    assert result.status=='COMMITTED' and result.promoted
    stored=h.store.get_observation('TEST:AAA','QUOTE',None)
    assert stored.record_id==result.record_id and stored.first_available_at==h.now
    assert h.ingest(original,audit_id='one',raw='a'*64)==result
    assert h.ingest(original,audit_id='one',raw='b'*64).status=='REJECTED'
    altered=change(original,'payload.last_price',101.)
    assert h.ingest(altered,audit_id='one',raw='a'*64).status=='REJECTED'
    h.now += timedelta(minutes=1)
    for _ in range(3):
        duplicate=original.model_copy(update={'received_at':h.now,'first_available_at':stored.first_available_at,
                                              'selection_audit_id':'another-selection'},deep=True)
        result2=h.ingest(duplicate)
        assert result2.status=='UNCHANGED' and result2.revision==1 and not result2.promoted
    assert query(h,'SELECT count(*) FROM observations')==[(1,)]
    assert query(h,'SELECT count(*) FROM ingest_receipts')==[(4,)]
    h.store=h.open()
    assert h.store.get_observation('TEST:AAA','QUOTE',None).first_available_at==stored.first_available_at


def test_correction_lineage_pit_replacement_and_exact_history(h):
    o=h.observation(bars=True); first=h.ingest(o); cutoff=h.now
    original=query(h,'SELECT payload_json,original_json FROM observations WHERE record_id=?',(first.record_id,))
    h.now+=timedelta(hours=1); h.order=2; h.parent=first.record_id
    changed=change(o,'payload.items.0.close',106.)
    changed=change(changed,'payload.items.0.volume',150.)
    changed=change(changed,'payload.items.0.turnover',15000.)
    changed=change(changed,'source_revision','provider-correction-label')
    second=h.ingest(changed)
    assert second.promoted and second.revision==2
    current=h.store.get_observation('TEST:AAA','BARS',None)
    assert current.payload.items[0].volume==150. and current.payload.items[0].turnover==15000.
    assert current.source_revision=='provider-correction-label'
    assert current.first_available_at==h.now
    before=h.store.get_observation('TEST:AAA','BARS',cutoff)
    assert before.record_id==first.record_id and before.payload.items[0].volume==100.
    assert h.store.get_observation('TEST:AAA','BARS',cutoff-timedelta(microseconds=1))==Unavailable('NOT_FOUND')
    h.store=h.open()
    assert h.store.get_observation('TEST:AAA','BARS',cutoff)==before
    assert query(h,'SELECT payload_json,original_json FROM observations WHERE record_id=?',(first.record_id,))==original
    assert query(h,'SELECT predecessor_record_id FROM observations WHERE record_id=?',(second.record_id,))==[(first.record_id,)]


@pytest.mark.parametrize('delta',[-1,1])
def test_backdated_or_future_availability_rejected(h,delta):
    o=h.observation(first_available_at=h.now+timedelta(seconds=delta))
    assert h.ingest(o).status=='REJECTED'
    assert query(h,'SELECT count(*) FROM observations')==[(0,)]
    assert query(h,'SELECT count(*) FROM ingest_receipts')==[(0,)]


def test_backdated_receipt_and_clock_regression_rejected(h):
    assert h.ingest(h.observation(),received=h.now-timedelta(days=1)).status=='REJECTED'
    first=h.ingest(h.observation())
    h.now-=timedelta(seconds=1)
    assert h.ingest(h.observation(record_id='new-event')).status=='REJECTED'
    assert query(h,'SELECT record_id FROM current_projection')==[(first.record_id,)]


def test_out_of_order_and_same_time_events_do_not_choose_arrival(h):
    first=h.ingest(h.observation(bars=True)); h.now+=timedelta(minutes=1);h.order=2
    older=h.observation(bars=True,start=h.now-timedelta(days=2))
    retained=h.ingest(older)
    assert retained.status=='COMMITTED' and not retained.promoted
    assert h.store.get_observation('TEST:AAA','BARS',None).record_id==first.record_id
    # Different bar day advances with verified order; historical stays retained.
    newer=h.observation(bars=True,start=h.now-timedelta(hours=10));h.order=3
    new=h.ingest(newer)
    assert new.promoted
    assert query(h,'SELECT count(*) FROM bar_revisions')==[(3,)]


@pytest.mark.parametrize('missing',['identity','lifecycle','ref','order','parent','downgrade'])
def test_ambiguous_finality_or_order_quarantines(h,missing):
    first=h.ingest(h.observation(bars=True,provisional=False));h.now+=timedelta(minutes=1)
    h.parent=first.record_id;h.order=2
    changed=h.observation(bars=True,start=h.now-timedelta(days=1)-timedelta(minutes=1),provisional=False)
    changed=change(changed,'payload.items.0.close',106.)
    if missing in ('identity','lifecycle'): h.verified=False
    elif missing=='ref': h.ref=''
    elif missing=='order': h.order=None
    elif missing=='parent': h.parent=None
    else: changed=change(changed,'payload.items.0.provisional',True)
    result=h.ingest(changed)
    assert result.status=='COMMITTED' and not result.promoted and result.reason=='AMBIGUOUS_ORDER'
    assert h.store.get_observation('TEST:AAA','BARS',None).record_id==first.record_id
    assert query(h,"SELECT count(*) FROM gaps WHERE reason='AMBIGUOUS_ORDER'")==[(1,)]


def test_provisional_to_final_requires_lineage(h):
    o=h.observation(bars=True);first=h.ingest(o)
    h.now+=timedelta(minutes=1);h.parent=first.record_id;h.order=2
    final=change(o,'payload.items.0.provisional',False)
    assert h.ingest(final).promoted


def test_provider_label_is_not_ordering(h):
    o=h.observation();first=h.ingest(o);h.now+=timedelta(minutes=1)
    h.parent=first.record_id # order remains 1 despite huge provider label
    o=change(o,'payload.last_price',101.);o=change(o,'source_revision','999999999999')
    result=h.ingest(o)
    assert result.status=='COMMITTED' and not result.promoted
    assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==first.record_id


def test_multiple_same_time_ticks_have_distinct_identity(h):
    a=h.observation();first=h.ingest(a)
    b=change(a,'record_id','upstream-event-2');h.order=2
    second=h.ingest(b)
    assert first.record_id!=second.record_id
    assert query(h,'SELECT count(*) FROM observations')==[(2,)]
    assert not second.promoted


@pytest.mark.parametrize('change',[{'price_basis':'ADJUSTED','adjustment_version':'adj-v1'},
    {'source_id':'other-source'}, {'board_id':'G2'}, {'origin_provider':'other-origin'}])
def test_series_isolation_and_ambiguous_read(h,change):
    first=h.ingest(h.observation(bars=True));h.now+=timedelta(minutes=1);h.order=2
    second=h.ingest(h.observation(bars=True,**change))
    assert first.promoted and second.promoted
    assert query(h,'SELECT count(*) FROM current_projection')==[(2,)]
    assert h.store.get_observation('TEST:AAA','BARS',None)==Unavailable('UNKNOWN')


def test_cross_series_predecessor_rejected_atomically(h):
    first=h.ingest(h.observation(bars=True));h.now+=timedelta(minutes=1)
    h.parent=first.record_id;h.order=2
    cross=h.ingest(h.observation(bars=True,price_basis='ADJUSTED',adjustment_version='v1'))
    assert cross.status=='REJECTED'
    assert query(h,'SELECT count(*) FROM series')==[(1,)]
    assert query(h,'SELECT count(*) FROM observations')==[(1,)]


def test_batched_bars_are_independent_and_atomic(h):
    o=h.observation(bars=True)
    older=o.payload.items[0].model_copy(deep=True)
    older=older.model_copy(update={'start_at':older.start_at-timedelta(days=1),'end_at':older.end_at-timedelta(days=1)})
    o.payload.items.insert(0,older)
    result=h.ingest(o)
    assert result.promoted
    assert query(h,'SELECT count(*) FROM observations')==[(2,)]
    assert query(h,'SELECT count(*) FROM receipt_records')==[(2,)]
    assert h.store.get_observation('TEST:AAA','BARS',None).payload.items[0].start_at==o.payload.items[1].start_at
    assert h.ingest(o).status=='UNCHANGED'


@pytest.mark.parametrize('stage',['ingest_begin','ingest_validated','ingest_identity','ingest_rights',
    'ingest_observation','ingest_bar','ingest_projection','ingest_receipt','ingest_audit','ingest_gaps','ingest_commit'])
def test_each_ingest_stage_failure_rolls_back(h,stage):
    original=h.observation(bars=True);first=h.ingest(original)
    before={table:query(h,f'SELECT * FROM {table}') for table in ('observations','bar_revisions','current_projection',
        'projection_history','ingest_receipts','receipt_records','selection_audit','rights_registry','gaps','series','instruments')}
    h.now+=timedelta(minutes=1);h.parent=first.record_id;h.order=2
    changed=change(original,'payload.items.0.close',106.)
    def fault(s):
        if s==stage: raise OSError('injected disk failure')
    h.hook=fault
    result=h.ingest(changed)
    assert result.status=='UNAVAILABLE'
    h.hook=lambda stage:None;h.store=h.open()
    assert {t:query(h,f'SELECT * FROM {t}') for t in before}==before
    assert h.store.integrity()['foreign_key_check']==[]
    assert h.store.get_observation('TEST:AAA','BARS',None).record_id==first.record_id


def test_second_bar_failure_rolls_back_entire_batch(h):
    o=h.observation(bars=True);second=o.payload.items[0].model_copy(deep=True)
    second=second.model_copy(update={'start_at':second.start_at-timedelta(days=1),'end_at':second.end_at-timedelta(days=1)})
    o=change(o,'payload.items',o.payload.items+[second])
    calls=[]
    def fault(stage):
        if stage=='ingest_observation':
            calls.append(stage)
            if len(calls)==2: raise OSError('second item failure')
    h.hook=fault
    assert h.ingest(o).status=='UNAVAILABLE'
    assert query(h,'SELECT count(*) FROM observations')==[(0,)]
    assert query(h,'SELECT count(*) FROM ingest_receipts')==[(0,)]


def test_immutable_history_fk_unique_and_projection_guards(h):
    first=h.ingest(h.observation())
    for statement in ['UPDATE observations SET revision=2','DELETE FROM observations',
                      'UPDATE ingest_receipts SET reason=\'overwrite\'','DELETE FROM projection_history']:
        with pytest.raises(sqlite3.IntegrityError): query(h,statement)
    with pytest.raises(sqlite3.IntegrityError): query(h,"UPDATE current_projection SET record_id='absent'")
    with pytest.raises(sqlite3.IntegrityError): query(h,'INSERT INTO observations SELECT * FROM observations')
    h.now+=timedelta(minutes=1);h.verified=False
    quarantined=h.ingest(h.observation(record_id='another-event'))
    with pytest.raises(sqlite3.IntegrityError): query(h,'UPDATE current_projection SET record_id=?',(quarantined.record_id,))
    assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==first.record_id


@pytest.mark.parametrize('bad',['price','ohlc','timestamp','basis','profile','duplicate-bars','missing-identity'])
def test_malformed_unsafe_candidates_preserve_current(h,bad):
    first=h.ingest(h.observation());h.now+=timedelta(minutes=1)
    o=h.observation(record_id='changed')
    if bad=='price':o=change(o,'payload.last_price',0.)
    elif bad=='ohlc':o=change(h.observation(bars=True),'payload.items.0.high',80.)
    elif bad=='timestamp':o=change(o,'event_at',h.now+timedelta(minutes=1))
    elif bad=='basis':o=change(o,'price_basis','ADJUSTED');o=change(o,'adjustment_version',None)
    elif bad=='profile':o=change(o,'profile','INVESTOR')
    elif bad=='duplicate-bars':o=h.observation(bars=True);o=change(o,'payload.items',o.payload.items*2)
    else:o=change(o,'record_id',None)
    assert h.ingest(o).status=='REJECTED'
    assert query(h,'SELECT count(*) FROM observations')==[(1,)]
    assert h.store.get_observation('TEST:AAA','QUOTE',None).record_id==first.record_id


def test_rights_expiry_revocation_restart_and_no_fallback(h):
    o=h.observation();h.ingest(o);cutoff=h.now
    h.now+=timedelta(days=4);h.store=h.open()
    assert h.store.get_observation('TEST:AAA','QUOTE',cutoff)==Unavailable('RIGHTS_BLOCKED')
    h.now=cutoff+timedelta(minutes=1)
    series=query(h,'SELECT series_key FROM series')[0][0]
    h.store.revoke_rights(series,'isolated-revocation')
    h.store=h.open()
    assert h.store.get_observation('TEST:AAA','QUOTE',cutoff)==Unavailable('RIGHTS_BLOCKED')
    # Polling valid rights cannot undo trusted revocation.
    h.order=2;other=change(h.observation(record_id='event-new'),'payload.last_price',101.)
    assert not h.ingest(other).promoted
    assert h.store.get_observation('TEST:AAA','QUOTE',None)==Unavailable('RIGHTS_BLOCKED')
    h.ingest(h.observation(source_id='another-series'))
    assert h.store.get_observation('TEST:AAA','QUOTE',None)==Unavailable('RIGHTS_BLOCKED')


def test_unknown_rights_never_promote(h):
    o=change(h.observation(),'rights.retained_use','UNKNOWN')
    r=h.ingest(o)
    assert r.status=='COMMITTED' and not r.promoted
    assert query(h,"SELECT reason FROM gaps")==[('RIGHTS_BLOCKED',)]


def test_fixture_store_cannot_reopen_as_investor(h):
    h.ingest(h.observation())
    with pytest.raises(MigrationError): h.open(profile='INVESTOR')


def test_investor_store_rejects_synthetic(h,tmp_path):
    store=SQLiteStore(tmp_path/'fox2-investor',instrument_registry=lambda i:True,clock=lambda:h.now)
    from fox2.ports.outcomes import IngestAudit
    assert store.append_and_promote(h.observation(profile='INVESTOR'),IngestAudit('x',h.now,'a'*64)).status=='REJECTED'


def test_safe_path_policy(tmp_path):
    with pytest.raises(StoreError):SQLiteStore('relative/fox2',instrument_registry=lambda i:True)
    with pytest.raises(StoreError):SQLiteStore(tmp_path/'legacy',instrument_registry=lambda i:True)
    with pytest.raises(StoreError):SQLiteStore(Path(__file__).resolve().parents[2]/'fox2-store',instrument_registry=lambda i:True)
    legacy=tmp_path/'Data'/'Fox'/'fox2-subdir'
    with pytest.raises(StoreError):SQLiteStore(legacy,instrument_registry=lambda i:True)
    assert not legacy.exists()
