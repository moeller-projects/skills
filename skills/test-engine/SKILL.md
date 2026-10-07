---
name: test-engine
description: Use when designing or improving unit, integration, E2E, or flake-reduction test coverage. Do not use when the request is broader code review or refactoring quality work, or when the task is documentation-only.
allowed-tools:
  - read_file
title: Test Engine
version: 5.0.1
summary: Design resilient test strategies and practical unit, integration, E2E, and Playwright coverage improvements.
---

# Test Engine

## Purpose

Design and improve test strategy, coverage, edge-case validation, unit and integration tests, E2E flows, and Playwright-based automation.

## Use When

- Writing tests for new or changed behavior.
- Reviewing test quality or coverage gaps.
- Designing E2E or Playwright workflows.
- Reducing flaky or brittle tests.
- Improving edge-case validation.

## Avoid When

- The task is pure refactoring without tests.
- The user only wants documentation.

## Workflow

1. MUST map the behavior, risk, and test boundaries that matter; if behavior is ambiguous, ask one question before writing tests.
2. MUST choose the lowest-cost test level that proves the behavior.
3. MUST add meaningful happy-path, edge-case, and failure coverage.
4. MUST keep E2E tests stable by controlling timing, data, and selectors; skip E2E when the test environment is unavailable and note the gap.
5. MUST report gaps, cases, and remaining risk.

## Output Contract

Default:

```text
test-plan:
1. ...

coverage-gaps:
- ...

cases:
- given/when/then

risk:
- ...
```

## Handoffs

- Accepts work from `repo-engine` once the test surface to cover is identified.
- Accepts work from `code-quality-engine` when code changes require new or updated test coverage.
- Accepts work from `spec-engine` when acceptance criteria need test validation.
- Terminal skill — output is the final artifact; no downstream handoff.

## Error Handling

1. Local: If target behavior is unclear, ask one question before writing tests.
2. Flow: Skip E2E tests when the test environment is unavailable; note the coverage gap explicitly.
3. Recovery: Revert to the last stable test suite state if new tests fail unexpectedly.

## Validation Checklist

- [ ] Test levels are the lowest cost that prove the behavior.
- [ ] Happy-path, failure, and edge-case cases all present.
- [ ] Every case follows GIVEN/WHEN/THEN format.
- [ ] E2E tests deferred with explicit re-enable condition if environment unavailable.
- [ ] Coverage gaps listed explicitly.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — discount function test plan
- `assets/examples/edge-case.md` — unavailable E2E environment scenario
- `scripts/validate-output.py` — validates output structure

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/examples.md` for sample test plans.

## Rules

- `rules/_sections.md`
- `rules/behavior-over-implementation.md`
- `rules/meaningful-coverage.md`
- `rules/edge-cases.md`
- `rules/e2e-stability.md`
- `rules/flaky-test-reduction.md`
