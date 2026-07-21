"""Executable confinement probe for the macOS reference wrapper."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

from .seatbelt import admitted


def _invoke(deny: Path, program: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "harnessie_engine_wrappers.cli",
            "--deny",
            str(deny),
            "--",
            sys.executable,
            "-c",
            program,
        ],
        text=True,
        capture_output=True,
        check=False,
        env=os.environ,
    )


def run_probe() -> dict[str, object]:
    if platform.system() != "Darwin":
        return {
            "ok": False,
            "backend": None,
            "error": "platform_unsupported",
            "detail": f"no admitted probe backend for {platform.system()}",
        }
    backend_ok, backend_detail = admitted()
    if not backend_ok:
        return {
            "ok": False,
            "backend": "macos-seatbelt",
            "error": "backend_unavailable",
            "detail": backend_detail,
        }

    with tempfile.TemporaryDirectory(prefix="harnessie-wrapper-probe-") as raw:
        root = Path(raw)
        denied = root / "credentials"
        denied.mkdir()
        canary = "HEW_CANARY_7PM2K"
        secret = denied / "token.txt"
        secret.write_text(canary, encoding="utf-8")
        visible = root / "visible.txt"
        visible.write_text("visible", encoding="utf-8")
        link = root / "credential-link"
        link.symlink_to(secret)

        direct = _invoke(denied, f"from pathlib import Path; print(Path({str(secret)!r}).read_text())")
        symlink = _invoke(denied, f"from pathlib import Path; print(Path({str(link)!r}).read_text())")
        allowed = _invoke(denied, f"from pathlib import Path; print(Path({str(visible)!r}).read_text())")

        checks = {
            "direct_read_denied": direct.returncode != 0 and canary not in direct.stdout + direct.stderr,
            "symlink_read_denied": symlink.returncode != 0 and canary not in symlink.stdout + symlink.stderr,
            "unrelated_read_allowed": allowed.returncode == 0 and allowed.stdout.strip() == "visible",
        }
        return {
            "ok": all(checks.values()),
            "backend": "macos-seatbelt",
            "checks": checks,
            "return_codes": {
                "direct": direct.returncode,
                "symlink": symlink.returncode,
                "allowed": allowed.returncode,
            },
            "residual": "This probe covers credential-file reads only; it does not claim network, write, process, keychain API, or screen containment.",
        }


def main() -> int:
    result = run_probe()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
