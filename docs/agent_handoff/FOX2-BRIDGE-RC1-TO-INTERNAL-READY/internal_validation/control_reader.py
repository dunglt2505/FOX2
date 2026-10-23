import json, sqlite3, sys, tempfile, tomllib
from contextlib import closing
from pathlib import Path

FIELDS = ("state", "paused", "setup_complete", "current_dispatch")
STATES = {"STOPPED", "PAUSED", "IDLE", "STARTING", "RECONCILING", "POLLING",
          "EXECUTING", "PUBLISHING", "STOPPING", "ERROR", "DEGRADED"}

def inspect(root):
    root = Path(root).resolve()
    config = root / "config/bridge.toml"
    db = root / "data/bridge.db"
    wal = db.with_name(db.name + "-wal")
    journal = db.with_name(db.name + "-journal")
    def capture():
        return (config.read_bytes(), db.read_bytes(),
                wal.read_bytes() if wal.exists() else None,
                journal.read_bytes() if journal.exists() else None)
    before = capture()
    cfg = tomllib.loads(before[0].decode("utf-8"))
    if (Path(cfg.get("bridge_root", root)).resolve() != root or
            Path(cfg.get("database_path", db)).resolve() != db):
        raise ValueError("CONFIG_TARGET_MISMATCH")
    if before[3]:
        raise ValueError("ROLLBACK_JOURNAL_PRESENT")
    # No Bridge import, live SQLite connection, checkpoint, or host state write.
    # Only a private temporary copy is opened by SQLite; it is removed on exit.
    with tempfile.TemporaryDirectory(prefix="FOX2-control-read-") as folder:
        copy = Path(folder) / "bridge.db"
        copy.write_bytes(before[1])
        if before[2] is not None:
            copy.with_name("bridge.db-wal").write_bytes(before[2])
        with closing(sqlite3.connect(str(copy), timeout=3)) as conn:
            conn.execute("PRAGMA query_only=ON")
            if conn.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
                raise ValueError("COPY_INTEGRITY_FAILED")
            row = conn.execute("SELECT payload FROM worker_state WHERE id=1").fetchone()
            if row is None:
                raise ValueError("WORKER_ROW_MISSING")
            state = json.loads(row[0])
    if before != capture():
        raise ValueError("SOURCE_CHANGED")
    if not isinstance(state, dict):
        raise ValueError("WORKER_OBJECT_INVALID")
    checks = {
        "state": type(state.get("state")) is str and state["state"] == "STOPPED",
        "paused": state.get("paused") is True,
        "setup_complete": state.get("setup_complete") is True,
        "current_dispatch": "current_dispatch" in state and state["current_dispatch"] is None,
    }
    public = {}
    for key in FIELDS:
        value = state.get(key)
        if key not in state:
            value = "MISSING"
        elif key == "state":
            value = value if type(value) is str and value in STATES else "INVALID_OR_REDACTED"
        elif key in ("paused", "setup_complete"):
            value = value if type(value) is bool else "INVALID_TYPE"
        else:
            value = "NULL" if value is None else "PRESENT_REDACTED"
        public[key] = {"present": key in state, "value": value, "pass": checks[key]}
    return {"schema": "FOX2_CONTROL_READONLY_V1", "snapshot_stable": True,
            "fields": public, "safe": all(checks.values()),
            "failed": [key for key in FIELDS if not checks[key]]}

if __name__ == "__main__":
    try:
        result = inspect(sys.argv[1])
    except Exception:
        print('{"schema":"FOX2_CONTROL_READONLY_V1","safe":false,"probe_error":"READ_FAILED_RECONCILE"}')
        sys.exit(2)
    print(json.dumps(result, sort_keys=True))
