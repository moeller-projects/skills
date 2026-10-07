# Spec Engine — Output Template

## Default (spec + quality_gates + open_questions)

```text
spec:
- goal: <one sentence — the outcome the feature must achieve>
- scope:
  - IN: <what is included>
  - OUT: <what is explicitly excluded>
- requirements:
  - REQ-01: <requirement statement — testable, no ambiguity>
  - REQ-02: <requirement statement>
- acceptance_criteria:
  - AC-01 (REQ-01): GIVEN <precondition> WHEN <action> THEN <observable outcome>
  - AC-02 (REQ-01): GIVEN <precondition> WHEN <action> THEN <observable outcome>

quality_gates:
- [ ] <policy or governance check>

risk_tier: <Low | Medium | High | Critical>

open_questions:
- OQ-01: <question> — owner: <person or team> — due: <date or milestone>
```

## Revision Snapshot (stay on the standard contract)

```text
spec:
- goal: <updated outcome>
- scope:
  - IN: <what remains in scope for this revision>
  - OUT: <what stays out of scope>
- requirements:
  - REQ-01: <updated testable requirement>
- acceptance_criteria:
  - AC-01 (REQ-01): GIVEN <baseline context> WHEN <change is applied> THEN <observable result>

quality_gates:
- [ ] Prior spec version reviewed before applying this revision

risk_tier: <Low | Medium | High | Critical>

open_questions:
- OQ-01: <what still blocks the revision> — owner: <person or team> — due: <date or milestone>
```

## OpenSpec Output (`output_format: openspec`)

```text
output_format: openspec
openspec_proposal:
  path: proposals/
  change_path: openspec/changes/<change-name>/
  metadata_file: .openspec.yaml
  proposal_file: proposal.md
  delta_spec_files:
  - specs/<capability>/spec.md

.openspec.yaml:
  schema: spec-driven
  created: YYYY-MM-DD

proposal.md:
## Why
<why this change is needed>

## What Changes
- <summary of the proposed changes>

## Capabilities
- <capability name>

## Impact
- <affected systems, teams, or tests>

specs/<capability>/spec.md:
## ADDED Requirements
### Requirement: <requirement title>
The system MUST <normative behavior>.

#### Scenario: <scenario name>
- **WHEN** <trigger>
- **THEN** <observable result>
```

## Rules

- Every requirement must be testable: no "should", "might", or "as needed".
- Every acceptance criterion must follow GIVEN/WHEN/THEN format.
- Every conflicting requirement must be surfaced as an open question, not silently resolved.
- Out-of-scope items must be explicit; do not leave scope ambiguous.
- OpenSpec output must keep the authored requirement intent while changing only serialization format.
