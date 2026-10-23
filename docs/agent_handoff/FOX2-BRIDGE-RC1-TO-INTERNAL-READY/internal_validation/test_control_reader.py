import importlib.util, tempfile, sqlite3, json, contextlib
from pathlib import Path
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("reader",here/"control_reader.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# Sandbox-specific writable temporary parent; production uses user TEMP.
tempfile.tempdir=str(here)
base={"state":"STOPPED","paused":True,"setup_complete":True,"current_dispatch":None}
cases=[("safe",base,[]),("actual_paused_false",dict(base,paused=False),["paused"])]
for k,v in [("state","EXECUTING"),("paused","true"),("setup_complete",1),("current_dispatch","SECRET_DO_NOT_PRINT")]:
    cases.append(("invalid_"+k,dict(base,**{k:v}),[k]))
for k in base:
    d=base.copy();del d[k];cases.append(("missing_"+k,d,[k]))
with tempfile.TemporaryDirectory() as t:
    r=Path(t);(r/"data").mkdir();(r/"config").mkdir();(r/"config/bridge.toml").write_text("[tools]\n")
    db=r/"data/bridge.db"
    with contextlib.closing(sqlite3.connect(db)) as c:
        c.execute("CREATE TABLE worker_state(id INTEGER PRIMARY KEY,payload TEXT)")
        c.execute("INSERT INTO worker_state VALUES(1,?)",(json.dumps(base),));c.commit()
    for name,s,failed in cases:
        with contextlib.closing(sqlite3.connect(db)) as c:
            c.execute("UPDATE worker_state SET payload=?",(json.dumps(s),));c.commit()
        before=db.read_bytes();out=m.inspect(r)
        assert out["failed"]==failed,(name,out)
        assert out["safe"]==(not failed)
        assert before==db.read_bytes()
        assert "SECRET_DO_NOT_PRINT" not in json.dumps(out)
        print(name,"PASS")
    with contextlib.closing(sqlite3.connect(db)) as c:
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("UPDATE worker_state SET payload=?",(json.dumps(base),));c.commit()
        paths=[db,db.with_name("bridge.db-wal"),db.with_name("bridge.db-shm")]
        before=[q.read_bytes() for q in paths]
        assert m.inspect(r)["safe"]
        assert before==[q.read_bytes() for q in paths]
        print("active_WAL_snapshot_no_source_write PASS")
    (r/"config/bridge.toml").write_text('database_path="C:/unexpected/bridge.db"\n')
    try:
        m.inspect(r)
        raise AssertionError("redirect accepted")
    except ValueError:
        print("config_redirect_DENY PASS")
print("TOTAL 12 PASS")
