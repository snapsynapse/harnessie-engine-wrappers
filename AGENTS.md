# Agent instructions

This repository ships security-impacting operator-side wrappers. Treat every confinement claim as unearned until the local executable probe passes on the target machine.

## Non-negotiable rules

1. Fail closed when a platform, backend, policy, or probe cannot be verified.
2. Add a bypass test and a legitimate-operation control for every security mechanic.
3. Keep claims narrower than the probe. Record residuals in `SECURITY.md`.
4. Never copy or adapt another developer's wrapper code without license compatibility, provenance, and their consenting contribution.
5. Preserve command arguments as an argv list. Do not introduce shell-string execution.
6. A new platform is not supported until CI runs the actual wrapper and live probe on that platform.

## Required checks

```bash
PYTHONPATH=src python3 -m pytest -q
PYTHONPATH=src python3 -m harnessie_engine_wrappers.probe
git diff --check
```

The local probe may honestly return `backend_unavailable` inside a nested sandbox. That is a refusal, not a pass. Release CI must produce a real passing probe on the claimed platform.
