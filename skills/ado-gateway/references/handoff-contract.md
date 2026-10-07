# Handoff Contract

`ado-gateway` is the only producer for the Azure DevOps normalization contract.

## Producer Requirements

1. Emit the exact envelope shape from `assets/schemas/ado-openspec-handoff.schema.json`.
2. Set `producer` to `ado-gateway` and `consumer` to `spec-engine`.
3. Set `source.read_only` to `true`.
4. Use `normalization.status = pass` only when required fields for the selected mode are present.
5. Use `partial` when one requested source is unavailable but a usable contract can still be produced.
6. Use `fail` only with matching blocker or error output.

`consumer` should default to `spec-engine`, but the schema remains reusable for other future consumers.

## Required Fields by Mode

- `work-item` → `source.work_item_id`, `work_item.title`, `work_item.description`
- `pr-comments` → `source.pull_request_id`, `pr_comments`, `pull_request.source_branch`, `pull_request.target_branch`
- `work-item-plus-pr-comments` → both sets above

Always include:

- `pull_request` and `linked_work_items` top-level keys.
  - In PR modes, `pull_request` includes PR metadata (including source/target branches) and `linked_work_items` includes linked item details.
  - In non-PR modes, these default to an empty object (`{}`) and empty array (`[]`).
- `work_item.comments` is always an array of normalized records containing `id`, `author`, `content`, `created_date`, and `modified_date`.
- `work_item.history` is an array of update records with `update_id`, `revision`, `revised_by`, `revised_date`, and `changed_fields`; each changed field has a `reference_name` and only the old/new values Azure DevOps supplied.
- `work_item.related_work` is an array of current `System.LinkTypes.Related` links with relation type, target URL, and relation attributes. Other relation types are excluded.
- `pr_comments[*].file_path` normalized to repo-root-relative format starting with `/` when present.

## Identifier Types

- `source.work_item_id` and `work_item.id` are both integer values when known, otherwise `null`.
- `source.pull_request_id` is an integer when known, otherwise `null`.
- Scripts must not emit stringified numeric identifiers in the handoff contract.
