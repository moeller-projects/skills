# Workflow

## Read Flow

1. Determine whether the request targets a work item, PR comments, or both.
2. Resolve identifiers from explicit inputs first; parse any PR URL into organization, project, repository, and pull request ID.
3. Require `AZURE_DEVOPS_PAT` for network calls.
4. Fetch Azure DevOps work-item comments, paged update history, and current related-work relations with GET-only scripts, alongside PR threads and metadata.
5. Normalize the work item payload, including comments, changed fields per update, and related-work links, with `scripts/normalize-work-item.py`.
6. Emit the contract with `scripts/emit-handoff.py`, or run the full flow with `scripts/generate-handoff.py`.

## Locate a Pull Request from the Current Branch

1. Prefer an explicit pull request URL or ID. Parse a URL with `scripts/parse-pr-url.py`. For an ID, obtain repository identifiers from the current checkout's remote as below, then use the supplied ID without a branch lookup.
2. When no URL or ID is supplied, or an ID needs repository identifiers, select a remote if the checkout has more than one. Pipe its URL directly to `scripts/parse-git-remote.py`; never place the URL in a command argument or print it because it may contain credentials:
   `git remote get-url <remote> | python scripts/parse-git-remote.py`
3. Show the parsed organization, project, and repository and ask the user to approve them before an ADO request. If the remote parser reports an inferred project, state that inference explicitly.
4. Use `git branch --show-current` for the local branch. Empty output means detached HEAD. Do not substitute the upstream branch.
5. Search active PRs with `scripts/find-pull-request.py` using that local branch. Show every candidate. Ask which PR to use if several match; confirm a single inferred candidate before fetching it. If none match, search completed PRs with `--status completed --top 3` for context only, report those results, and ask for a PR URL or ID.
6. For an ID, combine it only with the confirmed organization, project, and repository. Do not infer a PR from the ID alone.

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
