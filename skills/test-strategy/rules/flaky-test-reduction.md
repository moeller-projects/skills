# Rule: Flaky Test Reduction

> Impact: high

## Description

Treat flakiness as a product defect in the test system and reduce it by isolating non-determinism, retries of last resort, and root-cause tracking.

## Apply When

- Existing tests are unreliable or hard to trust.

## Checks

- MUST identify the source of non-determinism before adding retries.
- Prefer deterministic fixtures, cleanup, and synchronization.

## Anti-Pattern

Masking flaky behavior with broad retries while the underlying instability remains.
