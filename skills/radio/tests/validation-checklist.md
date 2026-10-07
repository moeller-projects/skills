# Radio — Validation Checklist

## Discovery Validation

- [x] Frontmatter clearly triggers on Azure DevOps work item retrieval, PR comment retrieval, PR URL parsing, and supported write actions.
- [x] Frontmatter clearly rejects destructive writes, PR completion/approval, GitHub review tasks, and OpenSpec authoring.

## Logic Validation

- [x] Workflow distinguishes `work-item`, `pr-comments`, and `work-item-plus-pr-comments`.
- [x] Missing PAT or identifiers produce blocker output.
- [x] PR URL parsing is deterministic and limited to Azure DevOps URL shapes.
- [x] The handoff contract names and field types are stable.
- [x] Write actions are isolated to dedicated scripts.
- [x] Write actions default to dry-run.
- [x] Write execution requires `--confirm`.

## Edge Cases

- [x] Missing `System.Description` results in an empty string plus warning, not a fabricated summary.
- [x] Missing acceptance criteria is reflected in warnings.
- [x] Deleted PR comments remain represented with deletion flags.
- [x] Missing line anchors remain `null`.
- [x] Partial fetches mark `normalization.status: partial`.
- [x] General PR comment threads can be created without inline anchors.
- [x] Inline PR comment threads require a file path and line.

## Validation Evidence

Run:

```text
python skills/radio/tests/run-validation.py
```
