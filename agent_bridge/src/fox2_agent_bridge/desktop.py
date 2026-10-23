"""Durable per-user worker and fixed local controls; no network IPC."""
from __future__ import annotations

import json
import os
import time
import uuid
import threading
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Callable

from .config import BridgeConfig
from .e2e_runner import BridgeE2ERunner
from .ledger import SQLiteLedger, utc_now
from .logging_config import configure_logging, redact_context
from .ops_runner import BridgeOps
from .process_lock import ProcessLock
from .runtime_tools import discover_all
from .paths import BRIDGE_ROOT
from .agent_policy import configuration_mismatch

STATES = frozenset({'STOPPED', 'STARTING', 'RECONCILING', 'IDLE', 'POLLING',
                    'EXECUTING', 'PUBLISHING', 'PAUSED', 'DEGRADED', 'ERROR', 'STOPPING'})
BACKOFF = (30, 60, 120, 300)
LEGACY_ROOT = Path(r'C:\Projects\FOX2-AgentBridge')


def initialize_runtime(config: BridgeConfig) -> SQLiteLedger:
    ledger = SQLiteLedger(config.database_path)
    legacy_root = LEGACY_ROOT
    legacy_db = legacy_root / 'data' / 'bridge.db'
    cross_root = config.bridge_root == BRIDGE_ROOT.resolve()
    if cross_root and not config.database_path.exists() and legacy_db.exists():
        # Carry forward all consumed identities before the first per-user poll.
        # Never snapshot while an old supervisor can still claim/execute.
        with ProcessLock(config.bridge_root / 'data' / 'bootstrap.lock'):
            if not config.database_path.exists():
                with ProcessLock(legacy_root / 'data' / 'bridge.lock'):
                    config.database_path.parent.mkdir(parents=True, exist_ok=True)
                    temporary = config.database_path.with_suffix('.migration')
                    with closing(sqlite3.connect(legacy_db.as_uri() + '?mode=ro', uri=True)) as source:
                        with closing(sqlite3.connect(temporary)) as destination:
                            source.backup(destination)
                            # Publish only a denied snapshot, even if the source
                            # was written by a newer single-root fixture ledger.
                            with destination:
                                destination.execute(
                                    "INSERT OR REPLACE INTO bridge_meta (key, value) "
                                    "VALUES ('claim_authority', 'DENY_CROSS_ROOT_UNKNOWN')"
                                )
                    temporary.replace(config.database_path)
    # Every configured runtime root shares the FOX2 dispatch namespace. Moving
    # it via --config is not evidence of old-writer retirement. F0 has no
    # positive runtime admission; unrelated direct single-DB fixtures remain
    # supported by SQLiteLedger.initialize(). Keep legacy snapshot discovery
    # restricted to the canonical root above.
    ledger.initialize(cross_root_authority_unknown=True)
    manual = config.bridge_root / 'data' / 'manual_consumption.json'
    if manual.exists():
        receipt = json.loads(manual.read_text(encoding='utf-8'))
        if receipt.get('format') != 'FOX2_MANUAL_CONSUMPTION_1':
            raise ValueError('invalid manual consumption receipt')
        identities = receipt.get('dispatch_ids')
        import re
        if (not isinstance(identities, list) or not identities or
                any(not isinstance(i, str) or not re.fullmatch(r'FOX2-[A-Za-z0-9._-]+', i) for i in identities)):
            raise ValueError('invalid consumed dispatch identities')
        with ledger.connect() as connection:
            connection.execute('BEGIN IMMEDIATE')
            now = utc_now()
            for identity in identities:
                connection.execute('INSERT OR IGNORE INTO dispatches '
                    '(dispatch_id,state,payload_hash,created_at_utc,updated_at_utc) '
                    'VALUES (?, ?, NULL, ?, ?)', (identity, 'NEEDS_RECONCILIATION', now, now))
    return ledger


def reconcile(ledger: SQLiteLedger, runner: BridgeE2ERunner | None) -> list[dict[str, object]]:
    outcomes = []
    for row in ledger.pending_executions():
        context = json.loads(row['checkpoint_json'] or '{}')
        state = 'NEEDS_RECONCILIATION'
        result = None
        if row['stage'] == 'CLAIMED':
            # Durable launch intent is written before spawning. Preserve the claim;
            # elapsed time never grants a replay and max_runs=1 remains enforced.
            state = 'SAFE_NOT_STARTED'
        elif (row['stage'] in {'AGENT_EXITED', 'PUBLISHING'} and context.get('agent_exit_code') == 0
              and not (context.get('agent_metadata') and (
                  context['agent_metadata'].get('post_start_failure') or
                  configuration_mismatch(context['agent_metadata'])))):
            try:
                if runner is None:
                    raise ValueError('remote verifier unavailable')
                payload = context['payload']
                owner = payload.get('delivery_owner')
                if owner == 'BRIDGE':
                    # A BRIDGE-owned Agent must NEVER be able to impersonate
                    # publication with its own Git commit/push. The durable
                    # exact SHA can only come from Bridge's PUBLISHING intent.
                    if row['stage'] != 'PUBLISHING' or not context.get('expected_result_sha'):
                        raise ValueError('Bridge publication has no durable commit identity')
                    head, paths = runner._reconcile_publishing(context)
                elif owner == 'AGENT':
                    head, paths = runner._verify_result(
                        payload=payload, worktree=Path(str(payload['worktree'])),
                        before_head=str(context['before_head']),
                        agent_stdout=str(context['agent_stdout']),
                        agent_label=str(payload['_agent_product']))
                else:
                    raise ValueError('unknown immutable delivery owner')
                if context.get('expected_result_sha') and head != context['expected_result_sha']:
                    raise ValueError('remote result does not match durable publish identity')
                result = {'after_head': head, 'changed_paths': list(paths),
                          'recovered': True, 'requested_agent': payload['agent'],
                          'agent_metadata': context.get('agent_metadata')}
                state = 'PUSHED_UNREVIEWED'
            except Exception:
                # Offline contact, dirty workspaces and unverified results require
                # human reconciliation; never publish or invoke an Agent here.
                pass
        ledger.finish_execution(
            dispatch_id=str(row['dispatch_id']), execution_id=str(row['execution_id']),
            dispatch_state=state, execution_state=state, finished_at_utc=utc_now(),
            result=result, error_code=None if result else state,
            error_message=None if result else 'No automatic replay; retained immutable claim')
        outcomes.append({'dispatch_id': row['dispatch_id'], 'outcome': state,
                         'remote_result_sha': result['after_head'] if result else None})
    return outcomes


class DesktopWorker:
    def __init__(self, config: BridgeConfig, *, ops=None, runner=None,
                 monotonic: Callable[[], float] = time.monotonic,
                 sleep: Callable[[float], None] = time.sleep) -> None:
        self.config = config
        self.ledger = SQLiteLedger(config.database_path)
        # Share the Operational lock so one-shot runners and Worker cannot compete.
        self.lock = ProcessLock(config.bridge_root / 'data' / 'bridge.lock')
        self.ops = ops
        self.runner = runner
        self.clock, self.sleep = monotonic, sleep
        self.failures = 0
        self.due = 0.0
        self.check_seen = 0

    def state(self, value: str, **fields: object) -> None:
        if value not in STATES:
            raise ValueError('invalid worker state')
        self.ledger.update_worker(state=value, heartbeat=utc_now(), **fields)

    def progress(self, message: str) -> None:
        if message.startswith('OPS poll complete:') and 'POLL_FAILED' not in message:
            self.failures = 0
        if message.startswith('OPS selected '):
            self.state('EXECUTING', current_dispatch=message.removeprefix('OPS selected '))
        elif 'verifies, commits' in message or 'verify pushed result' in message:
            self.state('PUBLISHING')
        else:
            self.ledger.update_worker(heartbeat=utc_now())

    def tick(self) -> bool:
        control = self.ledger.worker_state()
        if control.get('stop_requested'):
            return False
        self.ledger.update_worker(heartbeat=utc_now())
        if control.get('paused'):
            self.state('PAUSED')
            return True
        generation = int(control.get('check_generation', 0))
        if self.clock() < self.due and generation == self.check_seen:
            return True
        self.check_seen = generation
        self.state('POLLING', check_consumed=generation, last_poll=utc_now())
        try:
            result = self.ops.run_next()
            if result.status == 'POLL_BLOCKED':
                raise ConnectionError('control poll blocked')
            self.failures = 0
            delay = self.config.poll_interval_seconds
            self.state('IDLE', last_result=result.as_dict(), current_dispatch=None,
                       backoff_seconds=delay, last_error=None)
        except Exception as exc:
            delay = BACKOFF[min(self.failures, len(BACKOFF)-1)]
            self.failures += 1
            self.state('DEGRADED', last_error=redact_context(str(exc)),
                       current_dispatch=None, backoff_seconds=delay)
        self.due = self.clock() + delay
        return True

    def run(self) -> None:
        self.lock.acquire()
        failed = False
        heartbeat_stop = threading.Event()
        heartbeat_thread = None
        try:
            self.ledger = initialize_runtime(self.config)
            from .f1_client import inspect_authority
            self.ledger.update_worker(f1_authority=inspect_authority())
            self.state('STARTING', generation=str(uuid.uuid4()), started=utc_now(),
                       stopped=None, stop_requested=False)
            self.state('RECONCILING')
            def pulse():
                while not heartbeat_stop.wait(5):
                    self.ledger.update_worker(heartbeat=utc_now())
            heartbeat_thread = threading.Thread(target=pulse, daemon=True)
            heartbeat_thread.start()
            logger = configure_logging(self.config.log_directory)
            runner = self.runner or BridgeE2ERunner(self.config, self.ledger, logger=logger)
            outcomes = reconcile(self.ledger, runner)
            tools = [tool.as_dict() for tool in discover_all(self.config)]
            self.ledger.update_worker(reconciliation=outcomes, tools=tools)
            self.ops = self.ops or BridgeOps(self.config, self.ledger, logger=logger,
                                            progress=self.progress)
            # Recheck control inside Ops immediately before claiming, including a
            # pause/exit arriving while Git discovery was in progress.
            self.ops.can_claim = lambda: not any(self.ledger.worker_state().get(key)
                                                 for key in ('paused', 'stop_requested'))
            self.state('IDLE')
            while self.tick():
                self.sleep(0.5)
            self.state('STOPPING')
        except KeyboardInterrupt:
            self.state('STOPPING')
        except BaseException as exc:
            failed = True
            self.state('ERROR', last_error=redact_context(str(exc)))
            raise
        finally:
            heartbeat_stop.set()
            if heartbeat_thread:
                heartbeat_thread.join(timeout=10)
            try:
                self.state('ERROR' if failed else 'STOPPED', stopped=utc_now())
            finally:
                self.lock.release()


def control(config: BridgeConfig, command: str) -> dict[str, object]:
    ledger = initialize_runtime(config)
    if command == 'open-logs':
        config.log_directory.mkdir(parents=True, exist_ok=True)
        os.startfile(config.log_directory)
        return {'log_directory': str(config.log_directory)}
    return ledger.control(command)
