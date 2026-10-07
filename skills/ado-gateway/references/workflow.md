# Workflow

## Read Flow

1. Determine whether the request targets a work item, PR comments, or both.
2. Resolve identifiers from explicit inputs first; parse any PR URL into organization, project, repository, and pull request ID.
3. Require `AZURE_DEVOPS_PAT` for network calls.
4. Fetch Azure DevOps data with GET-only Python scripts, including PR threads, PR branch metadata, and linked work item details when PR context is present.
5. Normalize the work item payload with `scripts/normalize-work-item.py`.
6. Emit the contract with `scripts/emit-handoff.py`, or run the full flow with `scripts/generate-handoff.py`.

Run scripts using Python 3.9+ and its standard library: `python scripts/<name>.py`.

## Write Flow

1. Confirm the user requested one of the supported write actions.
2. Generate dry-run output first.
3. Review the dry-run payload for endpoint, method, request body, and required PAT scope.
4. Execute only with `--confirm`.
5. Return the Azure DevOps response or structured `WRITE_FAILED` error.

## Partial Flow

1. If one read source succeeds and the other source is unavailable, emit `normalization.status: partial`.
2. Record unavailable fields in `normalization.missing_fields`.
3. Do not fabricate missing values.

## Abort Conditions

- Missing PAT or auth env var for network calls
- Malformed PR URL
- Missing work item ID or pull request ID
- Unsupported write action
- Write execution requested without explicit `--confirm`
