"""Per-profile outbound mailbox Worker using Bridge's existing execution ledger.

The discovery cursor commits with candidates. The separate processed cursor advances
only after draining those candidates, so interruptions between these commits retry
selection, never a previously claimed Agent. Local controls use a named OS event,
not a network listener. BridgeApp owns startup reconciliation and the runtime lock.
"""

from __future__ import annotations

import ctypes
import getpass
import hashlib
import time
from ctypes import wintypes
from pathlib import Path
from typing import Callable

from .dispatch_poller import DispatchPoller, GitTransport
from .errors import BridgeError, LockHeld, StartupBlocked
from .ops_runner import BridgeOps
from .logging_config import log_event

SAFE_POLLS = {"NO_CHANGE", "INITIALIZED", "ADVANCED", "ALREADY_SEEN", "CANDIDATES_DISCOVERED"}
BACKOFF = (30, 60, 120, 300)


class LocalWake:
    """Auto-reset Windows event shared by local controls for this user/profile."""

    def __init__(self, profile: Path) -> None:
        identity = f"{getpass.getuser()}:{str(profile.resolve()).casefold()}"
        name = "Local\\FOX2BridgeWake_" + hashlib.sha256(identity.encode()).hexdigest()
        self.api = ctypes.WinDLL("kernel32", use_last_error=True)
        self.api.CreateEventW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.BOOL, wintypes.LPCWSTR]
        self.api.CreateEventW.restype = wintypes.HANDLE
        self.api.SetEvent.argtypes = [wintypes.HANDLE]
        self.api.SetEvent.restype = wintypes.BOOL
        self.api.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        self.api.WaitForSingleObject.restype = wintypes.DWORD
        self.api.CloseHandle.argtypes = [wintypes.HANDLE]
        self.api.CloseHandle.restype = wintypes.BOOL
        self.handle = self.api.CreateEventW(None, False, False, name)
        if not self.handle:
            raise StartupBlocked("cannot create local Worker wake event")

    def set(self) -> None:
        if not self.api.SetEvent(self.handle):
            raise StartupBlocked("cannot signal local Worker wake event")

    def wait(self, seconds: float) -> bool:
        result = self.api.WaitForSingleObject(self.handle, min(int(max(0, seconds) * 1000), 0xFFFFFFFE))
        if result not in (0, 258):
            raise StartupBlocked("local Worker wake wait failed")
        return result == 0

    def close(self) -> None:
        if self.handle:
            self.api.CloseHandle(self.handle)
            self.handle = None


class BackgroundWorker:
    def __init__(self, app, *, transport: GitTransport | None = None,
                 wake=None, clock: Callable[[], float] = time.monotonic,
                 timeout_seconds: int = 300) -> None:
        if not app._started:
            raise StartupBlocked("Worker requires Bridge startup and its singleton lock")
        self.app = app
        self.ledger = app.ledger
        self.config = app.config
        self.poller = DispatchPoller(self.config, self.ledger, logger=app.logger, transport=transport)
        self.ops = BridgeOps(self.config, self.ledger, logger=app.logger, transport=self.poller.transport)
        self.wake = wake or LocalWake(self.config.bridge_root)
        self.clock = clock
        self.timeout_seconds = timeout_seconds
        self.stop_sequence = int(self.ledger.worker_state()["stop_sequence"])

    def may_launch(self) -> bool:
        state = self.ledger.worker_state()
        return not state["paused"] and int(state["stop_sequence"]) == self.stop_sequence

    def iteration(self) -> dict[str, object]:
        """One deterministic poll/drain; sleeping is exclusively in run()."""
        before = self.ledger.worker_state()
        poll = self.poller.poll_once()
        # Any successful ref contact (including a missing ref) resets backoff.
        contact = poll.observed_remote_sha is not None or poll.status == "CONTROL_BRANCH_UNAVAILABLE"
        failures = 0 if contact else min(int(before["failures"]) + 1, len(BACKOFF))
        delay = self.config.poll_interval_seconds if contact else BACKOFF[failures - 1]
        observation = {"observed_sha": poll.observed_remote_sha} if poll.observed_remote_sha else {}
        self.ledger.worker_state(**observation, failures=failures,
                                 delay_seconds=delay, poll_status=poll.status)
        executions = []
        state = self.ledger.worker_state()
        if (poll.status in SAFE_POLLS and poll.observed_remote_sha != state["processed_sha"]
                and self.may_launch()):
            while self.may_launch():
                try:
                    result = self.ops.run_discovered(
                        poll_status=poll.status, control_sha=poll.observed_remote_sha,
                        timeout_seconds=self.timeout_seconds, may_launch=self.may_launch,
                        worker_stop_sequence=self.stop_sequence,
                    )
                except BridgeError as exc:
                    # Keep the processing checkpoint pending; existing Core persists
                    # terminal/delivery-recovery outcomes. Never re-claim those rows.
                    self.ledger.worker_state(poll_status="EXECUTION_BLOCKED")
                    if self.app.logger is not None:
                        log_event(self.app.logger, component="worker", event="execution_blocked",
                                  context={"error": exc.as_dict(), "control_sha": poll.observed_remote_sha})
                    break
                if result.status == "NO_ELIGIBLE_DISPATCH":
                    self.ledger.worker_state(processed_sha=poll.observed_remote_sha)
                    break
                if result.status == "PAUSED":
                    break
                executions.append(result.as_dict())
        return {"poll": poll.as_dict(), "executions": executions,
                "state": self.ledger.worker_state()}

    def run(self) -> None:
        if not self.app._worker_guard.acquire(blocking=False):
            self.wake.close()
            raise LockHeld("another Worker owns this Bridge runtime")
        try:
            while int(self.ledger.worker_state()["stop_sequence"]) == self.stop_sequence:
                state = self.iteration()["state"]
                deadline = self.clock() + float(state["delay_seconds"])
                sequence = int(state["wake_sequence"])
                while self.clock() < deadline:
                    current = self.ledger.worker_state()
                    if (int(current["wake_sequence"]) != sequence
                            or int(current["stop_sequence"]) != self.stop_sequence):
                        break
                    if self.wake.wait(deadline - self.clock()):
                        break
        finally:
            self.wake.close()
            self.app._worker_guard.release()


def control_worker(app, command: str) -> dict[str, object]:
    """Controls intentionally do not start BridgeApp or contend for its writer lock."""
    if command == "status":
        return app.ledger.worker_state()
    state = app.ledger.worker_control(command)
    wake = LocalWake(app.config.bridge_root)
    try:
        wake.set()
    finally:
        wake.close()
    return state
