# Edge-Case Example — Published Branch

## Scenario

A shared `main` branch contains a bad commit and another team is working from it.

## Expected Decision

Do not use `git reset --hard` or `git push --force`. Create a new commit with `git revert <bad-commit>`, review the revert diff, and push normally. If the bad commit includes secrets, stop and hand off to the security or incident process rather than relying on Git history cleanup alone.
