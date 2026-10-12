# Examples

## Conventional Commit

`fix(parser): reject unterminated quoted values`

For an incompatible contract, add a body footer:

`BREAKING CHANGE: malformed quoted values now return a validation error instead of being accepted.`

## Published Undo

Use `git revert <published-commit>` and push the new revert commit. Do not use `git reset --hard` followed by a force-push on a shared branch.

## Conflict Recovery

Inspect with `git status`; resolve only the intended paths; run `git add <paths>`; continue with `git rebase --continue` or finish the merge. If the result is wrong, use `git rebase --abort` or `git merge --abort` before restarting from a rescue point.

## Stacked PRs

Maintain `feat/base`, then `feat/child` based on it. Merge or update the base first, rebase the child onto the new base, retarget the child PR, and publish only a private child branch or an explicitly coordinated update.
