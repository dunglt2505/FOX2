"""Installed request/status surface. No local fallback and no spawn token."""
import ctypes as C
import json
import time

from .f1_protocol import AuthorityDeny, PIPE_NAME, deny
from .f1_windows import Win32


def call(operation: str, request=None) -> dict:
    try:
        api = Win32()
        # Authenticated impersonation, local pipe only. Never start the service.
        with api.handle(api.k.CreateFileW(PIPE_NAME, 0xc0000000, 0, None, 3,
                                         0x120000, None)) as pipe:
            api.verify_server(pipe)
            mode = C.c_ulong(3)  # message mode, nonblocking
            api.check(api.k.SetNamedPipeHandleState(pipe, C.byref(mode), None, None))
            api.send(pipe, json.dumps({'operation': operation, 'request': request},
                                     separators=(',', ':')).encode())
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                raw = api.receive(pipe)
                if raw is not None:
                    result = json.loads(raw)
                    if not isinstance(result, dict) or result.get('decision') not in (
                            'DENY', 'STARTED', 'RECORDED'):
                        raise AuthorityDeny('RESPONSE_SHAPE')
                    api.send(pipe, b'ACK')
                    return result
                time.sleep(0.01)
            return deny('SERVICE_TIMEOUT_UNCERTAIN')
    except (AuthorityDeny, OSError, ValueError, TypeError):
        return deny('SERVICE_UNAVAILABLE_OR_UNTRUSTED')


def inspect_authority() -> dict:
    return call('inspect_authority')


def claim_and_spawn(request: dict) -> dict:
    return call('claim_and_spawn', request)


def execute_dispatch(dispatch_id: str, dispatch_digest: str) -> dict:
    status = call('inspect_authority', {'dispatch_id': dispatch_id, 'dispatch_digest': dispatch_digest})
    request = status.get('request')
    if not isinstance(request, dict):
        return deny('DISPATCH_NOT_STAGED')
    return claim_and_spawn(request)
