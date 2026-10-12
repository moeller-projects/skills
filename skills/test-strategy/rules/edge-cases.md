# Rule: Edge Cases

> Impact: high

## Description

Identify boundary conditions, invalid inputs, race-prone states, and failure paths that are likely to break in production.

## Apply When

- The behavior has constraints, branching, or state transitions.

## Checks

- MUST include at least one meaningful non-happy-path case when risk exists.
- MUST cover boundaries that have historically caused defects.

## Anti-Pattern

Shipping only a happy-path test suite for behavior with obvious failure modes.
