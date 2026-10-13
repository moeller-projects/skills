# Workflow

## Default Flow

1. Establish branch publication, ownership, remote, and stack parent.
2. Inspect status, staged and unstaged diffs, recent log, and likely secrets or generated files.
3. Define atomic commits and Conventional Commit subjects. Use `BREAKING CHANGE:` for incompatible behavior.
4. Pick rebase for private linear cleanup; pick merge when preserving shared topology or published ancestry matters; pick revert to undo published changes.
5. Apply `rules/history-safety.md` before any reset, interactive rebase, or force-push; require confirmation at the destructive step.
6. Resolve conflicts explicitly, verify the resulting diff, and update stacked branches bottom-up.
7. Publish only after diff hygiene and branch-target checks.

## Decision Gates

- Unknown publication status: block rewriting and ask for confirmation.
- Shared or published branch: do not reset or force-push; use a revert or coordinated merge.
- Child branch in a stack: update parent first, then rebase child onto the new parent and retarget its PR.
- Conflict: preserve the operation state; use the matching abort command if the intended resolution is not clear.

## Recovery

For reflog, rescue-branch, and abort-command procedures, follow `rules/history-safety.md` and `rules/recovery-and-stacks.md`.
