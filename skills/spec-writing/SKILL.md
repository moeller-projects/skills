---
name: spec-writing
description: Use when turning ambiguous requests, tickets, research, or normalized azure-devops handoffs into an implementation-ready spec or OpenSpec proposal. Do not use when the task is pure code implementation or governance review with no new spec-authoring step.
metadata:
  title: Spec Writing
  version: "1.1.4"
  summary: Turn requests or azure-devops handoffs into structured, version-aware specs with risk tiers, acceptance criteria, policy gates, and optional OpenSpec proposal output.
---

# Spec Writing

## Purpose

Extract requirements, create structured specs, validate requirement quality while authoring, manage spec diffs while evolving a spec, enforce versioning, and produce implementation-ready artifacts.

## Use When

- Creating a freeform implementation-ready spec from user input, tickets, or research.
- Consuming a normalized azure-devops handoff JSON to generate a spec from Azure DevOps work item data.
- Emitting an OpenSpec proposal from a spec produced by this skill or a prior session.
- Producing implementation-ready artifacts from ambiguous requests.

## Avoid When

- The user only wants code.
- The task has no requirement or spec component.
- The task is validating, scoring, or diffing an existing spec file with no new authoring step.
- The task is pure OpenSpec governance with no spec-authoring step.

## Workflow

1. Capture goals, constraints, and scope, then choose freeform or OpenSpec output.
2. Write testable requirements and GIVEN/WHEN/THEN acceptance criteria.
3. Check ambiguity, policy gaps, risk tier, open questions, and required handoffs.
4. Deliver the spec, preserving prior versions when changing an existing spec.

## Output Contract

Default:

```text
spec:
- goal:
- scope:
- requirements:
- acceptance_criteria:

risk_tier: # Low | Medium | High | Critical

quality_gates:
- ...

open_questions:
- ...
```

When `output_format=openspec`:

```text
output_format: openspec
openspec_proposal:
  path: proposals/
  change_path: openspec/changes/<change-name>/
  metadata_file: .openspec.yaml
  proposal_file: proposal.md
  skip_specs: true # omit delta_spec_files when no capability delta is needed
  delta_spec_files:
  - specs/<capability>/spec.md
  required_apply_files:
  - tasks.md
  optional_files:
  - design.md
```

## Handoffs

- Accept normalized `azure-devops` handoff JSON when Azure DevOps context must be converted into a spec or OpenSpec proposal.
- Hand off to `task-planning` when the spec is stable and the next output must be an executable task breakdown with dependencies and done criteria.
- Hand off OpenSpec lifecycle work (continue, apply, verify, sync, archive) to the official `openspec-*` skills from `Fission-AI/OpenSpec`; this skill only authors the spec and serializes it into proposal shape.

## Error Handling

1. Local: If requirements conflict, surface the conflict as an open question rather than resolving it by assumption.
2. Flow: Skip policy gate checks when no governance rules are defined; note the omission explicitly.
3. Recovery: Preserve the prior spec version as a baseline when diffing or versioning changes.
4. Overwrite: If a spec file with the same name already exists, stop and request explicit approval before overwriting. Present a summary of what will change. Do not silently replace existing content.

## Validation Checklist

- [ ] Every requirement is testable (no "should", "might", "as needed").
- [ ] Every AC follows GIVEN/WHEN/THEN format (see `rules/acceptance-criteria.md`).
- [ ] Conflicting requirements surfaced as open questions, not resolved by assumption.
- [ ] IN and OUT scope are both explicit.
- [ ] Every open question has an owner and due date.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — read when producing the standard output contract.
- `assets/examples/happy-path.md` — read when drafting a password-reset spec.
- `assets/examples/edge-case.md` — read when resolving conflicting requirements.
- `scripts/validate-output.py` — run when validating output structure.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to validate skill output.
- `tests/validation-checklist.md` — read when reviewing validation requirements.

## References

- Read `references/workflow.md` for the detailed workflow after selecting the output mode.
- Read `references/artifact-schema.md` when checking the output schema.
- Read `references/openspec-format.md` when serializing an OpenSpec proposal.
- Read `references/examples.md` when comparing sample specs.

## Rules

- `rules/requirement-quality.md` — read when checking requirement testability.
- `rules/acceptance-criteria.md` — read when writing GIVEN/WHEN/THEN criteria.
- `rules/diff-versioning.md` — read when evolving an existing authored spec.
- `rules/policy-gates.md` — read when governance or policy constraints apply.
- `rules/handoff-consumption.md` — read when consuming normalized handoff data.
- `rules/openspec-format.md` — read when emitting an OpenSpec proposal.
