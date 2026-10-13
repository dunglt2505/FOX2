"""Bridge startup, health inspection, and graceful resource cleanup."""

from __future__ import annotations

from datetime import UTC, datetime
import sys
from pathlib import Path
from typing import Any

from .config import BridgeConfig, load_config
from .copilot_adapter import CopilotAdapter, CopilotRunResult
from .dispatch_poller import DispatchPoller, PollResult
from .e2e_runner import BridgeE2ERunner, E2EResult
from .errors import BridgeError, StartupBlocked
from .ledger import SQLiteLedger, utc_now
from .logging_config import configure_logging, log_event
from .models import Status, ToolRecord
from .ops_runner import BridgeOps, OpsRunResult
from .process_lock import ProcessLock
from .runtime_tools import discover_all


class BridgeApp:
    def __init__(self, config: BridgeConfig) -> None:
        self.config = config
        self.lock = ProcessLock(config.bridge_root / "data" / "bridge.lock")
        self.ledger = SQLiteLedger(config.database_path)
        self.logger = None
        self._started = False
        self._schema_version: int | None = None
        self._tools: tuple[ToolRecord, ...] = ()

    @classmethod
    def from_file(cls, config_path: Path | None = None) -> BridgeApp:
        return cls(load_config(config_path))

    def start(self) -> None:
        try:
            self.config.bridge_root.mkdir(parents=True, exist_ok=True)
            self.config.log_directory.mkdir(parents=True, exist_ok=True)
            self.logger = configure_logging(self.config.log_directory)
            self.lock.acquire()
            self._schema_version = self.ledger.initialize()
            recovered = self.ledger.recover_interrupted_executions(
                finished_at_utc=utc_now()
            )
            self._tools = discover_all(self.config)
            self._started = True
            log_event(
                self.logger,
                component="lifecycle",
                event="bridge_started",
                context={
                    "project_id": self.config.project_id,
                    "schema_version": self._schema_version,
                    "stale_lock_metadata_recovered": self.lock.stale_owner_detected,
                    "interrupted_executions_recovered": recovered,
                },
            )
        except (OSError, BridgeError) as exc:
            try:
                self.lock.release()
            except BridgeError:
                pass
            if isinstance(exc, BridgeError):
                raise
            raise StartupBlocked(f"Bridge startup failed: {type(exc).__name__}") from exc

    def health_report(self) -> dict[str, Any]:
        if not self._started or self._schema_version is None:
            raise StartupBlocked("Bridge health is available only after successful startup")
        tools = {record.tool_name: record.as_dict() for record in self._tools}
        unavailable = [name for name, record in tools.items() if not record["available"]]
        status = Status.BLOCKED if unavailable else Status.READY
        return {
            "project_id": self.config.project_id,
            "repository": self.config.repository,
            "observed_at": datetime.now(UTC).isoformat(),
            "status": status.value,
            "config": {"status": Status.READY.value},
            "paths": {
                "status": Status.READY.value,
                "bridge_root": str(self.config.bridge_root),
                "local_repo": str(self.config.local_repo),
                "worktree_root": str(self.config.worktree_root),
            },
            "database": {
                "status": Status.READY.value,
                "path": str(self.config.database_path),
                "schema_version": self._schema_version,
                "tables": list(self.ledger.table_names()),
            },
            "process_lock": {
                "status": Status.READY.value,
                "owner": self.lock.owner,
                "stale_owner_metadata_recovered": self.lock.stale_owner_detected,
            },
            "tools": tools,
            "scope": "FOX2 Bridge Operational MVP: immutable dispatch discovery, single-use Copilot CLI execution, stale recovery, status, and run-next",
        }

    def poll_once(self) -> PollResult:
        if not self._started:
            raise StartupBlocked("Bridge poll is available only after successful startup")
        poller = DispatchPoller(
            self.config,
            self.ledger,
            logger=self.logger,
        )
        return poller.poll_once()

    def copilot_smoke(
        self,
        *,
        worktree: Path,
        timeout_seconds: int = 120,
    ) -> CopilotRunResult:
        if not self._started:
            raise StartupBlocked("Copilot smoke relay requires a started Bridge")
        prompt = (
            "Return exactly FOX2_BRIDGE_COPILOT_SMOKE_OK. "
            "Do not edit files. Do not run tools. Do not make Git changes."
        )
        adapter = CopilotAdapter(self.config)
        log_event(
            self.logger,
            component="copilot_adapter",
            event="copilot_smoke_started",
            context={"worktree": str(worktree)},
        )
        result = adapter.run_prompt(
            worktree=worktree,
            prompt=prompt,
            timeout_seconds=timeout_seconds,
        )
        log_event(
            self.logger,
            component="copilot_adapter",
            event="copilot_smoke_finished",
            context={
                "worktree": result.worktree,
                "status": result.status,
                "exit_code": result.exit_code,
            },
        )
        return result

    def e2e_once(
        self,
        *,
        dispatch_path: str,
        timeout_seconds: int = 300,
    ) -> E2EResult:
        if not self._started:
            raise StartupBlocked("E2E execution requires a started Bridge")
        runner = BridgeE2ERunner(
            self.config,
            self.ledger,
            logger=self.logger,
            progress=lambda message: print(
                f"[E2E] {message}", file=sys.stderr, flush=True
            ),
        )
        return runner.run_once(
            dispatch_path=dispatch_path,
            timeout_seconds=timeout_seconds,
        )

    def ops_run_next(self, *, timeout_seconds: int = 300) -> OpsRunResult:
        if not self._started:
            raise StartupBlocked("OPS run-next requires a started Bridge")
        return BridgeOps(
            self.config,
            self.ledger,
            logger=self.logger,
            progress=lambda message: print(
                f"[OPS] {message}", file=sys.stderr, flush=True
            ),
        ).run_next(timeout_seconds=timeout_seconds)

    def ops_status(
        self,
        *,
        dispatch_id: str | None = None,
        limit: int = 20,
    ) -> dict[str, object]:
        if not self._started:
            raise StartupBlocked("OPS status requires a started Bridge")
        return BridgeOps(
            self.config,
            self.ledger,
            logger=self.logger,
        ).status(dispatch_id=dispatch_id, limit=limit)

    def shutdown(self) -> None:
        try:
            if self.logger is not None and self._started:
                log_event(
                    self.logger,
                    component="lifecycle",
                    event="bridge_stopped",
                    context={"timestamp": utc_now()},
                )
        finally:
            self._started = False
            self.lock.release()

    def __enter__(self) -> BridgeApp:
        self.start()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.shutdown()
