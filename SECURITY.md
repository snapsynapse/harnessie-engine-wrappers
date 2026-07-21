# Security policy

## Supported versions

Only the latest tagged release is supported. Version 0.1 is a macOS reference wrapper with the narrow contract in `PROBE_CONTRACT.md`.

## Reporting a vulnerability

Use GitHub private vulnerability reporting for this repository. Do not include real credentials in a report. Use synthetic canaries and include the platform version, wrapper version, policy inputs, probe JSON, and the smallest reproducer.

## Threat model

Attacker goal: an attached engine reads operator credentials from the local filesystem despite a declared deny policy.

Enforcement: the wrapper launches the engine under a macOS Seatbelt profile that denies `file-read*` beneath canonicalized credential roots. The probe attacks direct and symlink-mediated reads and checks that canary bytes do not appear in either output stream.

Fail-closed conditions: unsupported platform, missing backend, empty policy, multiline path, filesystem root, or the entire home directory. These refuse before child launch.

## Residual risks

- `sandbox-exec` is deprecated by Apple and its semantics may change. The per-machine probe is mandatory because CI cannot certify another machine.
- The profile is not a general sandbox. It allows operations not explicitly denied.
- The default deny list cannot enumerate every credential location. Operators must add application-specific paths.
- A parent process, kernel compromise, accessibility permission, Keychain API, screen capture, clipboard access, and network exfiltration are outside the 0.1 contract.
- A command may fail because it legitimately needs a denied credential. That is a safe failure; configure a separate credential specifically for the engine instead of weakening unrelated credential roots.
