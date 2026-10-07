# Write Actions

This skill supports a narrow mutation surface for Azure DevOps. It is not a general-purpose REST API writer.

## Safety Model

All write scripts are dry-run by default. A write executes only when `--confirm` is present. Run scripts with Python 3.9+ and the standard library:

```text
python scripts/create-work-item.py --organization example-org --project example-project --type Bug --title "Example dry-run"
```

Dry-run output is a JSON action plan containing the HTTP method, URL, request body, required PAT scopes, and risk metadata.

## Create Work Item

Endpoint: `POST /{organization}/{project}/_apis/wit/workitems/${type}?api-version=7.1` with content type `application/json-patch+json`.

```text
python scripts/create-work-item.py --organization example-org --project example-project --type Bug --title "Checkout fails" --description "Observed during checkout."
```

Optional fields can be supplied as a JSON object with `--fields-json`.

## Create Pull Request

Endpoint: `POST /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests?api-version=7.1` with content type `application/json`.

```text
python scripts/create-pull-request.py --organization example-org --project example-project --repository-id example-repo --source-branch feature/my-change --target-branch main --title "Add checkout validation" --description "Adds validation and tests."
```

Branches are normalized to `refs/heads/<name>` when the prefix is omitted.

## Create Work Item Comment

Endpoint: `POST /{organization}/{project}/_apis/wit/workItems/{workItemId}/comments?api-version=7.1-preview.4` with content type `application/json`.

```text
python scripts/create-work-item-comment.py --organization example-org --project example-project --work-item-id 456 --text "<p>Ready for validation.</p>"
```

Required scopes: Work Items: Read & write; OAuth `vso.work_write`.

## Optional Mention Helpers for Work Item Comments

Mention markup syntax:

```html
<a href="#" data-vss-mention="version:2.0,{userID}">@Name</a>
```

Generate markup from a known work-item mention identity id:

```text
python scripts/format-work-item-mention.py --mention-id 11111111-2222-3333-4444-555555555555 --display-name "Ada Lovelace"
```

Resolve a user by email through Azure DevOps identity lookup:

```text
python scripts/resolve-ado-user.py --organization example-org --email ada@example.com
```

The resolver uses Azure DevOps Identity API (`vssps.dev.azure.com/_apis/identities`) with `AZURE_DEVOPS_PAT`. It resolves `mention_id` from identity `id` (or `originId` fallback). If no user is found or multiple users match, it fails without emitting degraded mention markup.

## Create PR Comment Thread

General thread:

```text
python scripts/create-pr-comment.py --mode thread --organization example-org --project example-project --repository-id example-repo --pull-request-id 123 --content "Please consider extracting this validation."
```

Inline thread:

```text
python scripts/create-pr-comment.py --mode thread --organization example-org --project example-project --repository-id example-repo --pull-request-id 123 --content "This branch needs a null guard." --file-path src/order.ts --side right --line 42
```

Add `--end-line` to anchor across a line range. It must be an integer greater than or equal to `--line`.

`--file-path` must be repository-root-relative (for example, `src/order.ts` or `/src/order.ts`). Filesystem absolute paths and traversal segments are rejected.

## Reply to Existing PR Thread

```text
python scripts/create-pr-comment.py --mode reply --organization example-org --project example-project --repository-id example-repo --pull-request-id 123 --thread-id 99 --content "Fixed in the latest push."
```

## Explicitly Unsupported

- Delete or update work items
- Approve/reject PRs
- Complete, abandon, or merge PRs
- Add reviewers or change branch policies
- Arbitrary REST endpoint execution
