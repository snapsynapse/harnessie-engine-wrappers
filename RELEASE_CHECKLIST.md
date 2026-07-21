# Release checklist

## Verify

- [ ] `python -m pytest -q` passes.
- [ ] `harnessie-engine-wrapper-probe` passes on macOS.
- [ ] Unsupported-platform refusal is verified on Linux CI.
- [ ] Direct and symlink bypass probes emit no canary bytes.
- [ ] Legitimate unrelated reads still succeed.
- [ ] `git diff --check` passes.

## Release

- [ ] Version matches package, changelog, probe contract, and release notes.
- [ ] CI passes on the release commit.
- [ ] Annotated tag is pushed.
- [ ] Source archive digest is recorded.
- [ ] GitHub Release exists and is marked latest.
