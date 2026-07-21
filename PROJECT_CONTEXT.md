# Project context

## Purpose

Harnessie Engine Wrappers is the separate delivery surface approved by Harnessie AIDR-0008. It packages operator-side engine containment as probe-gated wrappers, independently consumable by any runner.

## Ecosystem relationship

This repository owns wrapper implementation, platform claims, probes, and releases. The federated Harnessie authority map and release relationship live in [Harnessie ECOSYSTEM.md](https://github.com/snapsynapse/harnessie/blob/main/ECOSYSTEM.md). Engine wrappers release independently until Harnessie consumes a versioned verification seam; a Harnessie core release alone does not justify a wrapper version bump.

## Current contract

Version 0.1.0 contains one fresh-authored macOS Seatbelt reference wrapper. Its probe verifies direct credential-file read denial, symlink-mediated read denial, and an unrelated allowed read. Unsupported platforms and missing backends fail closed.

## Boundaries

This is not a general sandbox, policy engine, or claim of complete host containment. Network, writes, processes, Keychain APIs, clipboard, screen, kernel, and parent-process security remain outside the 0.1 contract.

## Contribution posture

Credit ideas generously. Keep intellectual-property boundaries conservative. The initial seed contains no copied or adapted community wrapper code; later work lands only through authors who consent to contribute under Apache-2.0.
