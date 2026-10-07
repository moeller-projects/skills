# Rule: Diff First

> Impact: critical

## Description

Review the changeset, not the codebase. The diff defines the review surface; surrounding files are context, not targets.

## Apply When

- Starting any pull request or changeset review.

## Checks

- Review begins from the diff, not from a repository walk.
- Files outside the diff are opened only to understand changed lines.
- Every reported finding references a line inside the changeset.

## Anti-Pattern

Reviewing the whole file that happens to be touched and reporting pre-existing issues as if the author introduced them.
