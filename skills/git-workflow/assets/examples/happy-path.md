# Happy-Path Example — Private Feature Branch

## Scenario

A developer has a private feature branch with two mixed commits. The branch must become two atomic Conventional Commits before opening a stacked PR.

## Expected Output

```text
context:
- goal: split parser feature and tests into atomic commits before publication
- publication: private
- collaborators: none; child branch depends on feature/parser

branch_strategy:
- branch: feat/parser-tokenizer
- parent_or_base: main
- choice: rebase
- rationale: branch is private, so interactive cleanup gives a linear reviewable history

commit_plan:
- commit: tokenizer implementation
  message: feat(parser): add tokenization for quoted values
  breaking_footer: none
- commit: tokenizer coverage
  message: test(parser): cover quoted-value tokenization
  breaking_footer: none

operations:
- id: O-01
  command: git status --short && git diff && git log --oneline --decorate -5
  rationale: confirm scope, current branch, and unpublished state
  risk: safe
  confirmation: not_required
  blast_radius: none; read-only
  rollback: not_applicable
- id: O-02
  command: git branch rescue/parser-before-rewrite HEAD
  rationale: preserve a named recovery point before rewriting private commits; retain it through verified completion
  risk: cautious
  confirmation: not_required
  blast_radius: creates local rescue reference only
  rollback: preserve rescue/parser-before-rewrite; remove it only as a separately confirmed cleanup after verified recovery
- id: O-03
  command: git rebase -i main
  rationale: reorder and split the two private commits into atomic changes
  risk: destructive
  confirmation: REQUIRED: confirm this branch is private and no collaborator depends on its commit IDs
  blast_radius: rewrites commits reachable from feat/parser-tokenizer after main
  rollback: git reset --hard rescue/parser-before-rewrite
- id: O-04
  command: git diff --check && git diff main...HEAD && git grep -n -I -E '(password|token|secret|api[_-]?key)'
  rationale: inspect whitespace, final diff, and likely secret material before publication
  risk: safe
  confirmation: not_required
  blast_radius: none; read-only
  rollback: not_applicable
- id: O-05
  command: git push -u origin feat/parser-tokenizer
  rationale: publish the cleaned branch for review
  risk: cautious
  confirmation: not_required
  blast_radius: publishes this branch; does not alter shared main
  rollback: git push origin --delete feat/parser-tokenizer

safety_notes:
- Do not force-push if the branch became shared; use a new branch or coordinate explicitly.

rollback:
- checkpoint: rescue/parser-before-rewrite
- command: git reset --hard rescue/parser-before-rewrite
- limits: commits created after the checkpoint must be recovered separately from reflog.
```
