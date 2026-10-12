# Rule: OpenSpec Output Format

> Impact: high

## Description

When `output_format=openspec`, serialize the existing spec into an OpenSpec-compatible proposal directory without rewriting requirement intent.

## Apply When

- The user requests OpenSpec output.

## Checks

- Output declares `output_format: openspec`.
- Output declares an OpenSpec proposal directory with `proposal.md`, `.openspec.yaml`, and one or more `specs/<capability>/spec.md` delta files.
- When the `openspec` CLI is available, artifact structure comes from `openspec instructions <artifact-id> --change <name> --json` (`template`, `rules`, `resolvedOutputPath`); the hardcoded checks below are the fallback for the default `spec-driven` schema only.
- `proposal.md` includes: `## Why`, `## What Changes`, `## Capabilities`, `## Impact`.
- Delta specs use OpenSpec section headers: `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements`, or `## RENAMED Requirements`.
- Every ADDED/MODIFIED requirement uses `### Requirement:` and includes at least one `#### Scenario:` block.
- Every ADDED/MODIFIED requirement body MUST include SHALL or MUST normative language.
- Use `.openspec.yaml` metadata (`schema`, `created`) and do not emit `change.yaml`.
- Do not create delta spec files when the change declares `skip_specs: true`.

## Deferral

- Lifecycle operations (continue, apply, verify, sync, archive, validation runs) belong to the official `openspec-*` skills from `Fission-AI/OpenSpec`; hand off instead of reimplementing them here.

## Anti-Pattern

Copying requirements into an OpenSpec folder shape that omits delta headers, scenario blocks, or proposal sections, which breaks OpenSpec validation and archive behavior.
