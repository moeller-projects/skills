# Rule: Behavior Over Implementation

> Impact: critical

## Description

Prefer tests that verify externally visible behavior and contracts instead of internal implementation details that make tests brittle.

## Apply When

- Designing or reviewing automated tests.

## Checks

- Assertions MUST focus on outputs, state changes, or user-visible results.
- MUST NOT mock or assert internals unless they are the contract.

## Anti-Pattern

Locking tests to private method calls, DOM structure trivia, or incidental sequencing.
