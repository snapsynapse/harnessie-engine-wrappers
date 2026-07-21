# Harnessie Engine Wrappers

Probe-gated operator-side engine containment. A wrapper is admitted only when its probe verifies the stated confinement contract on the machine where it will run. No passing probe means no run.

This repository is the separate delivery surface approved by [Harnessie AIDR-0008](https://github.com/snapsynapse/harnessie/blob/main/decisions/AIDR-0008-operator-side-engine-wrapper-containment.md). The initial seed is freshly authored. It does not copy or adapt code from community pull requests. Ideas are credited generously; code lands only through its author's consenting contribution.

## What 0.1 contains

- A macOS Seatbelt reference wrapper.
- A shared credential-path deny policy.
- An executable probe for direct reads, symlink-mediated reads, and an unrelated allowed read.
- Fail-closed refusal on unsupported platforms or missing backends.

The 0.1 contract is deliberately narrow: credential-file reads only. It does not claim network, write, process, Keychain API, screen, clipboard, or full-host containment. Linux support is not yet admitted.

## Install for development

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e . pytest
python -m pytest -q
harnessie-engine-wrapper-probe
```

## Run a command

```bash
harnessie-engine-wrapper -- your-engine --its-arguments
```

The default policy denies reads beneath common credential locations including SSH, cloud CLIs, Kubernetes, Docker, package registries, GnuPG, and macOS Keychains. Add a repository-specific path with `--deny PATH` or a newline-delimited file with `--policy-file PATH`.

Run the probe on every target machine before relying on the wrapper:

```bash
harnessie-engine-wrapper-probe
```

Exit `0` means every declared probe passed. Exit `2` means the contract was not earned. The JSON output names each check and the honest residual.

## Security model

Read [SECURITY.md](SECURITY.md) and [PROBE_CONTRACT.md](PROBE_CONTRACT.md) before using the wrapper. The wrapper preserves the child command's exit code. Wrapper refusal codes are `64` for invalid policy, `69` for unsupported platform, and `70` for a missing backend.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). New wrappers need a specific contract, a local executable probe, CI on the claimed platform, bypass tests, legitimate-operation tests, and explicit residuals. A script without a passing probe is an example, not an admitted wrapper.

Apache-2.0. Copyright 2026 Snap Synapse LLC.
