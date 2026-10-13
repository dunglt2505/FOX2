"""OS-backed singleton lock for the local Bridge supervisor."""

from __future__ import annotations

import json
import msvcrt
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .errors import LockError, LockHeld


class ProcessLock:
    def __init__(self, lock_path: Path) -> None:
        self.lock_path = lock_path
        self._stream: Any = None
        self._acquired = False
        self.stale_owner_detected = False
        self.owner: dict[str, object] | None = None

    def acquire(self) -> None:
        if self._acquired:
            return
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        stream = None
        try:
            stream = self.lock_path.open("a+b")
            stream.seek(0, os.SEEK_END)
            if stream.tell() == 0:
                stream.write(b" ")
                stream.flush()
            stream.seek(0)
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                stream.close()
                raise LockHeld("another Bridge process owns the runtime lock") from exc

            self._stream = stream
            self._acquired = True
            stream.seek(0)
            previous = stream.read()
            if previous:
                try:
                    old_owner = json.loads(previous.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    old_owner = {}
                self.stale_owner_detected = bool(old_owner)

            self.owner = {
                "pid": os.getpid(),
                "acquired_at": datetime.now(UTC).isoformat(),
            }
            stream.seek(0)
            stream.truncate()
            stream.write(json.dumps(self.owner).encode("utf-8"))
            stream.flush()
            os.fsync(stream.fileno())
        except LockHeld:
            raise
        except OSError as exc:
            cleanup_error = None
            if self._acquired:
                try:
                    self.release()
                except LockError as release_exc:
                    cleanup_error = release_exc.message
            elif stream is not None and not stream.closed:
                stream.close()
            suffix = f"; cleanup also failed: {cleanup_error}" if cleanup_error else ""
            raise LockError(f"cannot acquire runtime lock: {exc}{suffix}") from exc

    def release(self) -> None:
        if not self._acquired or self._stream is None:
            return
        stream = self._stream
        self._stream = None
        self._acquired = False
        try:
            stream.seek(0)
            stream.truncate()
            stream.flush()
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError as exc:
            raise LockError(f"cannot release runtime lock: {exc}") from exc
        finally:
            stream.close()

    def __enter__(self) -> ProcessLock:
        self.acquire()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.release()
