"""Ordered SQLite migrations. No executescript implicit commits or repair."""
import hashlib
import sqlite3

APPLICATION_ID = 0x46583232
VERSION = 1

STATEMENTS = (
    'CREATE TABLE schema_migrations(version INTEGER PRIMARY KEY CHECK(version>0), checksum TEXT NOT NULL)',
    'CREATE TABLE store_metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL)',
    'CREATE TABLE instruments(instrument_id TEXT PRIMARY KEY CHECK(length(instrument_id)>0))',
    '''CREATE TABLE series(series_key TEXT PRIMARY KEY, instrument_id TEXT NOT NULL REFERENCES instruments,
       capability TEXT NOT NULL CHECK(capability IN ('QUOTE','BARS','INDEX')), identity_json TEXT NOT NULL)''',
    '''CREATE TABLE observations(record_id TEXT PRIMARY KEY, series_key TEXT NOT NULL REFERENCES series,
       logical_key TEXT NOT NULL, fingerprint TEXT NOT NULL, revision INTEGER NOT NULL CHECK(revision>0),
       first_available_at TEXT NOT NULL, market_at TEXT NOT NULL, source_order INTEGER,
       predecessor_record_id TEXT REFERENCES observations(record_id), eligible INTEGER NOT NULL CHECK(eligible IN (0,1)),
       payload_json TEXT NOT NULL, original_json TEXT NOT NULL, evidence_json TEXT NOT NULL,
       UNIQUE(series_key,logical_key,fingerprint), UNIQUE(series_key,logical_key,revision), UNIQUE(record_id,series_key))''',
    '''CREATE TABLE bar_revisions(record_id TEXT PRIMARY KEY REFERENCES observations(record_id),
       start_at TEXT NOT NULL, provisional INTEGER CHECK(provisional IN (0,1)))''',
    '''CREATE TABLE current_projection(series_key TEXT PRIMARY KEY REFERENCES series,
       record_id TEXT NOT NULL, FOREIGN KEY(record_id,series_key) REFERENCES observations(record_id,series_key))''',
    '''CREATE TABLE projection_history(promotion_id INTEGER PRIMARY KEY, series_key TEXT NOT NULL REFERENCES series,
       record_id TEXT NOT NULL, promoted_at TEXT NOT NULL,
       FOREIGN KEY(record_id,series_key) REFERENCES observations(record_id,series_key))''',
    '''CREATE TABLE ingest_receipts(audit_id TEXT PRIMARY KEY, received_at TEXT NOT NULL, raw_sha256 TEXT NOT NULL,
       candidate_sha256 TEXT NOT NULL, status TEXT NOT NULL, reason TEXT NOT NULL, result_json TEXT NOT NULL,
       original_json TEXT NOT NULL)''',
    '''CREATE TABLE receipt_records(audit_id TEXT NOT NULL REFERENCES ingest_receipts(audit_id),
       record_id TEXT NOT NULL REFERENCES observations(record_id), PRIMARY KEY(audit_id,record_id))''',
    '''CREATE TABLE gaps(gap_id INTEGER PRIMARY KEY, audit_id TEXT NOT NULL REFERENCES ingest_receipts(audit_id),
       record_id TEXT REFERENCES observations(record_id), reason TEXT NOT NULL, detail_json TEXT NOT NULL)''',
    '''CREATE TABLE selection_audit(selection_id INTEGER PRIMARY KEY,
       audit_id TEXT NOT NULL REFERENCES ingest_receipts(audit_id), record_id TEXT NOT NULL REFERENCES observations(record_id),
       promoted INTEGER NOT NULL CHECK(promoted IN (0,1)), reason TEXT NOT NULL)''',
    '''CREATE TABLE rights_registry(rights_id INTEGER PRIMARY KEY, series_key TEXT NOT NULL REFERENCES series,
       read_state TEXT NOT NULL, retained_state TEXT NOT NULL, evidence_ref TEXT,
       verified_until TEXT, observed_at TEXT NOT NULL, revoked INTEGER NOT NULL CHECK(revoked IN (0,1)))''',
    '''CREATE TABLE watchlist_preferences(singleton INTEGER PRIMARY KEY CHECK(singleton=1),
       version INTEGER NOT NULL CHECK(version>=0), items_json TEXT NOT NULL, updated_at TEXT)''',
    "INSERT INTO watchlist_preferences VALUES(1,0,'[]',NULL)",
    'CREATE INDEX observation_availability ON observations(series_key,first_available_at)',
    'CREATE INDEX history_cutoff ON projection_history(series_key,promoted_at,promotion_id)',
    'CREATE INDEX rights_series ON rights_registry(series_key,rights_id)',
)
IMMUTABLE = ('observations', 'bar_revisions', 'projection_history', 'ingest_receipts',
             'receipt_records', 'gaps', 'selection_audit', 'rights_registry', 'series', 'instruments', 'store_metadata')
STATEMENTS += tuple(
    f"CREATE TRIGGER immutable_{table}_{action.lower()} BEFORE {action} ON {table} "
    "BEGIN SELECT RAISE(ABORT,'immutable history'); END"
    for table in IMMUTABLE for action in ('UPDATE', 'DELETE')
)
# Prevent promotion of quarantine even through direct SQL.
STATEMENTS += tuple(
    f'''CREATE TRIGGER projection_eligible_{action.lower()} BEFORE {action} ON current_projection
        WHEN NOT EXISTS(SELECT 1 FROM observations WHERE record_id=NEW.record_id
        AND series_key=NEW.series_key AND eligible=1)
        BEGIN SELECT RAISE(ABORT,'ineligible projection'); END'''
    for action in ('INSERT', 'UPDATE')
)
CHECKSUM = hashlib.sha256('\n'.join(STATEMENTS).encode()).hexdigest()


class MigrationError(ValueError):
    """Sanitized refusal; caller must never repair unknown data automatically."""


def migrate(connection: sqlite3.Connection, profile: str, hook=lambda stage: None):
    connection.execute('BEGIN IMMEDIATE')
    try:
        app_id = connection.execute('PRAGMA application_id').fetchone()[0]
        version = connection.execute('PRAGMA user_version').fetchone()[0]
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        if app_id == 0 and version == 0 and not tables:
            hook('migration_before')
            for number, statement in enumerate(STATEMENTS):
                connection.execute(statement)
                hook(f'migration_statement_{number}')
            connection.execute('INSERT INTO schema_migrations VALUES(?,?)', (VERSION, CHECKSUM))
            connection.execute('INSERT INTO store_metadata VALUES(?,?)', ('profile', profile))
            connection.execute(f'PRAGMA application_id={APPLICATION_ID}')
            connection.execute(f'PRAGMA user_version={VERSION}')
            hook('migration_after')
        else:
            if app_id != APPLICATION_ID or version != VERSION:
                raise MigrationError('INCOMPATIBLE_STORE')
            if connection.execute('SELECT version,checksum FROM schema_migrations ORDER BY version').fetchall() != [(VERSION, CHECKSUM)]:
                raise MigrationError('MIGRATION_HISTORY_MISMATCH')
            if connection.execute("SELECT value FROM store_metadata WHERE key='profile'").fetchone() != (profile,):
                raise MigrationError('PROFILE_MISMATCH')
            # Detect dropped/altered schema objects, not just changed metadata.
            expected = sqlite3.connect(':memory:')
            try:
                for statement in STATEMENTS:
                    expected.execute(statement)
                query = "SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name"
                if connection.execute(query).fetchall() != expected.execute(query).fetchall():
                    raise MigrationError('SCHEMA_MISMATCH')
            finally:
                expected.close()
        if connection.execute('PRAGMA foreign_key_check').fetchall():
            raise MigrationError('FOREIGN_KEY_FAILURE')
        hook('migration_commit')
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
