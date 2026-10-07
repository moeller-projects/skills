# ADO Gateway

Version: 5.0.1

Read Azure DevOps work items and pull request discussions, normalize them, and perform a small approved set of write actions through deterministic dry-run-first Python scripts.

## Includes

- Read-only Azure DevOps work item retrieval
- Azure DevOps PR URL parsing, PR branch/work-item enrichment, and PR comment flattening
- Normalized handoff contract for `spec-engine`
- Guarded writes for work items, comments, PRs, and PR comments
- Dry-run JSON action plans before any mutation
- Explicit `--confirm` gate for every write

## Read flow

Set `AZURE_DEVOPS_PAT` in the environment using your platform's shell, then run:

```text
python scripts/generate-handoff.py --pull-request-url https://dev.azure.com/example-org/example-project/_git/example-repo/pullrequest/123 --work-item-id 456
```

## Write flow: dry run first

```text
python scripts/create-work-item.py --organization example-org --project example-project --type Bug --title "Checkout fails for invalid coupon" --description "Observed during checkout validation."
```

Review the JSON plan. Add `--confirm` only when the write is explicitly approved. Python 3.9+; standard library only.
