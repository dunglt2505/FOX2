"""Single service-owned claim/spawn engine; no client launch capabilities.

Dependencies are injected for deterministic source tests. Production constructs
these only in f1_service after OS authentication and protected-plan validation.
Offline store/reconciliation APIs remain insufficient to authorize execution.
"""
from __future__ import annotations

from dataclasses import dataclass
import secrets
import threading
import time

from .f1_broker_store import BrokerEpoch, F1BrokerStore
from .f1_protocol import AuthorityDeny, Peer, Request, deny


@dataclass(frozen=True)
class ApprovedTask:
    request: Request
    caller_sid: str
    caller_session: int
    expires_at: int
    argv: tuple[str, ...]
    worktree: str
    # Host-sealed plan identity; never obtained from an IPC request.
    bindings: tuple[tuple[str, str], ...]
    controls_db: str


class Authority:
    def __init__(self, store: F1BrokerStore, *, fence, spawner,
                 clock=time.time, monotonic=time.monotonic):
        self.store, self.fence, self.spawner = store, fence, spawner
        self.clock, self.monotonic = clock, monotonic
        self.lock = threading.RLock()
        self.tasks: dict[str, ApprovedTask] = {}
        self.epoch = 0
        self.closed = True
        self.wall = 0
        self.tick = 0.0
        self.children = []
        self.storage_uncertain = False
        self.adoption_digest = ''

    def start(self, binding: BrokerEpoch, *, adoption_digest: str | None = None) -> None:
        with self.lock:
            # A failed boot still fences the old epoch and all old leases.
            self.epoch = self.store.begin_service_epoch(binding)
            self.adoption_digest = adoption_digest or binding.policy_id
            self.wall, self.tick = int(self.clock()), self.monotonic()
            self.closed = True

    def _now(self) -> int:
        now, tick = int(self.clock()), self.monotonic()
        # Compare wall time against both its durable floor and elapsed uptime.
        if now < self.wall or tick < self.tick or now + 2 < self.wall + tick - self.tick:
            raise AuthorityDeny('CLOCK_ROLLBACK')
        if not self.store.observe_trusted_time(now):
            raise AuthorityDeny('CLOCK_ROLLBACK')
        self.wall, self.tick = now, tick
        return now

    def stage(self, tasks: tuple[ApprovedTask, ...]) -> None:
        """Privileged, in-process only. Reconciliation precedes this operation."""
        with self.lock:
            if self.store.service_plan_revoked(self.adoption_digest):
                raise AuthorityDeny('ADOPTION_REVOKED')
            if len({t.request.dispatch_id for t in tasks}) != len(tasks):
                raise AuthorityDeny('DUPLICATE_TASK')
            self.fence(None)
            for task in tasks:
                if task.request.epoch != self.epoch:
                    raise AuthorityDeny('STAGED_EPOCH')
                self.fence(task)
            self.store.activate_service_epoch(self.epoch, self._now())
            self.tasks = {t.request.dispatch_id: t for t in tasks}
            self.closed = False

    def revoke(self) -> None:
        with self.lock:
            self.closed = True
            try:
                self.store.revoke_from_privileged_service(adoption_digest=self.adoption_digest)
            except Exception:
                self.storage_uncertain = True
            finally:
                for child in self.children:
                    child.close()  # kill-on-close job, even on corrupt storage
                self.children.clear()

    def inspect(self) -> dict:
        # Status is explicitly non-granting. No lease IDs are returned.
        return {'decision': 'DENY', 'reason': 'STATUS_ONLY',
                'epoch': self.epoch, 'staged': not self.closed}

    def monitor(self) -> None:
        with self.lock:
            if self.closed:
                return
            try:
                now = self._now()
                self.fence(None)
                live = []
                for child in self.children:
                    if now >= child.expires_at:
                        child.close()
                    else:
                        live.append(child)
                self.children = live
            except Exception:
                self.revoke()

    def claim_and_spawn(self, value: object, peer: Peer) -> dict:
        with self.lock:
            child = None
            try:
                request = Request.parse(value)
                if self.closed:
                    raise AuthorityDeny('AUTHORITY_REVOKED')
                task = self.tasks.get(request.dispatch_id)
                if task is None or request != task.request or request.epoch != self.epoch:
                    raise AuthorityDeny('TASK_BINDING')
                if (peer.sid != task.caller_sid or peer.session != task.caller_session
                        or peer.pid <= 0 or not peer.token):
                    raise AuthorityDeny('CALLER_IDENTITY')
                now = self._now()
                self.fence(task)
                expires = min(task.expires_at, now + 60)
                lease = secrets.token_hex(32)  # retained inside service only
                if not self.store.claim(dispatch_id=request.dispatch_id, lease_id=lease,
                        epoch=self.epoch, package_sha256=request.package_digest,
                        now=now, expires_at=expires):
                    raise AuthorityDeny('CONSUMED_OR_EXPIRED')
                # Consume a one-use spawn intent before entering any OS creation API.
                self.fence(task)
                if not self.store.take_spawn_intent(dispatch_id=request.dispatch_id,
                        lease_id=lease, epoch=self.epoch,
                        package_sha256=request.package_digest, now=self._now()):
                    raise AuthorityDeny('LEASE_INVALID')
                child = self.spawner.prepare(task, peer)  # suspended, job-assigned
                self.fence(task)
                if not self.store.spawn_permitted(dispatch_id=request.dispatch_id,
                        lease_id=lease, epoch=self.epoch,
                        package_sha256=request.package_digest, now=self._now()):
                    raise AuthorityDeny('LEASE_INVALID')
                child.expires_at = expires
                child.resume()
                self.children.append(child)
                return {'decision': 'STARTED', 'dispatch_id': request.dispatch_id}
            except AuthorityDeny as exc:
                if child is not None:
                    child.close()
                if str(exc) not in ('REQUEST_SHAPE', 'REQUEST_IDENTITY', 'REQUEST_DIGEST',
                        'AUTHORITY_REVOKED', 'TASK_BINDING', 'CALLER_IDENTITY',
                        'CONSUMED_OR_EXPIRED'):
                    self.revoke()
                return deny(str(exc))
            except Exception:
                if child is not None:
                    child.close()
                # Includes SQLite corruption, OS/API or ambiguous spawn failure.
                self.revoke()
                return deny('AUTHORITY_UNCERTAIN')

    def report_outcome(self, dispatch_id: str, outcome: str, peer: Peer) -> dict:
        with self.lock:
            task = self.tasks.get(dispatch_id)
            if not task or peer.sid != task.caller_sid or peer.session != task.caller_session:
                return deny('CALLER_IDENTITY')
            return {'decision': 'RECORDED' if self.store.report_outcome(
                dispatch_id, outcome) else 'DENY'}
