# Git Workflow — Output Template

```text
context:
- goal: <one logical change and desired end state>
- publication: private | shared | published | unknown
- collaborators: <people, branches, or PRs affected>

branch_strategy:
- branch: <lowercase/type/name>
- parent_or_base: <branch or commit>
- choice: rebase | merge | revert | no-history-rewrite
- rationale: <why this fits ownership and publication status>

commit_plan:
- commit: <atomic change>
  message: <type(scope): imperative description>
  breaking_footer: <BREAKING CHANGE: ... | none>

operations:
- id: O-01
  command: git status --short && git diff --cached
  rationale: <what this establishes or changes>
  risk: safe | cautious | destructive
  confirmation: not_required | REQUIRED: <what user must confirm before execution>
  blast_radius: <files, commits, branches, or collaborators affected>
  rollback: <exact rollback command, or not_applicable for safe read-only work>

safety_notes:
- <shared-history, secret, conflict, or force-push warning>

rollback:
- checkpoint: <rescue branch, tag, reflog entry, or remote ref>
- command: <exact recovery command>
- limits: <what cannot be recovered automatically>
```

Rules:
- Keep operations ordered and use exact commands, not prose placeholders.
- Any command containing `reset --hard`, `rebase`, or `push --force` is destructive for this contract and MUST include `confirmation`, `blast_radius`, and an exact `rollback` command.
- For published history, use `git revert <commit>` instead of reset; never force-push a shared branch.
- A safe read-only command may use `rollback: not_applicable`; cautious commands still need a rollback or explain why no state changes occur.
