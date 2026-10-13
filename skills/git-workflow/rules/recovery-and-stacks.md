# Rule: Recovery and Stacks

> Impact: high

## Description

Make interrupted operations and dependent branch updates reversible, observable, and ordered.

## Apply When

- Resolving conflicts, recovering lost commits, or updating stacked/dependent PRs.

## Checks

- Conflict plans preserve work and include `git status`, resolution, `git add`, and `git rebase --continue` or merge continuation.
- Abort paths use the matching `git rebase --abort` or `git merge --abort` command.
- Reflog recovery identifies the lost tip and creates a rescue branch before further cleanup.
- Stacks are rebased bottom-up, and each child PR is retargeted or force-pushed only when its branch is private and authorized.
- Stack operations performed with the `gh stack` CLI extension are handed off to the `gh-stack` skill rather than planned as raw git commands.

## Anti-Pattern

Resolving conflicts by deleting files, recovering by guessing a commit hash, or force-pushing every branch in a stack indiscriminately.
