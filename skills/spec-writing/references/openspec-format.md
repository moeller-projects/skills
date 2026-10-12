# OpenSpec Format Reference

## Source of Truth

- Upstream project: `Fission-AI/OpenSpec`
- Stable version referenced: `v1.3.1`
- Annotated tag object SHA: `c95caf063c834b9c1d3bfb59bd94911d7c44c92b`
- Tagged commit SHA (stable source snapshot): `3c7a05c5dc88b2397c478805890b55ed392b19e8`

## Proposal Directory Layout

OpenSpec proposal changes are active under:

```text
openspec/changes/<change-name>/
├── .openspec.yaml
├── proposal.md
├── design.md            # optional depending on complexity
├── tasks.md             # required for apply workflow
└── specs/
    └── <capability>/
        └── spec.md      # delta spec
```

Archived proposals move to:

```text
openspec/changes/archive/YYYY-MM-DD-<change-name>/
```

## Proposal Content Requirements

`proposal.md` sections for spec-driven workflow:

- `## Why`
- `## What Changes`
- `## Capabilities`
- `## Impact`

## Delta Syntax

Delta spec files (`specs/<capability>/spec.md`) use section headers:

- `## ADDED Requirements`
- `## MODIFIED Requirements`
- `## REMOVED Requirements`
- `## RENAMED Requirements`

Requirement/scenario structure:

- Requirement header: `### Requirement: <name>`
- Scenario header: `#### Scenario: <name>`
- ADDED/MODIFIED entries must include SHALL or MUST language and at least one scenario.
- REMOVED entries may be requirement headers or bullet references to requirement headers.
- RENAMED entries use paired lines:
  - `FROM: ### Requirement: <old-name>`
  - `TO: ### Requirement: <new-name>`

## Change Metadata (`.openspec.yaml`)

For OpenSpec v1.3.1, the per-change metadata file is `.openspec.yaml` with keys:

- `schema` (for example `spec-driven`)
- `created` (`YYYY-MM-DD`)

`change.yaml` is not used by the v1.3.1 spec-driven workflow.

## Lifecycle States

- **Active:** Proposal folder exists under `openspec/changes/<change-name>/`
- **Archived:** Proposal folder moved to `openspec/changes/archive/YYYY-MM-DD-<change-name>/`
- **Artifact status model (CLI):** `done`, `ready`, or `blocked` per artifact during active lifecycle.

## Linter / Validation Rules (Relevant to Serialization)

OpenSpec `validate` checks (change/spec):

- Change deltas must exist in `specs/<capability>/spec.md` under recognized delta headers.
- ADDED/MODIFIED requirements require SHALL/MUST and at least one `#### Scenario:`.
- Duplicate or conflicting requirement operations are rejected.
- Main specs require `## Purpose` and `## Requirements`.
- Missing delta sections or empty parsed sections are validation errors.
