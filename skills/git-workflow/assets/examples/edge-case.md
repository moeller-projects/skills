# Edge-Case Example — Published Branch

## Scenario

A shared `main` branch contains a bad commit and another team is working from it.

## Expected Decision

Because other teams use this branch, preserve shared history: create a new commit with `git revert <bad-commit>`, review the revert diff, and push normally. If the bad commit includes secrets, stop and hand off to the security or incident process rather than relying on Git history cleanup alone.

## Rescue Reference Lifecycle

Before any authorized local rewrite, create and record a rescue reference:

```bash
git branch rescue/<topic>-before-rewrite HEAD
git reflog show <topic>
```

Keep that reference until the rewritten result is verified and the user confirms cleanup. Only then may the exact rescue reference be deleted:

```bash
git branch -d rescue/<topic>-before-rewrite
```

Never use `-D` as a shortcut, delete the only rescue reference, or remove it before verification. If cleanup is blocked or the result is wrong, preserve the reference and recover with `git reset --hard rescue/<topic>-before-rewrite` only on the private branch after confirmation; published/shared branches still require `git revert`.
