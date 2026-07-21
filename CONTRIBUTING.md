# Contributing

Contributions are welcome when authors have the right to submit the code under Apache-2.0. Do not copy or adapt code from another project unless its license permits that use and provenance is recorded.

Every new or changed wrapper must include:

1. A bounded, decidable confinement contract.
2. A local executable probe that exercises the actual wrapper and backend.
3. At least one bypass attempt and one legitimate-operation control.
4. CI on every platform the wrapper claims.
5. Fail-closed behavior when the backend or probe is unavailable.
6. Explicit residual risks in `SECURITY.md` and release notes.

Run:

```bash
python -m pip install -e . pytest
python -m pytest -q
harnessie-engine-wrapper-probe
```

Keep changes small. Do not widen a security claim without a probe that earns it.
