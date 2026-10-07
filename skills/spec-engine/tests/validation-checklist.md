# Spec Engine — Validation Checklist

Run this checklist before accepting a spec as complete.

## Trigger Check

- [ ] Task involves creating, reviewing, or versioning a spec or requirements.
- [ ] Task is NOT exclusively code implementation with no spec component.

## Requirements Check

- [ ] Every requirement is testable (no "should", "might", "as needed", "where appropriate").
- [ ] Every requirement has a unique identifier (REQ-XX).
- [ ] Conflicting requirements are surfaced as open questions, not silently resolved.

## Acceptance Criteria Check

- [ ] Every AC follows GIVEN/WHEN/THEN format.
- [ ] Every AC references a requirement (REQ-XX).
- [ ] Every AC describes an observable, verifiable outcome.

## Scope Check

- [ ] IN scope is explicit.
- [ ] OUT scope is explicit; nothing is left ambiguous.

## Quality Gates Check

- [ ] Policy or governance checks are listed as executable or verifiable conditions.
- [ ] Security-relevant requirements have an explicit quality gate.

## Open Questions Check

- [ ] Every unresolved decision is listed as OQ-XX with an owner and due date.
- [ ] No open questions are resolved by assumption.

## Error Format

```text
error: <what went wrong during spec creation>
conflict: <the conflicting requirements>
recovery: <action taken — e.g., surfaced as open question OQ-XX>
```

## OpenSpec Output Check (`output_format=openspec`)

- [ ] Output declares `output_format: openspec`.
- [ ] Proposal includes `Why`, `What Changes`, `Capabilities`, and `Impact`.
- [ ] Metadata file is `.openspec.yaml` (not `change.yaml`).
- [ ] Delta specs use OpenSpec headers (`ADDED` / `MODIFIED` / `REMOVED` / `RENAMED` Requirements).
- [ ] ADDED/MODIFIED requirements include at least one `#### Scenario:`.
