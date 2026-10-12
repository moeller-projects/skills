# Rule: OpenSpec Output Format

> Impact: high

## Description

When `output_format=openspec`, serialize the existing spec into an OpenSpec-compatible proposal directory without rewriting requirement intent.

## Apply When

- The user requests OpenSpec output.

## Checks

- Output declares `output_format: openspec`.
- Output declares an OpenSpec proposal directory with `proposal.md`, `.openspec.yaml`, and one or more `specs/<capability>/spec.md` delta files.
- `proposal.md` includes: `## Why`, `## What Changes`, `## Capabilities`, `## Impact`.
- Delta specs use OpenSpec section headers: `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements`, or `## RENAMED Requirements`.
- Every ADDED/MODIFIED requirement uses `### Requirement:` and includes at least one `#### Scenario:` block.
- Use `.openspec.yaml` metadata (`schema`, `created`) and do not emit `change.yaml` for OpenSpec v1.3.1.

## Anti-Pattern

Copying requirements into an OpenSpec folder shape that omits delta headers, scenario blocks, or proposal sections, which breaks OpenSpec validation and archive behavior.
