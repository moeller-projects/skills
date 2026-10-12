# Rule: Correctness First

> Impact: critical

## Description

Prioritize bugs, undefined behavior, data loss, and security-adjacent defects before style or aesthetic cleanup.

## Apply When

- Reviewing or refactoring production code.

## Checks

- High-risk correctness issues MUST appear before readability suggestions.
- Proposed fixes MUST preserve intended behavior.

## Anti-Pattern

Focusing on naming or formatting while real defects remain unresolved.
