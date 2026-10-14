"""Versioned SQLite ledger for FOX2 Bridge dispatch and execution workflows."""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from .errors import DatabaseError

SCHEMA_VERSION = 4
MIGRATIONS: dict[int, tuple[str, ...]] = {
    4: (
        "ALTER TABLE executions ADD COLUMN stage TEXT NOT NULL DEFAULT 'UNKNOWN'",
        "ALTER TABLE executions ADD COLUMN checkpoint_json TEXT",
        "CREATE TABLE worker_state (id INTEGER PRIMARY KEY CHECK(id=1), payload TEXT NOT NULL)",
        "INSERT INTO worker_state VALUES (1, '{}')",
        "UPDATE bridge_meta SET value = '4' WHERE key = 'schema_version'",
    ),
    1: (
        """
        CREATE TABLE dispatches (
            dispatch_id TEXT NOT NULL UNIQUE,
            state TEXT NOT NULL,
            payload_hash TEXT,
            created_at_utc TEXT NOT NULL,
            updated_at_utc TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE executions (
            execution_id TEXT PRIMARY KEY,
            dispatch_id TEXT NOT NULL,
            state TEXT NOT NULL,
            started_at_utc TEXT,
            finished_at_utc TEXT,
            FOREIGN KEY (dispatch_id) REFERENCES dispatches(dispatch_id)
        )
        """,
        """
        CREATE TABLE review_events (
            event_id TEXT PRIMARY KEY,
            review_key TEXT NOT NULL UNIQUE,
            dispatch_id TEXT NOT NULL,
            state TEXT NOT NULL,
            created_at_utc TEXT NOT NULL,
            FOREIGN KEY (dispatch_id) REFERENCES dispatches(dispatch_id)
        )
        """,
        """
        INSERT INTO bridge_meta (key, value)
        VALUES ('schema_version', '1')
        """,
    ),
    2: (
        """
        CREATE TABLE control_cursors (
            repository TEXT NOT NULL,
            control_branch TEXT NOT NULL,
            control_commit_sha TEXT NOT NULL,
            updated_at_utc TEXT NOT NULL,
            PRIMARY KEY (repository, control_branch)
        )
        """,
        """
        CREATE TABLE poll_observations (
            observation_id TEXT PRIMARY KEY,
            repository TEXT NOT NULL,
            control_branch TEXT NOT NULL,
            previous_control_commit_sha TEXT,
            observed_remote_sha TEXT,
            status TEXT NOT NULL,
            reason TEXT,
            error TEXT,
            cursor_advanced INTEGER NOT NULL CHECK (cursor_advanced IN (0, 1)),
            observed_at_utc TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE candidate_discoveries (
            discovery_id TEXT PRIMARY KEY,
            repository TEXT NOT NULL,
            control_branch TEXT NOT NULL,
            control_commit_sha TEXT NOT NULL,
            dispatch_path TEXT NOT NULL,
            dispatch_blob_sha TEXT,
            discovery_state TEXT NOT NULL CHECK (
                discovery_state IN ('DISCOVERED', 'PATH_MODIFIED', 'PATH_DELETED')
            ),
            trust_state TEXT NOT NULL DEFAULT 'UNVALIDATED_CANDIDATE'
                CHECK (trust_state = 'UNVALIDATED_CANDIDATE'),
            observed_at_utc TEXT NOT NULL,
            UNIQUE (repository, control_branch, control_commit_sha, dispatch_path)
        )
        """,
        "CREATE INDEX candidate_discoveries_by_path "
        "ON candidate_discoveries (repository, dispatch_path, observed_at_utc)",
        """
        UPDATE bridge_meta SET value = '2' WHERE key = 'schema_version'
        """,
    ),
    3: (
        "ALTER TABLE executions ADD COLUMN result_json TEXT",
        "ALTER TABLE executions ADD COLUMN error_code TEXT",
        "ALTER TABLE executions ADD COLUMN error_message TEXT",
        "CREATE INDEX executions_by_dispatch_started "
        "ON executions (dispatch_id, started_at_utc DESC)",
        """
        UPDATE bridge_meta SET value = '3' WHERE key = 'schema_version'
        """,
    ),
}


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class SQLiteLedger:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        return connection

    def worker_state(self) -> dict[str, object]:
        with self.connect() as connection:
            return json.loads(connection.execute(
                "SELECT payload FROM worker_state WHERE id=1"
            ).fetchone()[0])

    def update_worker(self, **values: object) -> dict[str, object]:
        from .logging_config import redact_context
        with self.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            state = json.loads(connection.execute(
                "SELECT payload FROM worker_state WHERE id=1"
            ).fetchone()[0])
            state.update(redact_context(values))
            connection.execute("UPDATE worker_state SET payload=? WHERE id=1",
                               (json.dumps(state, sort_keys=True),))
        return state

    def control(self, command: str) -> dict[str, object]:
        if command not in {'status', 'pause', 'resume', 'check-now', 'request-exit'}:
            raise ValueError('unsupported fixed control command')
        with self.connect() as connection:
            connection.execute('BEGIN IMMEDIATE')
            state = json.loads(connection.execute(
                'SELECT payload FROM worker_state WHERE id=1').fetchone()[0])
            if command in {'pause', 'resume'}:
                state['paused'] = command == 'pause'
            elif command == 'check-now':
                state['check_generation'] = int(state.get('check_generation', 0)) + 1
            elif command == 'request-exit':
                state['stop_requested'] = True
            connection.execute('UPDATE worker_state SET payload=? WHERE id=1',
                               (json.dumps(state, sort_keys=True),))
        return state

    def checkpoint(self, execution_id: str, stage: str, context: dict[str, object]) -> None:
        from .logging_config import redact_context
        if stage not in {'CLAIMED', 'RUNNING', 'AGENT_EXITED', 'PUBLISHING'}:
            raise ValueError('invalid execution checkpoint')
        with self.connect() as connection:
            connection.execute('UPDATE executions SET stage=?, checkpoint_json=? WHERE execution_id=?',
                               (stage, json.dumps(redact_context(context)), execution_id))

    def pending_executions(self) -> tuple[dict[str, object], ...]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM executions WHERE state='RUNNING'").fetchall()
        return tuple(dict(row) for row in rows)

    def initialize(self) -> int:
        try:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            with self.connect() as connection:
                connection.execute("PRAGMA journal_mode = WAL")
                connection.execute("PRAGMA synchronous = FULL")
                connection.execute("BEGIN IMMEDIATE")
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS bridge_meta "
                    "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                )
                row = connection.execute(
                    "SELECT value FROM bridge_meta WHERE key = 'schema_version'"
                ).fetchone()
                current = int(row["value"]) if row else 0
                if current > SCHEMA_VERSION:
                    raise DatabaseError(
                        f"database schema {current} is newer than supported {SCHEMA_VERSION}"
                    )
                for version in range(current + 1, SCHEMA_VERSION + 1):
                    for statement in MIGRATIONS[version]:
                        connection.execute(statement)
                return SCHEMA_VERSION
        except DatabaseError:
            raise
        except (OSError, sqlite3.Error, ValueError) as exc:
            raise DatabaseError(f"cannot initialize SQLite ledger: {exc}") from exc

    def table_names(self) -> tuple[str, ...]:
        try:
            with self.connect() as connection:
                rows = connection.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
                ).fetchall()
            return tuple(row["name"] for row in rows)
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot inspect SQLite ledger: {exc}") from exc

    def get_control_cursor(self, repository: str, control_branch: str) -> str | None:
        try:
            with self.connect() as connection:
                row = connection.execute(
                    "SELECT control_commit_sha FROM control_cursors "
                    "WHERE repository = ? AND control_branch = ?",
                    (repository, control_branch),
                ).fetchone()
            return str(row["control_commit_sha"]) if row else None
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot read control cursor: {exc}") from exc

    def record_poll_success(
        self,
        *,
        repository: str,
        control_branch: str,
        previous_cursor: str | None,
        observed_remote_sha: str,
        status: str,
        candidates: Iterable[dict[str, str | None]],
        observed_at_utc: str,
        cursor_advanced: bool = True,
    ) -> tuple[int, int]:
        observation_id = str(uuid.uuid4())
        inserted = 0
        already_seen = 0
        try:
            with self.connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                for candidate in candidates:
                    discovery_id = str(uuid.uuid4())
                    cursor = connection.execute(
                        """
                        INSERT INTO candidate_discoveries (
                            discovery_id, repository, control_branch,
                            control_commit_sha, dispatch_path, dispatch_blob_sha,
                            discovery_state, trust_state, observed_at_utc
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'UNVALIDATED_CANDIDATE', ?)
                        ON CONFLICT (
                            repository, control_branch, control_commit_sha, dispatch_path
                        ) DO NOTHING
                        """,
                        (
                            discovery_id,
                            repository,
                            control_branch,
                            candidate["control_commit_sha"],
                            candidate["dispatch_path"],
                            candidate["dispatch_blob_sha"],
                            candidate["discovery_state"],
                            observed_at_utc,
                        ),
                    )
                    if cursor.rowcount == 1:
                        inserted += 1
                    else:
                        already_seen += 1

                connection.execute(
                    """
                    INSERT INTO poll_observations (
                        observation_id, repository, control_branch,
                        previous_control_commit_sha, observed_remote_sha,
                        status, reason, error, cursor_advanced, observed_at_utc
                    ) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?)
                    """,
                    (
                        observation_id,
                        repository,
                        control_branch,
                        previous_cursor,
                        observed_remote_sha,
                        status,
                        int(cursor_advanced),
                        observed_at_utc,
                    ),
                )
                if cursor_advanced:
                    connection.execute(
                        """
                        INSERT INTO control_cursors (
                            repository, control_branch, control_commit_sha, updated_at_utc
                        ) VALUES (?, ?, ?, ?)
                        ON CONFLICT(repository, control_branch) DO UPDATE SET
                            control_commit_sha = excluded.control_commit_sha,
                            updated_at_utc = excluded.updated_at_utc
                        """,
                        (repository, control_branch, observed_remote_sha, observed_at_utc),
                    )
            return inserted, already_seen
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot commit poll discovery transaction: {exc}") from exc

    def record_poll_failure(
        self,
        *,
        repository: str,
        control_branch: str,
        previous_cursor: str | None,
        observed_remote_sha: str | None,
        status: str,
        reason: str | None,
        error: str | None,
        observed_at_utc: str,
    ) -> None:
        try:
            with self.connect() as connection:
                connection.execute(
                    """
                    INSERT INTO poll_observations (
                        observation_id, repository, control_branch,
                        previous_control_commit_sha, observed_remote_sha,
                        status, reason, error, cursor_advanced, observed_at_utc
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        repository,
                        control_branch,
                        previous_cursor,
                        observed_remote_sha,
                        status,
                        reason,
                        error,
                        observed_at_utc,
                    ),
                )
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot record failed poll observation: {exc}") from exc

    def list_candidate_discoveries(
        self,
        repository: str,
        control_branch: str,
        *,
        limit: int = 200,
    ) -> tuple[dict[str, object], ...]:
        if limit < 1 or limit > 5000:
            raise DatabaseError("candidate discovery limit must be between 1 and 5000")
        try:
            with self.connect() as connection:
                rows = connection.execute(
                    """
                    SELECT repository, control_branch, control_commit_sha,
                           dispatch_path, dispatch_blob_sha, discovery_state,
                           trust_state, observed_at_utc
                    FROM candidate_discoveries
                    WHERE repository = ? AND control_branch = ?
                    ORDER BY observed_at_utc DESC, rowid DESC
                    LIMIT ?
                    """,
                    (repository, control_branch, limit),
                ).fetchall()
            return tuple(dict(row) for row in rows)
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot list candidate discoveries: {exc}") from exc

    def claim_dispatch(
        self,
        *,
        dispatch_id: str,
        payload_hash: str,
        execution_id: str,
        observed_at_utc: str,
        honor_controls: bool = False,
    ) -> bool:
        """Atomically claim a dispatch exactly once and create its execution row."""
        try:
            with self.connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                if honor_controls:
                    control = json.loads(connection.execute(
                        'SELECT payload FROM worker_state WHERE id=1').fetchone()[0])
                    if control.get('paused') or control.get('stop_requested'):
                        return False
                existing = connection.execute(
                    "SELECT payload_hash FROM dispatches WHERE dispatch_id = ?",
                    (dispatch_id,),
                ).fetchone()
                if existing is not None:
                    return False
                connection.execute(
                    """
                    INSERT INTO dispatches (
                        dispatch_id, state, payload_hash, created_at_utc, updated_at_utc
                    ) VALUES (?, 'CLAIMED', ?, ?, ?)
                    """,
                    (dispatch_id, payload_hash, observed_at_utc, observed_at_utc),
                )
                connection.execute(
                    """
                    INSERT INTO executions (
                        execution_id, dispatch_id, state, started_at_utc, finished_at_utc
                    ) VALUES (?, ?, 'RUNNING', ?, NULL)
                    """,
                    (execution_id, dispatch_id, observed_at_utc),
                )
            return True
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot claim dispatch: {exc}") from exc

    def finish_execution(
        self,
        *,
        dispatch_id: str,
        execution_id: str,
        dispatch_state: str,
        execution_state: str,
        finished_at_utc: str,
        result: dict[str, object] | None = None,
        error_code: str | None = None,
        error_message: str | None = None,
    ) -> None:
        from .logging_config import redact_context
        result_json = (
            json.dumps(redact_context(result), ensure_ascii=True, sort_keys=True)
            if result is not None
            else None
        )
        try:
            with self.connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                updated_dispatch = connection.execute(
                    """
                    UPDATE dispatches
                    SET state = ?, updated_at_utc = ?
                    WHERE dispatch_id = ?
                    """,
                    (dispatch_state, finished_at_utc, dispatch_id),
                )
                updated_execution = connection.execute(
                    """
                    UPDATE executions
                    SET state = ?, finished_at_utc = ?, result_json = ?,
                        error_code = ?, error_message = ?
                    WHERE execution_id = ? AND dispatch_id = ?
                    """,
                    (
                        execution_state,
                        finished_at_utc,
                        result_json,
                        error_code,
                        redact_context(error_message),
                        execution_id,
                        dispatch_id,
                    ),
                )
                if updated_dispatch.rowcount != 1 or updated_execution.rowcount != 1:
                    raise DatabaseError("dispatch or execution row disappeared before completion")
        except DatabaseError:
            raise
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot finish dispatch execution: {exc}") from exc

    def recover_interrupted_executions(self, *, finished_at_utc: str) -> int:
        """Compatibility entry point: conservative recovery without remote evidence.

        Caller must own the singleton. A timestamp alone proves nothing about
        Agent launch or publication; Desktop startup supplies the real verifier.
        """
        from .desktop import reconcile
        return len(reconcile(self, None))

    def dispatch_state(self, dispatch_id: str) -> dict[str, object] | None:
        try:
            with self.connect() as connection:
                row = connection.execute(
                    """
                    SELECT dispatch_id, state, payload_hash, created_at_utc, updated_at_utc
                    FROM dispatches WHERE dispatch_id = ?
                    """,
                    (dispatch_id,),
                ).fetchone()
            return dict(row) if row else None
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot read dispatch state: {exc}") from exc

    def dispatch_status(self, dispatch_id: str) -> dict[str, object] | None:
        try:
            with self.connect() as connection:
                row = connection.execute(
                    """
                    SELECT d.dispatch_id, d.state AS dispatch_state, d.payload_hash,
                           d.created_at_utc, d.updated_at_utc,
                           e.execution_id, e.state AS execution_state,
                           e.started_at_utc, e.finished_at_utc,
                           e.result_json, e.error_code, e.error_message,
                           e.stage, e.checkpoint_json
                    FROM dispatches d
                    LEFT JOIN executions e ON e.execution_id = (
                        SELECT e2.execution_id
                        FROM executions e2
                        WHERE e2.dispatch_id = d.dispatch_id
                        ORDER BY e2.started_at_utc DESC, e2.rowid DESC
                        LIMIT 1
                    )
                    WHERE d.dispatch_id = ?
                    """,
                    (dispatch_id,),
                ).fetchone()
            if row is None:
                return None
            result = dict(row)
            raw = result.pop("result_json", None)
            result["result"] = json.loads(raw) if raw else None
            checkpoint = result.pop('checkpoint_json', None)
            result['checkpoint'] = json.loads(checkpoint) if checkpoint else None
            return result
        except (sqlite3.Error, json.JSONDecodeError) as exc:
            raise DatabaseError(f"cannot read dispatch status: {exc}") from exc

    def recent_status(self, *, limit: int = 20) -> tuple[dict[str, object], ...]:
        if limit < 1 or limit > 200:
            raise DatabaseError("status limit must be between 1 and 200")
        try:
            with self.connect() as connection:
                rows = connection.execute(
                    """
                    SELECT d.dispatch_id, d.state AS dispatch_state,
                           d.created_at_utc, d.updated_at_utc,
                           e.execution_id, e.state AS execution_state,
                           e.started_at_utc, e.finished_at_utc,
                           e.error_code, e.error_message
                    FROM dispatches d
                    LEFT JOIN executions e ON e.execution_id = (
                        SELECT e2.execution_id
                        FROM executions e2
                        WHERE e2.dispatch_id = d.dispatch_id
                        ORDER BY e2.started_at_utc DESC, e2.rowid DESC
                        LIMIT 1
                    )
                    ORDER BY d.updated_at_utc DESC, d.rowid DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
            return tuple(dict(row) for row in rows)
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot list dispatch status: {exc}") from exc
