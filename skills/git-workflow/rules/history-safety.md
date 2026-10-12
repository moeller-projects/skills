# Rule: History Safety

> Impact: critical

## Description

Treat reset, rebase of published commits, and force-push as destructive history rewrites requiring confirmation, blast-radius disclosure, and a recoverable reference.

## Apply When

- Rewriting commits, moving branch tips, or undoing published history.

## Checks

- Shared or published branches are never force-pushed without explicit authorization; prefer `git revert`.
- Before destructive work, preserve a rescue branch or capture the current tip and reflog reference.
- Every destructive operation states who is affected, asks for confirmation, and supplies an exact recovery command.
- Abort commands are provided for interrupted merge or rebase states.

## Anti-Pattern

Running `git reset --hard`, `git rebase`, or `git push --force` on an unknown or shared branch with no recovery point.
