"""Operational MVP orchestration for FOX2 Bridge."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .config import BridgeConfig
from .dispatch_poller import DispatchPoller, GitTransport
from .e2e_runner import BridgeE2ERunner, E2EResult
from .ledger import SQLiteLedger


@dataclass(frozen=True)
class OpsRunResult:
    status: str
    poll_status: str
    dispatch_path: str | None
    dispatch_id: str | None
    execution: dict[str, object] | None

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "poll_status": self.poll_status,
            "dispatch_path": self.dispatch_path,
            "dispatch_id": self.dispatch_id,
            "execution": self.execution,
        }


class BridgeOps:
    """Find and execute one opt-in immutable dispatch."""

    def __init__(
        self,
        config: BridgeConfig,
        ledger: SQLiteLedger,
        *,
        logger: Any = None,
        progress: Callable[[str], None] | None = None,
        transport: GitTransport | None = None,
    ) -> None:
        self.config = config
        self.ledger = ledger
        self.logger = logger
        self.progress = progress
        self.transport = transport or GitTransport(
            git_executable=(config.tool_paths or {})["git"] or Path("git"),
            store_path=config.bridge_root / "data" / "control.git",
        )

    def _progress(self, message: str) -> None:
        if self.progress is not None:
            self.progress(message)

    @staticmethod
    def _auto_execute_identity(raw: bytes) -> tuple[bool, str | None]:
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return False, None
        if not isinstance(payload, dict):
            return False, None
        runtime = payload.get("runtime_contract")
        if not isinstance(runtime, dict) or runtime.get("auto_execute") is not True:
            return False, None
        dispatch_id = payload.get("dispatch_id")
        if not isinstance(dispatch_id, str) or not dispatch_id:
            return False, None
        return True, dispatch_id

    def _eligible_dispatch(self) -> tuple[str, str] | None:
        control_sha = self.transport.query_control_sha(self.config.control_branch)
        if control_sha is None:
            return None
        self.transport.fetch_control(self.config.control_branch, control_sha)

        rows = self.ledger.list_candidate_discoveries(
            self.config.repository,
            self.config.control_branch,
            limit=500,
        )
        seen_paths: set[str] = set()
        for row in rows:
            path = str(row["dispatch_path"])
            if path in seen_paths:
                continue
            seen_paths.add(path)
            if row["discovery_state"] != "DISCOVERED":
                continue
            try:
                raw, _blob = self.transport.read_dispatch_blob(control_sha, path)
            except Exception:
                continue
            auto_execute, dispatch_id = self._auto_execute_identity(raw)
            if not auto_execute or dispatch_id is None:
                continue
            if self.ledger.dispatch_state(dispatch_id) is not None:
                continue
            return path, dispatch_id
        return None

    def run_next(self, *, timeout_seconds: int = 300) -> OpsRunResult:
        self._progress("OPS poll control branch")
        poller = DispatchPoller(
            self.config,
            self.ledger,
            logger=self.logger,
            transport=self.transport,
        )
        poll = poller.poll_once()
        self._progress(f"OPS poll complete: {poll.status}")
        safe_poll_states = {
            "NO_CHANGE",
            "INITIALIZED",
            "ADVANCED",
            "ALREADY_SEEN",
            "CANDIDATES_DISCOVERED",
        }
        if poll.status not in safe_poll_states:
            self._progress(f"OPS blocked by poll state: {poll.status}")
            return OpsRunResult(
                status="POLL_BLOCKED",
                poll_status=poll.status,
                dispatch_path=None,
                dispatch_id=None,
                execution={
                    "error": poll.error,
                    "reason": poll.reason,
                },
            )

        selected = self._eligible_dispatch()
        if selected is None:
            self._progress("OPS no eligible auto_execute dispatch")
            return OpsRunResult(
                status="NO_ELIGIBLE_DISPATCH",
                poll_status=poll.status,
                dispatch_path=None,
                dispatch_id=None,
                execution=None,
            )

        dispatch_path, dispatch_id = selected
        self._progress(f"OPS selected {dispatch_id}")
        result: E2EResult = BridgeE2ERunner(
            self.config,
            self.ledger,
            logger=self.logger,
            transport=self.transport,
            progress=self.progress,
        ).run_once(
            dispatch_path=dispatch_path,
            timeout_seconds=timeout_seconds,
        )
        return OpsRunResult(
            status=result.status,
            poll_status=poll.status,
            dispatch_path=dispatch_path,
            dispatch_id=dispatch_id,
            execution=result.as_dict(),
        )

    def status(
        self,
        *,
        dispatch_id: str | None = None,
        limit: int = 20,
    ) -> dict[str, object]:
        if dispatch_id is not None:
            dispatch = self.ledger.dispatch_status(dispatch_id)
            return {
                "status": "FOUND" if dispatch else "NOT_FOUND",
                "dispatch": dispatch,
            }
        return {
            "status": "OK",
            "dispatches": list(self.ledger.recent_status(limit=limit)),
        }
