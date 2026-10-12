# Rule: Standard Sections

> Impact: medium

## Description

Organize the output into spec, quality gates, and open questions so the result is easy to review and implement.

## Apply When

- Drafting or validating a specification.

## Checks

- Goals, scope, requirements, and acceptance criteria are all present.
- Open questions are separated from confirmed requirements.
- `risk_tier` is present and set to one of: Low, Medium, High, Critical.

## Anti-Pattern

Mixing assumptions and requirements together so no one knows what is approved. Emitting a spec with no risk classification, forcing the reader to infer risk from content.
