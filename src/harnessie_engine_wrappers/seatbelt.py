"""Fresh-authored macOS Seatbelt reference wrapper."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Mapping, Sequence


class BackendUnavailable(RuntimeError):
    """No supported, probeable containment backend is available."""


def admitted() -> tuple[bool, str]:
    """Prove Seatbelt can apply a minimal profile in this process context."""
    backend = shutil.which("sandbox-exec")
    if not backend:
        return False, "sandbox-exec not found"
    check = subprocess.run(
        [backend, "-p", "(version 1)\n(allow default)\n", "/usr/bin/true"],
        text=True,
        capture_output=True,
        check=False,
    )
    if check.returncode != 0:
        detail = (check.stderr or check.stdout).strip()[:300]
        return False, detail or f"admission probe exited {check.returncode}"
    return True, "ok"


def _seatbelt_string(path: Path) -> str:
    return str(path).replace("\\", "\\\\").replace('"', '\\"')


def profile_for(deny_paths: Sequence[Path]) -> str:
    """Build the narrow contract: normal operation except reads under denies."""
    rules = ["(version 1)", "(allow default)"]
    rules.extend(
        f'(deny file-read* (subpath "{_seatbelt_string(path)}"))'
        for path in deny_paths
    )
    return "\n".join(rules) + "\n"


def run(
    command: Sequence[str],
    deny_paths: Sequence[Path],
    *,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command inside the macOS reference policy."""
    backend = shutil.which("sandbox-exec")
    ok, detail = admitted()
    if not backend or not ok:
        raise BackendUnavailable(f"macOS Seatbelt admission probe failed: {detail}")
    if not command:
        raise ValueError("a command is required")
    return subprocess.run(
        [backend, "-p", profile_for(deny_paths), *command],
        env=dict(env) if env is not None else None,
        text=True,
        capture_output=True,
        check=False,
    )
