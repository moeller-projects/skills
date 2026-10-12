# OpenSpec Format Reference

## Source of Truth

- Upstream project: `Fission-AI/OpenSpec`
- Stable version referenced: `v1.14.1`
- Tag type: lightweight (no annotated tag object since the v1.3.1 pin)
- Tagged commit SHA (stable source snapshot): `87c3595ace6a2e22957f39ebe5b74c2f2316e0cb`

## Authority and Deferral

- This document is the offline fallback for the stable delta-spec core (directory shape, delta headers, requirement/scenario syntax, validation rules). It is not the authority for schema-specific artifact layout.
- When the `openspec` CLI is available, the CLI is authoritative: run `openspec instructions <artifact-id> --change <name> --json` and use its `template`, `rules`, and `resolvedOutputPath` instead of the hardcoded section lists below. Schemas other than the default `spec-driven` may define different artifacts and sections.
- Do not assume repo-local paths: resolve the change location from `openspec status --change <name> --json` (`planningHome`, `changeRoot`, `artifactPaths`).
- Lifecycle operations (continue, apply, verify, sync, archive) are owned by the official `openspec-*` skills from `Fission-AI/OpenSpec`; this skill only serializes a spec into proposal shape.

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

`proposal.md` sections for the default `spec-driven` schema (fallback when the CLI template is unavailable; other schemas may differ):

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

For the `spec-driven` schema, the per-change metadata file is `.openspec.yaml` with keys:

- `schema` (for example `spec-driven`)
- `created` (`YYYY-MM-DD`)

`change.yaml` is not used by the spec-driven workflow. A change may also declare `skip_specs: true` in `.openspec.yaml`, in which case delta spec files must NOT be created.

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
