# Rule: Verdict Discipline

> Impact: critical

## Description

Issue exactly one verdict, and make it consistent with the findings. An approve with open blockers is a broken review.

## Apply When

- Closing any review.

## Checks

- `approve` requires zero blocker and zero major findings.
- `request-changes` requires at least one blocker or major finding.
- `comment` is for informational reviews where merge readiness is not being asserted.
- Re-reviews check prior findings first and close them explicitly.

## Anti-Pattern

Approving "with comments" that actually contain blocking defects, leaving the author to guess whether merge is safe.
