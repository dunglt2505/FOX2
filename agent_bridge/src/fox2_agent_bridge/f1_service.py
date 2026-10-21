"""SCM entry point for the protected LocalSystem execution authority.

G2 ships source only. This module never registers/starts a service or applies
policy. G3/G4 must independently seal the runtime, complete reconciliation and
place a reviewed adoption plan/state in the protected ProgramData root.
"""
from __future__ import annotations

import ctypes as C
from ctypes import wintypes as W
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import threading
import time
from contextlib import closing

from .f1_authority import ApprovedTask, Authority
from .f1_broker_store import BrokerEpoch, F1BrokerStore
from .f1_policy import effective_policy_digest, f1_control_digest
from .f1_protocol import AuthorityDeny, Request, SERVICE_NAME, deny
from .f1_reconcile import reconcile_consumed
from .f1_windows import Win32, WindowsSpawner, HANDLE, DWORD, PTR, BOOL


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class HostFence:
    def __init__(self, api: Win32, root: Path, plan: dict, plan_digest: str):
        self.api, self.root, self.plan, self.plan_digest = api, root, plan, plan_digest

    def sealed_file(self, path: Path, digest: str):
        if not path.is_absolute() or not re.fullmatch('[0-9a-f]{64}', digest):
            raise AuthorityDeny('SEALED_FILE_IDENTITY')
        self.api.protected(path)
        # Ancestors must not allow rename/delete/replacement by a requester.
        for parent in path.parents:
            self.api.protected(parent, ancestor=True)
        if sha(path) != digest:
            raise AuthorityDeny('SEALED_FILE_DRIFT')

    def __call__(self, task: ApprovedTask | None):
        api, plan = self.api, self.plan
        api.require_system()
        api.protected(self.root, root=True)
        if api.service_pid() != os.getpid():
            raise AuthorityDeny('SERVICE_DRIFT')
        executable = self.root / 'runtime/Scripts/python.exe'
        binary, account, kind, start = api.service_config()
        expected_binary = '"' + str(executable) + '" -I -B -m fox2_agent_bridge.f1_service --scm'
        if (binary != expected_binary or account != 'LocalSystem' or kind != 0x10
                or start != plan['service_start_type']
                or Path(sys.executable).resolve() != executable.resolve()):
            raise AuthorityDeny('SERVICE_CONFIG_DRIFT')
        self.sealed_file(self.root / 'adoption.json', self.plan_digest)
        if plan.get('adoption') != 'G3_G4_VERIFIED':
            raise AuthorityDeny('HOST_ADOPTION_NOT_VERIFIED')
        inventory = plan['runtime_bindings']
        # G3 must seal the complete runtime, not merely its Python launcher.
        runtime = self.root / 'runtime'
        for path in runtime.rglob('*'):
            api.protected(path)
            if path.is_file() and str(path) not in inventory:
                raise AuthorityDeny('RUNTIME_INVENTORY_INCOMPLETE')
        if str(Path(__file__).resolve()) not in inventory or str(executable) not in inventory:
            raise AuthorityDeny('SERVICE_MODULE_UNBOUND')
        for name, digest in plan['runtime_bindings'].items():
            self.sealed_file(Path(name), digest)
        api.protected(self.root / 'broker.sqlite')
        # AppIDSvc status comes from SCM. Effective XML comes from the OS, not
        # the request/plan's assertion that enforcement is running.
        api.service_pid('AppIDSvc')
        system = C.create_unicode_buffer(32768)
        api.check(api.k.GetSystemDirectoryW(system, len(system)))
        powershell = Path(system.value) / 'WindowsPowerShell/v1.0/powershell.exe'
        result = subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-Command',
            "$ErrorActionPreference='Stop'; Import-Module ($PSHOME + '/Modules/AppLocker/AppLocker.psd1'); "
            'Get-AppLockerPolicy -Effective -Xml'], capture_output=True, text=True, timeout=10,
            env={'SystemRoot': str(Path(system.value).parent), 'WINDIR': str(Path(system.value).parent)},
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        try:
            if (result.returncode or effective_policy_digest(result.stdout.strip()) !=
                    plan['effective_policy_digest']):
                raise AuthorityDeny('EFFECTIVE_POLICY_BINDING')
            if f1_control_digest(result.stdout.strip(), plan['f1_rule_ids']) != plan['f1_control_digest']:
                raise AuthorityDeny('F1_CONTROL_BINDING')
        except AuthorityDeny:
            raise
        except (ValueError, KeyError, TypeError) as exc:
            # A legacy single-digest plan, malformed selector/XML or missing
            # control is a denial, never a compatibility fallback.
            raise AuthorityDeny('POLICY_CONTRACT') from exc
        if task is None:
            return
        if not task.argv or not Path(task.argv[0]).is_absolute() or Path(task.argv[0]).suffix.lower() != '.exe':
            raise AuthorityDeny('AGENT_EXECUTABLE')
        if task.argv[0] not in dict(task.bindings):
            raise AuthorityDeny('UNBOUND_EXECUTABLE')
        for path, digest in task.bindings:
            self.sealed_file(Path(path), digest)
        # PAUSE/STOP is additive user control, never positive host authority.
        db = Path(task.controls_db)
        if not db.is_file() or db.is_symlink() or db.is_junction():
            raise AuthorityDeny('CONTROLS_MISSING')
        with closing(sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)) as con:
            row = con.execute('SELECT payload FROM worker_state WHERE id=1').fetchone()
        control = json.loads(row[0]) if row else None
        if (not isinstance(control, dict) or type(control.get('paused')) is not bool
                or type(control.get('stop_requested')) is not bool
                or control['paused'] or control['stop_requested']):
            raise AuthorityDeny('PAUSED_OR_STOPPED')
        git = plan['git_executable']
        if git not in plan['runtime_bindings']:
            raise AuthorityDeny('UNBOUND_GIT')
        for arguments, expected in ((['rev-parse', 'HEAD'], plan['source_commit']),
                (['branch', '--show-current'], plan['tasks'][task.request.dispatch_id]['branch']),
                (['status', '--porcelain'], '')):
            result = subprocess.run([git, '-C', task.worktree, *arguments],
                capture_output=True, text=True, timeout=10,
                env={'SystemRoot': str(Path(system.value).parent), 'GIT_CONFIG_NOSYSTEM': '1',
                     'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_OPTIONAL_LOCKS': '0'},
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if result.returncode or result.stdout.strip() != expected:
                raise AuthorityDeny('SOURCE_WORKTREE_DRIFT')


def load_authority(api: Win32) -> tuple[Authority, dict]:
    api.require_system()
    root = api.authority_root()
    api.protected(root, root=True)
    path = root / 'adoption.json'
    api.protected(path)
    raw = path.read_bytes()
    plan = json.loads(raw)
    # No bootstrap/create/auto-adoption on service start. A missing store is HOLD.
    database = root / 'broker.sqlite'
    if not database.is_file():
        raise AuthorityDeny('RECONCILED_STORE_MISSING')
    api.protected(database)
    store = F1BrokerStore(database)
    # Read existing schema; initialize is confined to separately privileged G3.
    with closing(store._db()) as con:
        if con.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
            raise AuthorityDeny('STORE_CORRUPT')
    fence = HostFence(api, root, plan, hashlib.sha256(raw).hexdigest())
    authority = Authority(store, fence=fence, spawner=WindowsSpawner(api))
    authority.start(BrokerEpoch(1, plan['effective_policy_digest'], plan['source_commit'],
                                plan['package_digest'], plan['expires_at']),
                    adoption_digest=hashlib.sha256(raw).hexdigest())
    try:
        fence(None)
        snapshot = reconcile_consumed(tuple(Path(p) for p in plan['historical_roots']),
            manual_consumed=tuple(plan['manual_consumed']), inventory_complete=plan['inventory_complete'])
        if (snapshot.inventory_sha256 != plan['inventory_sha256']
                or not set(snapshot.consumed_ids) <= set(store.consumed_ids())):
            raise AuthorityDeny('RECONCILIATION_BINDING')
        tasks = []
        for dispatch_id, value in plan['tasks'].items():
            request = Request.parse({**value['request'], 'epoch': authority.epoch})
            if request.dispatch_id != dispatch_id or request.package_digest != plan['package_digest']:
                raise AuthorityDeny('PLAN_IDENTITY')
            bindings = tuple(sorted(value['bindings'].items()))
            digest = hashlib.sha256(json.dumps(dict(bindings), sort_keys=True,
                                                separators=(',', ':')).encode()).hexdigest()
            if (request.source_digest != digest
                    or dict(bindings).get(value['task_path']) != request.immutable_task_sha
                    or dict(bindings).get(plan['package_path']) != request.package_digest
                    or not re.fullmatch('[0-9a-f]{64}', value['dispatch_digest'])
                    or not value['branch'].startswith('work/')):
                raise AuthorityDeny('PLAN_SOURCE_PACKAGE')
            tasks.append(ApprovedTask(request, value['caller_sid'], value['caller_session'],
                min(value['expires_at'], plan['expires_at']), tuple(value['argv']),
                value['worktree'], bindings, value['controls_db']))
        authority.stage(tuple(tasks))
        return authority, plan
    except BaseException:
        authority.revoke()
        raise


def route(authority: Authority, plan: dict, message: object, peer) -> dict:
    if not isinstance(message, dict) or set(message) != {'operation', 'request'}:
        return deny('MESSAGE_SHAPE')
    operation, request = message['operation'], message['request']
    if operation == 'inspect_authority':
        result = authority.inspect()
        # The descriptor is public binding material, never a spawn capability.
        if isinstance(request, dict) and set(request) == {'dispatch_id', 'dispatch_digest'}:
            task = authority.tasks.get(request['dispatch_id'])
            if (task and peer.sid == task.caller_sid and peer.session == task.caller_session
                    and request['dispatch_digest'] == plan['tasks'][request['dispatch_id']]['dispatch_digest']):
                result['request'] = asdict(task.request)
        return result
    if operation == 'claim_and_spawn':
        return authority.claim_and_spawn(request, peer)
    if operation == 'revoke' and peer.administrator:
        authority.revoke()
        return deny('AUTHORITY_REVOKED')
    if operation == 'report_outcome' and isinstance(request, dict) and set(request) == {'dispatch_id', 'outcome'}:
        return authority.report_outcome(request['dispatch_id'], request['outcome'], peer)
    # Stage/reconciliation is not exposed over the interactive IPC endpoint.
    return deny('PRIVILEGED_OR_UNKNOWN_OPERATION')


def serve(api: Win32, stop: threading.Event):
    with api.singleton():
        authority, plan = load_authority(api)
        try:
            # One pipe instance for the entire service lifetime; never release
            # first-instance ownership between clients.
            with api.pipe() as pipe:
                while not stop.is_set():
                    connected = api.k.ConnectNamedPipe(pipe, None)
                    error = C.get_last_error()
                    if connected or error == 536:  # NOWAIT: now listening, no peer yet
                        authority.monitor(); stop.wait(0.05); continue
                    if error != 535:  # only ERROR_PIPE_CONNECTED establishes a peer
                        if error == 232:
                            api.k.DisconnectNamedPipe(pipe)
                            continue
                        raise AuthorityDeny('PIPE_CONNECT')
                    deadline = time.monotonic() + 5
                    try:
                        raw = None
                        while raw is None and not stop.is_set() and time.monotonic() < deadline:
                            raw = api.receive(pipe)
                            if raw is None:
                                authority.monitor(); stop.wait(0.01)
                        if raw is not None:
                            with api.peer(pipe) as peer:
                                answer = route(authority, plan, json.loads(raw), peer)
                                api.send(pipe, json.dumps(answer, separators=(',', ':')).encode())
                            # Bounded read acknowledgement avoids discarding an
                            # unread reply at DisconnectNamedPipe, without an
                            # unbounded FlushFileBuffers on an untrusted client.
                            deadline = time.monotonic() + 5
                            while not stop.is_set() and time.monotonic() < deadline:
                                if api.receive(pipe) is not None:
                                    break
                                authority.monitor(); stop.wait(0.01)
                    except (AuthorityDeny, ValueError, TypeError, KeyError):
                        # Malformed peers never create authority or escape the loop.
                        pass
                    finally:
                        api.k.DisconnectNamedPipe(pipe)
                    authority.monitor()
        finally:
            authority.revoke()


def main():
    if sys.argv[1:] != ['--scm']:
        raise SystemExit('SCM-only entry point; no install/start/policy command')
    api = Win32(); api.require_system()
    callback = C.WINFUNCTYPE(None, DWORD, PTR)
    handler_type = C.WINFUNCTYPE(DWORD, DWORD, DWORD, PTR, PTR)

    class Status(C.Structure):
        _fields_ = [(n, DWORD) for n in ('type', 'state', 'accepted', 'exit', 'specific', 'checkpoint', 'wait')]

    class Entry(C.Structure):
        _fields_ = [('name', W.LPWSTR), ('main', callback)]

    api.a.RegisterServiceCtrlHandlerExW.argtypes = [W.LPCWSTR, handler_type, PTR]
    api.a.RegisterServiceCtrlHandlerExW.restype = HANDLE
    api.a.SetServiceStatus.argtypes = [HANDLE, C.POINTER(Status)]
    api.a.SetServiceStatus.restype = BOOL
    api.a.StartServiceCtrlDispatcherW.argtypes = [C.POINTER(Entry)]
    api.a.StartServiceCtrlDispatcherW.restype = BOOL
    stop = threading.Event()

    @handler_type
    def handler(control, event, data, context):
        if control in (1, 5):
            stop.set()
        return 0

    @callback
    def service_main(argc, argv):
        handle = api.a.RegisterServiceCtrlHandlerExW(SERVICE_NAME, handler, None)
        if not handle:
            return
        code = 0
        try:
            api.check(api.a.SetServiceStatus(handle, C.byref(Status(0x10, 4, 5, 0, 0, 0, 0))))
            serve(api, stop)
        except Exception:
            code = 1
        finally:
            api.a.SetServiceStatus(handle, C.byref(Status(0x10, 1, 0, code, 0, 0, 0)))

    table = (Entry * 2)(Entry(SERVICE_NAME, service_main), Entry(None, callback()))
    api.check(api.a.StartServiceCtrlDispatcherW(table))


if __name__ == '__main__':
    main()
