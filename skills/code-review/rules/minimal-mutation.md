# Rule: Minimal Mutation

> Impact: high

## Description

Prefer narrow, surgical edits that improve the target concern without rewriting unrelated areas.

## Apply When

- The code is fragile, legacy, or lightly tested.

## Checks

- Each suggested change MUST have a direct link to the stated problem.
- Broad rewrites MUST NOT be done unless the small path is clearly unsafe.

## Anti-Pattern

Using a quality pass as justification for a sweeping rewrite with avoidable risk.
