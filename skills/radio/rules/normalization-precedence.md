# Rule: Normalization Precedence

> Impact: high

## Description

Normalization must preserve source fidelity by preferring explicit identifiers, authoritative Azure DevOps fields, and structured missing-data signals over inferred replacements.

## Apply When

- Normalizing Azure DevOps work items, PR comments, anchors, or metadata into the shared handoff contract.

## Checks

- Explicit identifiers win over values parsed from a URL or derived later in the flow.
- Work item acceptance criteria prefer the Microsoft field before any custom fallback field.
- Unknown line anchors stay `null` instead of being coerced to `0`.
- Missing data is surfaced with structured warning lists instead of inline prose.

## Anti-Pattern

Inventing fallback values during normalization that make incomplete Azure DevOps data look authoritative.
