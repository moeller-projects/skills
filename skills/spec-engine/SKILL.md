---
name: spec-engine
description: Use when turning ambiguous requests, tickets, research, or normalized ado-gateway handoffs into an implementation-ready spec or OpenSpec proposal. Do not use when the task is pure code implementation or governance review with no new spec-authoring step.
allowed-tools:
  - read_file
title: Spec Engine
version: 1.0.1
summary: Turn requests or ado-gateway handoffs into structured, version-aware specs with risk tiers, acceptance criteria, policy gates, and optional OpenSpec proposal output.
---

# Spec Engine

## Purpose

Extract requirements, create structured specs, validate requirement quality, manage spec diffs, enforce versioning, and produce implementation-ready artifacts.

## Use When

- Creating a freeform implementation-ready spec from user input, tickets, or research.
- Consuming a normalized ado-gateway handoff JSON to generate a spec from Azure DevOps work item data.
- Emitting an OpenSpec proposal from a spec produced by this skill or a prior session.
- Validating requirement quality or acceptance criteria.
- Diffing or versioning spec changes.
- Enforcing policy or governance around requirements.
- Producing implementation-ready artifacts from ambiguous requests.

## Avoid When

- The user only wants code.
- The task has no requirement or spec component.
- The task is validating, scoring, or diffing an existing spec file with no new authoring step.
- The task is pure OpenSpec governance with no spec-authoring step.

## Workflow

1. Convert goals, constraints, and context into explicit scope; if goals conflict, surface the conflict as an open question.
2. Write requirements and acceptance criteria that are testable. Every acceptance criterion is expressed in GIVEN/WHEN/THEN form per `rules/acceptance-criteria.md`.
3. Check for ambiguity, missing decisions, and policy gaps.
4. Assign a risk tier (Low / Medium / High / Critical) based on the scope of change: Low for internal clarification, Medium for additive features, High for cross-module behavior, Critical for public API or security posture changes. If the tier cannot be determined from available context, list it as an open question.
5. Capture diffs or version changes when the spec evolves.
6. Deliver the spec with gates and open questions.
7. Serialize to output_format. If output_format=openspec, emit the spec as an OpenSpec proposal directory per the rules in `rules/openspec-format.md`. Default output_format is freeform.

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
  delta_spec_files:
  - specs/<capability>/spec.md
  required_apply_files:
  - tasks.md
  optional_files:
  - design.md
```

## Handoffs

- Accept normalized `ado-gateway` handoff JSON when Azure DevOps context must be converted into a spec or OpenSpec proposal.
- Hand off to `delivery-engine` when the spec is stable and the next output must be an executable task breakdown with dependencies and done criteria.

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

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — password reset spec scenario
- `assets/examples/edge-case.md` — conflicting requirements scenario
- `scripts/validate-output.py` — validates output structure

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/artifact-schema.md` for the output schema.
- See `references/openspec-format.md` for OpenSpec serialization rules and source version pin.
- See `references/examples.md` for sample specs.

## Rules

- `rules/_sections.md`
- `rules/requirement-quality.md`
- `rules/acceptance-criteria.md`
- `rules/diff-versioning.md`
- `rules/policy-gates.md`
- `rules/handoff-consumption.md`
- `rules/openspec-format.md`
