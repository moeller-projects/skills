---
name: git-workflow
description: Use when committing changes, choosing a branch or merge strategy, rebasing, resolving merge conflicts, managing stacked or dependent PRs, cleaning history, undoing changes safely, or writing conventional commits. Do not use for reviewing PR content, CI/CD or deployment configuration, or live production incidents; hand those to pr-review, operations, or incident-response.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Git Workflow
  version: "1.0.0"
  summary: Plan safe, disciplined Git history, branching, commit, rebase, recovery, and stacked PR operations.
allowed-tools: read_file
---

# Git Workflow

## Purpose

Produce an executable, safety-first plan for Git history, branches, commits, rebases, merges, conflict recovery, and dependent PRs without executing commands.

## Use When

- Committing changes or designing atomic commit boundaries
- Choosing a branch or merge strategy
- Rebasing, resolving conflicts, or maintaining stacked/dependent PRs
- Cleaning up history or safely undoing local or published changes
- Writing Conventional Commit messages or checking pre-commit hygiene

## Avoid When

- Reviewing PR content or findings — use `pr-review`
- CI/CD pipeline or deployment configuration — use `operations`
- A live production incident — use `incident-response`

## Workflow

1. Inspect repository state, branch publication status, remotes, and collaboration constraints; do not assume a branch is private.
2. Define the logical change and branch/stack topology, then choose atomic commit boundaries and a Conventional Commit message.
3. Select rebase or merge using shared-history and collaboration criteria; document conflict-resolution order for dependent branches.
4. Build ordered operations with exact commands, a risk tier (`safe`, `cautious`, or `destructive`), rationale, and verification checkpoints.
5. For every destructive operation, require explicit user confirmation, state blast radius, and provide a tested-by-inspection recovery command using reflog or a safe remote reference.
6. Review the diff for unrelated files, secrets, generated debris, and accidental history changes before publication.

## Output Contract

Return a plan using `assets/templates/output.md` with:

- `context`, `branch_strategy`, and `commit_plan`.
- An ordered `operations` list where every item has an exact command, rationale, and risk tier.
- `safety_notes` covering destructive commands and shared-branch constraints.
- `rollback` with a recovery path and exact commands.
- Conventional Commit format: `type(scope): imperative description`; breaking changes use a `BREAKING CHANGE:` footer.
- Never force-push a shared branch; prefer `git revert` over reset for published history.

## Handoffs

- Hand off PR content review to `pr-review`.
- Hand off CI/CD, deployment, rollout, or pipeline configuration to `operations`.
- Hand off live production stabilization to `incident-response`.

## Error Handling

- If publication or ownership is unknown, stop before destructive commands and mark the operation blocked pending confirmation.
- If conflicts are unresolved, preserve the in-progress state, record conflicted paths, and give `git rebase --abort` or `git merge --abort` as applicable.
- If a recovery point is unclear, create a non-destructive reference (`git branch rescue/<name> HEAD`) before rewriting history.
- If scope includes PR review, deployment, or incident response, produce only the Git portion and name the handoff.

## Validation Checklist

- [ ] Every operation has an exact command, rationale, and risk tier.
- [ ] Commits are atomic and use valid imperative Conventional Commit subjects.
- [ ] Branch naming and stack dependencies are explicit.
- [ ] Rebase-versus-merge choice cites whether history is shared or published.
- [ ] Diff hygiene checks cover unrelated changes, secrets, generated debris, and staged contents.
- [ ] Every destructive operation has explicit confirmation, blast radius, and an exact rollback/recovery command.
- [ ] Published history is reverted rather than reset; shared branches are never force-pushed.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — use for every Git operation plan.
- `assets/examples/happy-path.md` — use as a complete private-branch rebase and stacked-PR example.
- `assets/examples/edge-case.md` — use when undoing a published/shared change safely.
- `scripts/validate-output.py` — run only when test execution is explicitly authorized to validate output mechanics.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to exercise valid and invalid fixtures.
- `tests/validation-checklist.md` — consult when reviewing contract and safety requirements.

## References

- See `references/workflow.md` for decision flow, safety gates, and recovery patterns.
- See `references/examples.md` for commit, rebase, merge, undo, and stacked-PR examples.

## Rules

- `rules/commit-hygiene.md`
- `rules/history-safety.md`
- `rules/branch-strategy.md`
- `rules/recovery-and-stacks.md`
