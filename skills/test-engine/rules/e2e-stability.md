# Rule: E2E Stability

> Impact: high

## Description

Keep end-to-end and Playwright tests deterministic by using stable selectors, explicit waits, isolated data, and robust environment control.

## Apply When

- Recommending or reviewing browser or workflow automation.

## Checks

- Prefer user-facing, stable selectors and deterministic setup.
- MUST remove timing assumptions and shared mutable state.

## Anti-Pattern

Relying on sleeps, fragile selectors, or test order dependencies that create flakiness.
