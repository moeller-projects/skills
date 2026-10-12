# Rule: Scope Guard

> Impact: high

## Description

Keep the review inside the changeset's blast radius. Pre-existing issues and adjacent refactor ideas belong under out-of-scope.

## Apply When

- Any review where the diff touches code with pre-existing problems.

## Checks

- Findings cover only lines the author changed.
- Pre-existing issues observed in touched files are listed under out-of-scope with a one-line reason.
- Suggested follow-up work is named, not silently added to the author's plate.

## Anti-Pattern

Blocking a small fix because the surrounding module has years of debt the author did not create.
