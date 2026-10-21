"""Win32-only F1 transport, token, ACL and suspended process primitives.

No pywin32/download dependency. No service installation or policy mutation.
All handles have pointer-sized ctypes signatures, including on Windows x64.
"""
from __future__ import annotations

import ctypes as C
from ctypes import wintypes as W
from contextlib import contextmanager
import os
from pathlib import Path
import subprocess

from .f1_protocol import AuthorityDeny, MAX_MESSAGE, PIPE_NAME, SERVICE_NAME, Peer

HANDLE = W.HANDLE
PTR = C.c_void_p
DWORD = W.DWORD
BOOL = W.BOOL
INVALID = C.c_void_p(-1).value


class SecurityAttributes(C.Structure):
    _fields_ = [('length', DWORD), ('descriptor', PTR), ('inherit', BOOL)]


class StartupInfo(C.Structure):
    _fields_ = [('cb', DWORD), ('reserved', W.LPWSTR), ('desktop', W.LPWSTR),
                ('title', W.LPWSTR), ('x', DWORD), ('y', DWORD), ('cx', DWORD),
                ('cy', DWORD), ('charsx', DWORD), ('charsy', DWORD), ('fill', DWORD),
                ('flags', DWORD), ('show', W.WORD), ('reserved2', W.WORD),
                ('bytes', PTR), ('stdin', HANDLE), ('stdout', HANDLE), ('stderr', HANDLE)]


class ProcessInfo(C.Structure):
    _fields_ = [('process', HANDLE), ('thread', HANDLE), ('pid', DWORD), ('tid', DWORD)]


class JobBasic(C.Structure):
    _fields_ = [('process_time', C.c_int64), ('job_time', C.c_int64), ('flags', DWORD),
                ('min_working', C.c_size_t), ('max_working', C.c_size_t),
                ('active_processes', DWORD), ('affinity', C.c_size_t),
                ('priority', DWORD), ('scheduling', DWORD)]


class JobLimits(C.Structure):
    _fields_ = [('basic', JobBasic), ('io', C.c_uint64 * 6),
                ('process_memory', C.c_size_t), ('job_memory', C.c_size_t),
                ('peak_process', C.c_size_t), ('peak_job', C.c_size_t)]


class ServiceConfig(C.Structure):
    _fields_ = [('type', DWORD), ('start', DWORD), ('error', DWORD),
                ('binary', W.LPWSTR), ('group', W.LPWSTR), ('tag', DWORD),
                ('dependencies', W.LPWSTR), ('account', W.LPWSTR), ('display', W.LPWSTR)]


class Win32:
    def __init__(self):
        if os.name != 'nt':
            raise AuthorityDeny('WINDOWS_REQUIRED')
        self.k = C.WinDLL('kernel32', use_last_error=True)
        self.a = C.WinDLL('advapi32', use_last_error=True)
        self.u = C.WinDLL('userenv', use_last_error=True)
        self.s = C.WinDLL('shell32', use_last_error=True)
        self.o = C.WinDLL('ole32', use_last_error=True)
        signatures = {
            'CloseHandle': (BOOL, [HANDLE]), 'LocalFree': (PTR, [PTR]),
            'GetCurrentProcess': (HANDLE, []), 'GetCurrentThread': (HANDLE, []),
            'GetSystemDirectoryW': (W.UINT, [W.LPWSTR, W.UINT]),
            'GetNamedPipeServerProcessId': (BOOL, [HANDLE, C.POINTER(DWORD)]),
            'GetNamedPipeClientProcessId': (BOOL, [HANDLE, C.POINTER(DWORD)]),
            'OpenProcess': (HANDLE, [DWORD, BOOL, DWORD]),
            'QueryFullProcessImageNameW': (BOOL, [HANDLE, DWORD, W.LPWSTR, C.POINTER(DWORD)]),
            'CreateNamedPipeW': (HANDLE, [W.LPCWSTR, DWORD, DWORD, DWORD, DWORD, DWORD,
                                        DWORD, C.POINTER(SecurityAttributes)]),
            'ConnectNamedPipe': (BOOL, [HANDLE, PTR]),
            'DisconnectNamedPipe': (BOOL, [HANDLE]),
            'PeekNamedPipe': (BOOL, [HANDLE, PTR, DWORD, PTR, C.POINTER(DWORD), PTR]),
            'ReadFile': (BOOL, [HANDLE, PTR, DWORD, C.POINTER(DWORD), PTR]),
            'WriteFile': (BOOL, [HANDLE, PTR, DWORD, C.POINTER(DWORD), PTR]),
            'CreateFileW': (HANDLE, [W.LPCWSTR, DWORD, DWORD, PTR, DWORD, DWORD, HANDLE]),
            'SetNamedPipeHandleState': (BOOL, [HANDLE, C.POINTER(DWORD), PTR, PTR]),
            'CreateJobObjectW': (HANDLE, [PTR, W.LPCWSTR]),
            'SetInformationJobObject': (BOOL, [HANDLE, C.c_int, PTR, DWORD]),
            'AssignProcessToJobObject': (BOOL, [HANDLE, HANDLE]),
            'ResumeThread': (DWORD, [HANDLE]),
            'TerminateProcess': (BOOL, [HANDLE, W.UINT]),
            'CreateMutexW': (HANDLE, [C.POINTER(SecurityAttributes), BOOL, W.LPCWSTR]),
        }
        for name, (result, args) in signatures.items():
            fn = getattr(self.k, name); fn.restype = result; fn.argtypes = args
        signatures = {
            'OpenProcessToken': (BOOL, [HANDLE, DWORD, C.POINTER(HANDLE)]),
            'OpenThreadToken': (BOOL, [HANDLE, DWORD, BOOL, C.POINTER(HANDLE)]),
            'GetTokenInformation': (BOOL, [HANDLE, C.c_int, PTR, DWORD, C.POINTER(DWORD)]),
            'ConvertSidToStringSidW': (BOOL, [PTR, C.POINTER(W.LPWSTR)]),
            'ConvertStringSecurityDescriptorToSecurityDescriptorW':
                (BOOL, [W.LPCWSTR, DWORD, C.POINTER(PTR), PTR]),
            'GetFileSecurityW': (BOOL, [W.LPCWSTR, DWORD, PTR, DWORD, C.POINTER(DWORD)]),
            'GetSecurityDescriptorOwner': (BOOL, [PTR, C.POINTER(PTR), C.POINTER(BOOL)]),
            'GetSecurityDescriptorDacl': (BOOL, [PTR, C.POINTER(BOOL), C.POINTER(PTR), C.POINTER(BOOL)]),
            'GetSecurityDescriptorControl': (BOOL, [PTR, C.POINTER(W.WORD), C.POINTER(DWORD)]),
            'GetAce': (BOOL, [PTR, DWORD, C.POINTER(PTR)]),
            'ImpersonateNamedPipeClient': (BOOL, [HANDLE]), 'RevertToSelf': (BOOL, []),
            'DuplicateTokenEx': (BOOL, [HANDLE, DWORD, PTR, C.c_int, C.c_int, C.POINTER(HANDLE)]),
            'CheckTokenMembership': (BOOL, [HANDLE, PTR, C.POINTER(BOOL)]),
            'ConvertStringSidToSidW': (BOOL, [W.LPCWSTR, C.POINTER(PTR)]),
            'CreateProcessAsUserW': (BOOL, [HANDLE, W.LPCWSTR, W.LPWSTR, PTR, PTR, BOOL,
                DWORD, PTR, W.LPCWSTR, C.POINTER(StartupInfo), C.POINTER(ProcessInfo)]),
            'OpenSCManagerW': (HANDLE, [W.LPCWSTR, W.LPCWSTR, DWORD]),
            'OpenServiceW': (HANDLE, [HANDLE, W.LPCWSTR, DWORD]),
            'CloseServiceHandle': (BOOL, [HANDLE]),
            'QueryServiceStatusEx': (BOOL, [HANDLE, C.c_int, PTR, DWORD, C.POINTER(DWORD)]),
            'QueryServiceConfigW': (BOOL, [HANDLE, PTR, DWORD, C.POINTER(DWORD)]),
        }
        for name, (result, args) in signatures.items():
            fn = getattr(self.a, name); fn.restype = result; fn.argtypes = args
        self.u.CreateEnvironmentBlock.argtypes = [C.POINTER(PTR), HANDLE, BOOL]
        self.u.CreateEnvironmentBlock.restype = BOOL
        self.u.DestroyEnvironmentBlock.argtypes = [PTR]
        self.u.DestroyEnvironmentBlock.restype = BOOL
        self.s.SHGetKnownFolderPath.argtypes = [PTR, DWORD, HANDLE, C.POINTER(W.LPWSTR)]
        self.s.SHGetKnownFolderPath.restype = C.c_long
        self.o.CoTaskMemFree.argtypes = [PTR]

    @staticmethod
    def check(ok):
        if not ok:
            raise AuthorityDeny('WINDOWS_API_DENY')
        return ok

    @contextmanager
    def handle(self, handle):
        if not handle or handle == INVALID:
            raise AuthorityDeny('WINDOWS_HANDLE_DENY')
        try:
            yield handle
        finally:
            self.k.CloseHandle(handle)

    def sid(self, pointer) -> str:
        result = W.LPWSTR()
        self.check(self.a.ConvertSidToStringSidW(pointer, C.byref(result)))
        try:
            return result.value
        finally:
            self.k.LocalFree(result)

    def token_info(self, token, kind):
        needed = DWORD()
        self.a.GetTokenInformation(token, kind, None, 0, C.byref(needed))
        buffer = C.create_string_buffer(needed.value)
        self.check(self.a.GetTokenInformation(token, kind, buffer, len(buffer), C.byref(needed)))
        return buffer

    def token_sid(self, token) -> str:
        info = self.token_info(token, 1)
        return self.sid(C.cast(info, C.POINTER(PTR))[0])

    def require_system(self):
        token = HANDLE()
        self.check(self.a.OpenProcessToken(self.k.GetCurrentProcess(), 8, C.byref(token)))
        with self.handle(token):
            if self.token_sid(token) != 'S-1-5-18':
                raise AuthorityDeny('LOCAL_SYSTEM_REQUIRED')

    def service_pid(self, name=SERVICE_NAME) -> int:
        manager = self.a.OpenSCManagerW(None, None, 1)
        if not manager:
            raise AuthorityDeny('SCM_UNAVAILABLE')
        service = None
        try:
            service = self.a.OpenServiceW(manager, name, 4)
            if not service:
                raise AuthorityDeny('SERVICE_ABSENT')
            status, needed = (DWORD * 9)(), DWORD()
            self.check(self.a.QueryServiceStatusEx(service, 0, status, C.sizeof(status), C.byref(needed)))
            if status[1] != 4:
                raise AuthorityDeny('SERVICE_NOT_RUNNING')
            return status[7]
        finally:
            if service:
                self.a.CloseServiceHandle(service)
            self.a.CloseServiceHandle(manager)

    def service_config(self) -> tuple[str, str, int, int]:
        manager = self.a.OpenSCManagerW(None, None, 1)
        if not manager:
            raise AuthorityDeny('SCM_UNAVAILABLE')
        service = None
        try:
            service = self.a.OpenServiceW(manager, SERVICE_NAME, 1)
            if not service:
                raise AuthorityDeny('SERVICE_ABSENT')
            needed = DWORD()
            self.a.QueryServiceConfigW(service, None, 0, C.byref(needed))
            buffer = C.create_string_buffer(needed.value)
            self.check(self.a.QueryServiceConfigW(service, buffer, len(buffer), C.byref(needed)))
            config = C.cast(buffer, C.POINTER(ServiceConfig)).contents
            return config.binary, config.account, config.type, config.start
        finally:
            if service:
                self.a.CloseServiceHandle(service)
            self.a.CloseServiceHandle(manager)

    def verify_server(self, pipe):
        pid = DWORD()
        self.check(self.k.GetNamedPipeServerProcessId(pipe, C.byref(pid)))
        if pid.value != self.service_pid():
            raise AuthorityDeny('SERVER_PID_MISMATCH')
        with self.handle(self.k.OpenProcess(0x1000, False, pid)) as process:
            token = HANDLE()
            self.check(self.a.OpenProcessToken(process, 8, C.byref(token)))
            with self.handle(token):
                if self.token_sid(token) != 'S-1-5-18':
                    raise AuthorityDeny('SERVER_IDENTITY')
            name, length = C.create_unicode_buffer(32768), DWORD(32768)
            self.check(self.k.QueryFullProcessImageNameW(process, 0, name, C.byref(length)))
            root = self.authority_root()
            expected = root / 'runtime' / 'Scripts' / 'python.exe'
            if Path(name.value).resolve() != expected.resolve():
                raise AuthorityDeny('SERVER_IMAGE')
            self.protected(root, root=True)
            for path in (expected, *expected.parents):
                if path == root:
                    break
                self.protected(path)

    def authority_root(self) -> Path:
        # FOLDERID_ProgramData; never trust requester-supplied environment paths.
        import uuid
        guid = C.create_string_buffer(uuid.UUID('62ab5d82-fdc1-4dc3-a9dd-070d1d495d97').bytes_le)
        result = W.LPWSTR()
        self.check(self.s.SHGetKnownFolderPath(guid, 0, None, C.byref(result)) == 0)
        try:
            return Path(result.value) / 'FOX2' / 'F1Authority'
        finally:
            self.o.CoTaskMemFree(result)

    def protected(self, path: Path, *, root=False, ancestor=False) -> None:
        """Reject reparse paths, untrusted owners, null ACLs and any user writes."""
        for p in (path, *path.parents):
            if p.is_symlink() or p.is_junction():
                raise AuthorityDeny('REPARSE_PATH')
        needed = DWORD()
        self.a.GetFileSecurityW(str(path), 5, None, 0, C.byref(needed))
        descriptor = C.create_string_buffer(needed.value)
        self.check(self.a.GetFileSecurityW(str(path), 5, descriptor, len(descriptor), C.byref(needed)))
        owner, defaulted = PTR(), BOOL()
        self.check(self.a.GetSecurityDescriptorOwner(descriptor, C.byref(owner), C.byref(defaulted)))
        trusted = ('S-1-5-18', 'S-1-5-32-544',
                   'S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464')
        if self.sid(owner) not in (trusted[:2] if root else trusted):
            raise AuthorityDeny('UNTRUSTED_OWNER')
        control, revision = W.WORD(), DWORD()
        self.check(self.a.GetSecurityDescriptorControl(descriptor, C.byref(control), C.byref(revision)))
        if root and not control.value & 0x1000:
            raise AuthorityDeny('UNPROTECTED_DACL')
        present, acl = BOOL(), PTR()
        self.check(self.a.GetSecurityDescriptorDacl(descriptor, C.byref(present), C.byref(acl), C.byref(defaulted)))
        if not present.value or not acl.value:
            raise AuthorityDeny('NULL_DACL')
        count = C.c_ushort.from_address(acl.value + 4).value
        if not count:
            raise AuthorityDeny('EMPTY_DACL')
        for index in range(count):
            ace = PTR()
            self.check(self.a.GetAce(acl, index, C.byref(ace)))
            # Only simple ACCESS_ALLOWED_ACE entries are supported by this seal.
            if C.c_ubyte.from_address(ace.value).value != 0:
                raise AuthorityDeny('UNSUPPORTED_DACL')
            trustee = self.sid(ace.value + 8)
            mask = DWORD.from_address(ace.value + 4).value
            flags = C.c_ubyte.from_address(ace.value + 1).value
            if flags & 8:  # INHERIT_ONLY is not an access grant on this object
                continue
            unsafe = mask & (0x100d0042 if ancestor else ~0x1200a9)
            if trustee not in trusted and unsafe:
                raise AuthorityDeny('USER_WRITABLE_AUTHORITY')

    @contextmanager
    def security(self, sddl):
        descriptor = PTR()
        self.check(self.a.ConvertStringSecurityDescriptorToSecurityDescriptorW(
            sddl, 1, C.byref(descriptor), None))
        try:
            yield SecurityAttributes(C.sizeof(SecurityAttributes), descriptor, False)
        finally:
            self.k.LocalFree(descriptor)

    @contextmanager
    def singleton(self):
        with self.security('D:P(A;;GA;;;SY)(A;;GA;;;BA)') as sa:
            handle = self.k.CreateMutexW(C.byref(sa), True, r'Global\FOX2.F1.Authority.v1')
            error = C.get_last_error()
        with self.handle(handle):
            if error == 183:
                raise AuthorityDeny('COMPETING_SERVICE')
            yield

    @contextmanager
    def pipe(self):
        # First-instance prevents pipe squatting; reject remote clients in NPFS.
        with self.security('D:P(A;;GA;;;SY)(A;;GA;;;BA)(A;;GRGW;;;IU)') as sa:
            handle = self.k.CreateNamedPipeW(PIPE_NAME, 0x80003, 0x0f, 1,
                                           MAX_MESSAGE, MAX_MESSAGE, 1000, C.byref(sa))
        with self.handle(handle):
            yield handle

    @contextmanager
    def peer(self, pipe):
        token, primary = HANDLE(), HANDLE()
        self.check(self.a.ImpersonateNamedPipeClient(pipe))
        try:
            self.check(self.a.OpenThreadToken(self.k.GetCurrentThread(), 0x0b, True, C.byref(token)))
            with self.handle(token):
                sid = self.token_sid(token)
                session = DWORD.from_buffer(self.token_info(token, 12)).value
                membership, admin = PTR(), BOOL()
                self.check(self.a.ConvertStringSidToSidW('S-1-5-32-544', C.byref(membership)))
                try:
                    self.check(self.a.CheckTokenMembership(token, membership, C.byref(admin)))
                finally:
                    self.k.LocalFree(membership)
                # Require a real impersonation token, never identification-only.
                level = DWORD.from_buffer(self.token_info(token, 9)).value
                if level < 2:
                    raise AuthorityDeny('IMPERSONATION_LEVEL')
                self.check(self.a.DuplicateTokenEx(token, 0x18b, None, 2, 1, C.byref(primary)))
        finally:
            if not self.a.RevertToSelf():
                if primary:
                    self.k.CloseHandle(primary)
                raise RuntimeError('fatal impersonation recovery failure')
        with self.handle(primary):
            pid = DWORD()
            self.check(self.k.GetNamedPipeClientProcessId(pipe, C.byref(pid)))
            yield Peer(sid, session, pid.value, primary.value, bool(admin.value))

    def receive(self, pipe) -> bytes | None:
        available = DWORD()
        self.check(self.k.PeekNamedPipe(pipe, None, 0, None, C.byref(available), None))
        if not available.value:
            return None
        if available.value > MAX_MESSAGE:
            raise AuthorityDeny('MESSAGE_SIZE')
        data, read = C.create_string_buffer(MAX_MESSAGE), DWORD()
        self.check(self.k.ReadFile(pipe, data, MAX_MESSAGE, C.byref(read), None))
        return data.raw[:read.value]

    def send(self, pipe, raw: bytes):
        if len(raw) > MAX_MESSAGE:
            raise AuthorityDeny('MESSAGE_SIZE')
        written = DWORD()
        self.check(self.k.WriteFile(pipe, raw, len(raw), C.byref(written), None))
        self.check(written.value == len(raw))


class Child:
    def __init__(self, api: Win32, job, info):
        self.api, self.job, self.info = api, job, info
        self.expires_at = 0

    def resume(self):
        if self.api.k.ResumeThread(self.info.thread) == 0xffffffff:
            raise AuthorityDeny('RESUME_FAILED')
        self.api.k.CloseHandle(self.info.thread)
        self.info.thread = None

    def close(self):
        # Closing the job kills the entire process tree, including suspended child.
        for handle in (self.job, self.info.thread, self.info.process):
            if handle:
                self.api.k.CloseHandle(handle)
        self.job = self.info.thread = self.info.process = None


class WindowsSpawner:
    def __init__(self, api: Win32):
        self.api = api

    def prepare(self, task, peer: Peer) -> Child:
        api = self.api
        job = api.k.CreateJobObjectW(None, None)
        if not job:
            raise AuthorityDeny('JOB_CREATE_FAILED')
        info, environment = ProcessInfo(), PTR()
        try:
            limits = JobLimits(); limits.basic.flags = 0x2000  # KILL_ON_JOB_CLOSE
            api.check(api.k.SetInformationJobObject(job, 9, C.byref(limits), C.sizeof(limits)))
            # Read the authenticated user's environment without inheriting the
            # service's credentials. Retain only credential/profile locations.
            api.check(api.u.CreateEnvironmentBlock(C.byref(environment), peer.token, False))
            retained = {}
            cursor = environment.value
            while True:
                entry = C.wstring_at(cursor)
                if not entry:
                    break
                key, separator, value = entry.partition('=')
                if separator and key.upper() in {'USERPROFILE', 'APPDATA', 'LOCALAPPDATA',
                        'TEMP', 'TMP', 'USERNAME', 'USERDOMAIN', 'HOMEDRIVE', 'HOMEPATH'}:
                    retained[key.upper()] = value
                cursor += (len(entry) + 1) * C.sizeof(C.c_wchar)
            api.u.DestroyEnvironmentBlock(environment)
            environment = PTR()
            system = C.create_unicode_buffer(32768)
            api.check(api.k.GetSystemDirectoryW(system, len(system)))
            system_root = str(Path(system.value).parent)
            retained.update(SYSTEMROOT=system_root, WINDIR=system_root,
                            PATH=str(Path(task.argv[0]).parent) + ';' + system.value)
            block = C.create_unicode_buffer('\0'.join(k + '=' + v for k, v in sorted(retained.items())) + '\0\0')
            startup = StartupInfo(); startup.cb = C.sizeof(startup)
            command = C.create_unicode_buffer(subprocess.list2cmdline(task.argv))
            api.check(api.a.CreateProcessAsUserW(peer.token, task.argv[0], command,
                None, None, False, 0x08000404, C.cast(block, PTR), task.worktree,
                C.byref(startup), C.byref(info)))
            api.check(api.k.AssignProcessToJobObject(job, info.process))
            return Child(api, job, info)
        except BaseException:
            if info.process:
                api.k.TerminateProcess(info.process, 1)
            Child(api, job, info).close()
            raise
        finally:
            if environment:
                api.u.DestroyEnvironmentBlock(environment)
