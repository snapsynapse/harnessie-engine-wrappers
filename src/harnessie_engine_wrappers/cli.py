"""Command-line reference wrapper with fail-closed platform handling."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

from .policy import DEFAULT_CREDENTIAL_PATHS, UnsafePolicy, load_policy_file, normalize_paths
from .seatbelt import BackendUnavailable, profile_for, run


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="harnessie-engine-wrapper",
        description="Run a command with probeable credential-read denials.",
    )
    p.add_argument("--deny", action="append", default=[], metavar="PATH")
    p.add_argument("--policy-file", type=Path)
    p.add_argument("--print-profile", action="store_true")
    p.add_argument("command", nargs=argparse.REMAINDER)
    return p


def _refusal(error: str, detail: str, why: str) -> str:
    return json.dumps({"error": error, "detail": detail, "why": why}, sort_keys=True)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    raw_paths = list(DEFAULT_CREDENTIAL_PATHS)
    if args.policy_file:
        raw_paths.extend(load_policy_file(args.policy_file))
    raw_paths.extend(args.deny)
    try:
        deny_paths = normalize_paths(raw_paths)
    except (OSError, UnsafePolicy) as exc:
        print(_refusal("invalid_policy", str(exc), "an ambiguous deny boundary cannot be enforced"), file=sys.stderr)
        return 64

    if platform.system() != "Darwin":
        print(_refusal(
            "platform_unsupported",
            f"no admitted backend for {platform.system()}",
            "the 0.1 reference wrapper ships only after its local probe can verify macOS Seatbelt",
        ), file=sys.stderr)
        return 69

    if args.print_profile:
        sys.stdout.write(profile_for(deny_paths))
        return 0

    command = list(args.command)
    if command and command[0] == "--":
        command.pop(0)
    if not command:
        parser().error("a command is required after --")
    try:
        result = run(command, deny_paths, env=os.environ)
    except BackendUnavailable as exc:
        print(_refusal("backend_unavailable", str(exc), "running without verified containment would violate the wrapper contract"), file=sys.stderr)
        return 70
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
