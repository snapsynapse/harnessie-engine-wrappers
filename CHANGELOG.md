# Changelog

## 0.1.0 - 2026-07-21

### Added

- Fresh-authored macOS Seatbelt reference wrapper with credential-file read denials.
- Shared default credential-path policy with canonicalization and broad-path refusal.
- Executable direct-read, symlink-read, and legitimate-read probe.
- Fail-closed unsupported-platform and missing-backend behavior.
- Backend admission probe so sandbox setup failures cannot masquerade as successful containment.
- macOS and Linux CI, with the live containment probe running on macOS.

### Security

- The release claims credential-file read denial only. Network, writes, processes, Keychain APIs, clipboard, screen, kernel, and parent-process containment are explicit residuals.
