"""Non-granting F1 wire contract. Only the Windows service creates Peer objects.

Nothing in this module, or an imported Python service object, is an OS fence.
The production entry point requires SCM/LocalSystem and protected host adoption.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

PIPE_NAME = r"\\.\pipe\FOX2.F1.Authority.v1"
SERVICE_NAME = "FOX2F1Authority"
MAX_MESSAGE = 16384


class AuthorityDeny(ValueError):
    """Bounded reason safe to return over IPC."""


@dataclass(frozen=True)
class Peer:
    sid: str
    session: int
    pid: int
    token: int
    administrator: bool = False


@dataclass(frozen=True)
class Request:
    protocol_version: int
    dispatch_id: str
    immutable_task_sha: str
    source_digest: str
    package_digest: str
    requested_actor: str
    request_nonce: str
    epoch: int

    @classmethod
    def parse(cls, value: object) -> Request:
        if not isinstance(value, dict) or set(value) != set(cls.__dataclass_fields__):
            raise AuthorityDeny("REQUEST_SHAPE")
        if (type(value['protocol_version']) is not int or value['protocol_version'] != 1
                or type(value['epoch']) is not int or value['epoch'] <= 0
                or not isinstance(value['dispatch_id'], str)
                or not re.fullmatch(r'FOX2-[A-Za-z0-9._-]{1,240}', value['dispatch_id'])
                or value['requested_actor'] not in ('CODEX', 'COPILOT')):
            raise AuthorityDeny("REQUEST_IDENTITY")
        for name in ('immutable_task_sha', 'source_digest', 'package_digest', 'request_nonce'):
            if not isinstance(value[name], str) or not re.fullmatch('[0-9a-f]{64}', value[name]):
                raise AuthorityDeny("REQUEST_DIGEST")
        return cls(**value)


def deny(reason: str) -> dict:
    return {'decision': 'DENY', 'reason': reason}
