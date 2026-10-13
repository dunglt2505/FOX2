"""Versioned SQLite ledger for future dispatch and execution workflows."""

from __future__ import annotations

import sqlite3
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from .errors import DatabaseError

SCHEMA_VERSION = 2
MIGRATIONS: dict[int, tuple[str, ...]] = {
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
    ) -> tuple[dict[str, object], ...]:
        try:
            with self.connect() as connection:
                rows = connection.execute(
                    """
                    SELECT repository, control_branch, control_commit_sha,
                           dispatch_path, dispatch_blob_sha, discovery_state,
                           trust_state, observed_at_utc
                    FROM candidate_discoveries
                    WHERE repository = ? AND control_branch = ?
                    ORDER BY control_commit_sha, dispatch_path
                    """,
                    (repository, control_branch),
                ).fetchall()
            return tuple(dict(row) for row in rows)
        except sqlite3.Error as exc:
            raise DatabaseError(f"cannot list candidate discoveries: {exc}") from exc
