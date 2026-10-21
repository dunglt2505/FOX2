"""Real non-elevated Win32 ABI/pipe tests; no service/policy activation.

These tests can run on Windows CI. They do not certify G3 host enforcement.
"""
import ctypes as C
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time
import uuid

import pytest

from fox2_agent_bridge import f1_windows
from fox2_agent_bridge.f1_protocol import AuthorityDeny
from fox2_agent_bridge.f1_windows import DWORD, HANDLE, JobLimits, ProcessInfo, StartupInfo, Win32

pytestmark = pytest.mark.skipif(os.name != 'nt', reason='Windows native API test')


def test_native_abi_and_current_user_cannot_enter_authority(tmp_path):
    api = Win32()
    assert C.sizeof(StartupInfo) == (104 if C.sizeof(C.c_void_p) == 8 else 68)
    assert C.sizeof(ProcessInfo) == (24 if C.sizeof(C.c_void_p) == 8 else 16)
    if C.sizeof(C.c_void_p) == 8:
        assert C.sizeof(JobLimits) == 144
    with pytest.raises(AuthorityDeny, match='LOCAL_SYSTEM_REQUIRED'):
        api.require_system()
    fixture = tmp_path / 'untrusted-plan.json'; fixture.write_text('{}')
    with pytest.raises(AuthorityDeny, match='UNTRUSTED_OWNER|USER_WRITABLE_AUTHORITY'):
        api.protected(fixture)
    with pytest.raises(AuthorityDeny, match='SERVICE_ABSENT'):
        api.service_pid('FOX2.G2.Nonexistent.' + uuid.uuid4().hex)
    assert api.authority_root().name == 'F1Authority'


def test_real_local_pipe_os_identity_and_untrusted_server_rejection(monkeypatch):
    api = Win32()
    # Unique test endpoint: never squat the production authority pipe name.
    name = r'\\.\pipe\FOX2.G2.Test.' + uuid.uuid4().hex
    monkeypatch.setattr(f1_windows, 'PIPE_NAME', name)
    expected_token = HANDLE()
    api.check(api.a.OpenProcessToken(api.k.GetCurrentProcess(), 8, C.byref(expected_token)))
    with api.handle(expected_token):
        expected_sid = api.token_sid(expected_token)
    ready, done = threading.Event(), queue.Queue()

    def server():
        try:
            with api.pipe() as pipe:
                ready.set()
                deadline = time.monotonic() + 10
                while time.monotonic() < deadline:
                    connected = api.k.ConnectNamedPipe(pipe, None)
                    if not connected and C.get_last_error() == 535:
                        break
                    time.sleep(0.01)
                else:
                    raise AssertionError('test client did not connect')
                raw = None
                while raw is None and time.monotonic() < deadline:
                    raw = api.receive(pipe)
                    if raw is None: time.sleep(0.01)
                assert raw == b'identity-fixture'
                with api.peer(pipe) as peer:
                    assert peer.sid == expected_sid and peer.pid == os.getpid()
                    assert peer.token and peer.session >= 0
                    api.send(pipe, b'identity-derived-from-windows')
                while time.monotonic() < deadline:
                    if api.receive(pipe) == b'ACK': break
                    time.sleep(0.01)
                api.k.DisconnectNamedPipe(pipe)
            done.put(None)
        except BaseException as exc:
            done.put(exc)
            ready.set()

    thread = threading.Thread(target=server, daemon=True); thread.start()
    assert ready.wait(5)
    with api.handle(api.k.CreateFileW(name, 0xc0000000, 0, None, 3, 0x120000, None)) as pipe:
        # A user-created server cannot impersonate SCM's LocalSystem authority.
        with pytest.raises(AuthorityDeny):
            api.verify_server(pipe)
        mode = DWORD(3)
        api.check(api.k.SetNamedPipeHandleState(pipe, C.byref(mode), None, None))
        api.send(pipe, b'identity-fixture')
        raw, deadline = None, time.monotonic() + 8
        while raw is None and time.monotonic() < deadline:
            raw = api.receive(pipe)
            if raw is None: time.sleep(0.01)
        assert raw == b'identity-derived-from-windows'
        api.send(pipe, b'ACK')
        thread.join(5)
    assert not thread.is_alive()
    error = done.get(timeout=1)
    if error: raise error


def test_native_applocker_hash_inventory_is_read_only(tmp_path):
    api = Win32()
    system = C.create_unicode_buffer(32768)
    api.check(api.k.GetSystemDirectoryW(system, len(system)))
    powershell = Path(system.value) / 'WindowsPowerShell/v1.0/powershell.exe'
    fixture = tmp_path / 'legacy.ps1'; fixture.write_text("Write-Output 'G2-harmless-fixture'\n")
    script = Path(__file__).parents[1] / 'scripts/f1_inventory.ps1'
    result = subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-File',
        str(script), '-LiteralPath', str(fixture)], capture_output=True, text=True, timeout=30,
        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    assert result.returncode == 0, 'read-only AppLocker inventory failed'
    records = json.loads(result.stdout)
    assert len(records) == 1 and records[0]['collection'] == 'Script'
    assert len(records[0]['applocker_hash']) == 64
    assert records[0]['length'] == fixture.stat().st_size
