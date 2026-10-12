# Rule: Commit Hygiene

> Impact: high

## Description

Keep each commit one logical change, review the staged diff, and use a precise Conventional Commit subject and breaking-change footer when required.

## Apply When

- Creating, splitting, amending, or preparing commits for publication.

## Checks

- `type(scope): imperative description` is used; the subject is concise and has no trailing period.
- One commit has one logical change; unrelated files are split or removed.
- `git diff --cached`, secret scans, and generated/debris checks happen before commit.
- Breaking API or behavior changes include a `BREAKING CHANGE:` footer.

## Anti-Pattern

Committing the entire worktree blindly, mixing refactors with features, or hiding a breaking change in an ordinary subject.
