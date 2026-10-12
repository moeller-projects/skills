# Workflow

## Default Flow

1. Establish branch publication, ownership, remote, and stack parent.
2. Inspect status, staged and unstaged diffs, recent log, and likely secrets or generated files.
3. Define atomic commits and Conventional Commit subjects. Use `BREAKING CHANGE:` for incompatible behavior.
4. Pick rebase for private linear cleanup; pick merge when preserving shared topology or published ancestry matters; pick revert to undo published changes.
5. Add a rescue branch before any reset, interactive rebase, or force-push. Require confirmation at the destructive step.
6. Resolve conflicts explicitly, verify the resulting diff, and update stacked branches bottom-up.
7. Publish only after diff hygiene and branch-target checks.

## Decision Gates

- Unknown publication status: block rewriting and ask for confirmation.
- Shared or published branch: do not reset or force-push; use a revert or coordinated merge.
- Child branch in a stack: update parent first, then rebase child onto the new parent and retarget its PR.
- Conflict: preserve the operation state; use the matching abort command if the intended resolution is not clear.

## Recovery

Use `git reflog --date=local` to locate the prior tip, then create `git branch rescue/<name> <hash>` before attempting another repair. For an active rebase use `git rebase --abort`; for an active merge use `git merge --abort`. A rescue branch is a recovery aid, not permission to delete the original reference.
