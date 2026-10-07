---
name: code-quality-engine
description: Use when reviewing, refactoring, or modernizing application or library code for correctness, maintainability, security, or evidence-backed performance work. Covers code-level security — injection flaws, authorization gaps, secrets in source, and unsafe handling of untrusted input. Do not use when the request is test quality or coverage review, documentation, or infrastructure work.
allowed-tools:
  - read_file
title: Code Quality Engine
version: 5.0.1
summary: Improve correctness, readability, maintainability, performance, and legacy modernization with minimal mutation.
---

# Code Quality Engine

## Purpose

Improve code correctness, readability, maintainability, performance, and modernization safety with the smallest reasonable change set.

## Use When

- Reviewing code for quality or safety.
- Reviewing application or library code for security defects (injection, authorization gaps, secrets in source, unsafe input handling).
- Refactoring for clarity or maintainability.
- Optimizing performance with real evidence.
- Reducing complexity in fragile areas.
- Modernizing legacy code with minimal mutation.

## Avoid When

- Only documentation is requested.
- Test design is the primary task.
- Infrastructure or deployment is the primary task.

## Workflow

1. MUST confirm current behavior, constraints, and failure risks; if behavior is unclear, ask one question before proceeding.
2. MUST find the highest-value correctness and maintainability issues first.
3. Prefer the smallest safe change; when the change touches critical paths, MUST verify behavior before applying.
4. MUST treat performance work as evidence-driven; skip it when no profiling data exists.
5. MUST present findings, patch order, and residual risk.

## Output Contract

Default:

```text
findings:
- [severity] file:line — issue
  why:
  fix:

patch-plan:
1. ...

risk:
- ...
```

## Handoffs

- Accepts work from `repo-engine` once the code surface to review or refactor is identified.
- Accepts work from `thinking-engine` when analysis resolves into a concrete code quality or security concern.
- Hand off to `test-engine` when fixes require new or updated test coverage.
- Hand off to `delivery-engine` when the patch plan needs an executable task breakdown with dependencies and done criteria.

## Error Handling

1. Local: If evidence for a finding is insufficient, note the gap and move to the next issue.
2. Flow: Skip performance changes when no profiling data exists; abort if the proposed patch surface is unsafe.
3. Recovery: Revert suggestions if applying a patch fails tests or introduces new failures.

## Validation Checklist

- [ ] Findings sorted by severity: critical → high → medium → low.
- [ ] Each finding has file, line, issue, and exact fix.
- [ ] Patch steps are in safe application order.
- [ ] Performance changes included only when profiling data exists.
- [ ] Residual risks listed.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — mixed bug/cleanup scenario
- `assets/examples/edge-case.md` — performance request without profiling data
- `scripts/validate-output.py` — validates output format

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/examples.md` for sample findings and patch plans.

## Rules

- `rules/_sections.md`
- `rules/correctness-first.md`
- `rules/minimal-mutation.md`
- `rules/complexity-reduction.md`
- `rules/performance-when-real.md`
- `rules/legacy-safety.md`
- `rules/injection-safety.md`
- `rules/secrets-in-source.md`
- `rules/authz-checks.md`
