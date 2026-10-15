"""One-shot, non-dispatch Windows installer probe for FOX2 Bridge Core 006.

Reuses the already-built Core006 wheel package in a NEW disposable profile.
No installed user Bridge access, no source changes, no dispatch replay.
Reports the failed stage and sanitized error class rather than only an exit code.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

WORKTREE = Path(r"C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B")
SOURCE_HEAD = "ce7a8253926b7489c79311e26d7dc75ba8c81fc6"
BASE = Path(r"C:\Temp\fox2-core006-u_7p0m_1")
BUILD_PYTHON = BASE / "build" / "Scripts" / "python.exe"
PACKAGE = BASE / "package1.zip"
EXPECTED_PACKAGE_SHA256 = "6e96ee19ea103e7bd606a63abf071d00de6fa3c6cd1663b8d9d921b01d70b3a9"

# Python source running inside the isolated build venv. No persistent monkey patch:
# the original installation._run is replaced only in this diagnostic subprocess.
CHILD = r'''
import json
import os
from pathlib import Path
import re
import subprocess
import sys

def scrub(value):
    value = str(value)
    value = re.sub(r"(?i)(authorization|bearer|api[_-]?key|token|password)[=: ]+\S+", r"\1=[REDACTED]", value)
    value = re.sub(r"https?://\S+", "<URL>", value)
    value = re.sub(r"[A-Za-z]:\\[^\s\"']+", "<WINDOWS_PATH>", value)
    return value.replace("\n", " ")[:250]

def classify(stderr):
    lines = [x.strip() for x in (stderr or "").splitlines() if x.strip()]
    significant = [x for x in lines if re.search(
        r"error|failed|denied|permission|no module|cannot|not found|not available|missing|exception|traceback|unable|invalid",
        x, re.IGNORECASE)]
    return scrub(significant[-1] if significant else (lines[-1] if lines else "<NO_STDERR>"))

result = {"status": "UNKNOWN", "stage": "BOOTSTRAP"}
try:
    from fox2_agent_bridge import installation as inst
    expected_root = Path(sys.argv[3]).resolve()
    actual_root = inst.BRIDGE_ROOT.resolve()
    if actual_root != expected_root:
        raise RuntimeError("ISOLATION_ROOT_MISMATCH")
    result["stage"] = "VERIFY_PACKAGE"
    package = Path(sys.argv[1])
    sha = sys.argv[2]
    if not package.is_file() or inst.digest(package.read_bytes()) != sha:
        raise RuntimeError("PACKAGE_SHA256_MISMATCH")
    inst.verified_package(package, sha)
    original_run = inst._run

    def observed_run(arguments, *, timeout=180):
        if "-m" in arguments and "venv" in arguments:
            result["stage"] = "CREATE_INSTALLED_VENV"
        elif "-m" in arguments and "pip" in arguments:
            result["stage"] = "OFFLINE_WHEEL_INSTALL"
        elif "-I" in arguments:
            result["stage"] = "INSTALLED_MODULE_PROOF"
        else:
            result["stage"] = "INSTALL_SUBPROCESS"
        proc = subprocess.run(
            arguments, capture_output=True, text=True, errors="replace",
            timeout=timeout,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if proc.returncode:
            result["subprocess_exit"] = proc.returncode
            result["stderr_class"] = classify(proc.stderr)
            raise RuntimeError("SUBPROCESS_FAILED")
        return proc

    inst._run = observed_run
    result["stage"] = "INSTALL_DISPOSABLE"
    receipt = inst.install(package, sha, root=expected_root)
    result.update(status="PASS", stage="INSTALLED_DISPOSABLE",
                  installed_status=receipt.get("status"),
                  installed_pointer_present=(expected_root / "current.json").is_file())
except BaseException as exc:
    result.update(status="FAIL", exception=type(exc).__name__,
                  exception_classification=scrub(str(exc)))
finally:
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
'''

def main() -> int:
    if sys.platform != "win32":
        print("STOP: Windows only")
        return 2
    if not BUILD_PYTHON.is_file() or not PACKAGE.is_file():
        print("STOP: Core006 disposable build assets missing; no install attempted")
        return 2
    current_head = subprocess.run(
        ["git", "-C", str(WORKTREE), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if current_head != SOURCE_HEAD:
        print("STOP: Source HEAD changed; no install attempted")
        return 2
    if hashlib.sha256(PACKAGE.read_bytes()).hexdigest() != EXPECTED_PACKAGE_SHA256:
        print("STOP: Package hash mismatch; no install attempted")
        return 2

    real_root = (Path.home() / "AppData" / "Local" / "FOX2" / "AgentBridge").resolve()
    with tempfile.TemporaryDirectory(prefix="fox2-install-probe-", dir=r"C:\Temp") as td:
        scratch = Path(td)
        profile = scratch / "user"
        expected = profile / "AppData" / "Local" / "FOX2" / "AgentBridge"
        local = expected.resolve()
        if real_root == local or local.is_relative_to(real_root) or real_root.is_relative_to(local):
            print("STOP: Test profile overlaps real Bridge; no install attempted")
            return 2
        (profile / "AppData" / "Local").mkdir(parents=True)
        (profile / "AppData" / "Roaming").mkdir(parents=True)
        (scratch / "tmp").mkdir()
        env = dict(os.environ)
        env.update(
            USERPROFILE=str(profile), HOME=str(profile),
            LOCALAPPDATA=str(profile / "AppData" / "Local"),
            APPDATA=str(profile / "AppData" / "Roaming"),
            TEMP=str(scratch / "tmp"), TMP=str(scratch / "tmp"),
            PYTHONPATH=str(WORKTREE / "agent_bridge" / "src"),
            PYTHONDONTWRITEBYTECODE="1",
        )
        proc = subprocess.run(
            [str(BUILD_PYTHON), "-c", CHILD, str(PACKAGE),
             EXPECTED_PACKAGE_SHA256, str(expected)],
            env=env, cwd=str(WORKTREE), capture_output=True, text=True,
            errors="replace", timeout=300,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        try:
            report = json.loads(proc.stdout.strip().splitlines()[-1])
        except (IndexError, ValueError):
            report = {"status": "FAIL", "stage": "CHILD_BOOTSTRAP",
                      "exit": proc.returncode,
                      "stderr_class": "CHILD_FAILED_BEFORE_JSON"}
        report["real_runtime_touched"] = False
        report["dispatch_executed"] = False
        report["uninstall_invoked"] = False
        report["disposable_only"] = True
        print(json.dumps(report, indent=2, ensure_ascii=True, sort_keys=True))
        return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
