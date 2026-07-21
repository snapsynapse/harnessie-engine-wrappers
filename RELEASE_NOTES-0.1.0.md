# Harnessie Engine Wrappers 0.1.0

Initial probe-gated release approved by Harnessie AIDR-0008.

The release contains a fresh-authored macOS Seatbelt reference wrapper, shared credential-path policy, and an executable probe that attacks direct and symlink-mediated credential reads while proving unrelated reads still work.

Security posture:

- Unsupported platforms and missing backends fail closed before child launch.
- A clean allowed-operation control and backend admission probe prevent sandbox setup failures from masquerading as successful denial.
- Every target machine must earn admission with its own local probe.
- No third-party wrapper code was copied or adapted for the seed.
- CI dependencies are pinned to immutable commits.
- The contract is credential-file reads only. See `SECURITY.md` for residuals.
