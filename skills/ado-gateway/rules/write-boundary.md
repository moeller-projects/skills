# Rule: Write Boundary

> Impact: critical

## Description

Write-mode support is limited to a fixed set of dry-run-first Azure DevOps creation scripts with explicit confirmation gates and least-privilege scope handling.

## Apply When

- Implementing, extending, or reviewing any write-mode behavior in `ado-gateway`.

## Checks

- Supported write behavior stays limited to `scripts/create-work-item.py`, `scripts/create-work-item-comment.py`, `scripts/create-pull-request.py`, and `scripts/create-pr-comment.py`.
- Write scripts default to dry-run and require explicit confirmation before execution.
- Dry-runs emit a JSON action plan before any mutation.
- Scripts use fixed Azure DevOps endpoint templates only.
- Scripts do not accept arbitrary URLs, arbitrary HTTP methods, DELETE, or PR vote/merge/abandon operations.
- Scripts never echo PATs and require least-privilege PAT scopes.

## Anti-Pattern

Introducing a generic write client or broad mutation command that can hit arbitrary Azure DevOps endpoints.
