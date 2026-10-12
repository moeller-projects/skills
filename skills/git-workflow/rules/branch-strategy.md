# Rule: Branch Strategy

> Impact: high

## Description

Choose branch names and integration strategy from ownership, publication, and dependency facts rather than personal preference.

## Apply When

- Creating feature branches, deciding rebase versus merge, or structuring stacked PRs.

## Checks

- Branch names are lowercase, slash-delimited, and identify intent (for example `feat/auth-reset` or `fix/parser-crash`).
- Rebase is preferred for a private branch needing linear history; merge is preferred when preserving shared topology matters.
- Stacked branches identify their parent, order, and retargeting plan.
- A branch's publication status and expected consumers are explicit.

## Anti-Pattern

Rebasing a branch others consume, or merging a stack without explaining parent PR order and base updates.
