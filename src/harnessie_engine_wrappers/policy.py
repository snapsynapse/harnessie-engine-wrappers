"""Credential-read deny policy shared by wrappers and probes."""

from __future__ import annotations

from pathlib import Path


DEFAULT_CREDENTIAL_PATHS = (
    "~/.aws",
    "~/.azure",
    "~/.config/gcloud",
    "~/.docker/config.json",
    "~/.gnupg",
    "~/.kube",
    "~/.netrc",
    "~/.npmrc",
    "~/.pypirc",
    "~/.ssh",
    "~/Library/Keychains",
)


class UnsafePolicy(ValueError):
    """The requested deny policy is empty, malformed, or dangerously broad."""


def normalize_paths(raw_paths: list[str] | tuple[str, ...]) -> tuple[Path, ...]:
    """Expand and canonicalize deny paths, rejecting ambiguous broad targets."""
    home = Path.home().resolve()
    paths: list[Path] = []
    for raw in raw_paths:
        value = raw.strip()
        if not value or "\n" in value or "\r" in value:
            raise UnsafePolicy("deny paths must be non-empty single lines")
        path = Path(value).expanduser().resolve(strict=False)
        if path == Path(path.anchor) or path == home:
            raise UnsafePolicy(f"refusing dangerously broad deny path: {path}")
        if path not in paths:
            paths.append(path)
    if not paths:
        raise UnsafePolicy("at least one credential deny path is required")
    return tuple(paths)


def load_policy_file(path: Path) -> tuple[str, ...]:
    """Read newline-delimited paths. Blank lines and comments are ignored."""
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)
    return tuple(lines)
