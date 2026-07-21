# Probe contract

Version: 0.1.0
Date: 2026-07-21

## Admission rule

A wrapper is admitted on a machine only when its local probe exits zero and every named check is true. Cached, copied, remote, or self-reported results do not admit another machine. A backend change, operating-system update, policy change, or wrapper change requires a new probe.

## macOS Seatbelt reference contract

The 0.1 probe verifies three decidable properties against a fresh random temporary tree:

1. A direct read beneath a declared credential root fails and emits no canary bytes.
2. A read through a symlink resolving beneath that credential root fails and emits no canary bytes.
3. A read outside the denied roots succeeds unchanged.

The wrapper fails closed before launching the child when the platform is not macOS, `sandbox-exec` is unavailable, the policy is empty, or a deny path is ambiguous or dangerously broad.

## Not claimed

The probe does not establish network denial, write denial, process isolation, Keychain API denial, clipboard isolation, screen isolation, kernel resistance, or protection from a compromised parent process. The Seatbelt profile uses default allow and adds credential-file read denials. Those residuals are product boundaries, not implied features.
