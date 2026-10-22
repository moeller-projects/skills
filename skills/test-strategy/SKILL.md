---
name: test-strategy
description: Plan resilient unit, integration, E2E, and flake-reduction test coverage: select levels, cases, and risk remedies. Use when planning coverage or making test-quality decisions; route requests to implement behavior with tests, including regression-test fixes, to `test-driven-development`. Do not use for writing tests or implementing behavior, broader code review or refactoring quality work, or documentation-only tasks.
allowed-tools: read_file
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Test Strategy
  version: "1.0.6"
  summary: Plan resilient test coverage by selecting levels, cases, and flake-risk remedies; route test writing and behavior implementation to test-driven-development.
---

# Test Strategy

## Purpose

Plan and improve test strategy, coverage, edge-case validation, test levels, and E2E stability without implementing the behavior under test.


## Workflow

1. MUST map the behavior, risk, and test boundaries that matter; if behavior is ambiguous, ask one question before finalizing the plan.
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
- case: <acceptance-criterion case>
  given: <precondition>
  when: <action>
  then: <observable outcome>
  level: unit|integration|e2e
  priority: critical|high|medium|low

risk:
- ...
```

## Handoffs

- Accepts work from `codebase-onboarding` once the test surface to cover is identified.
- Accepts work from `code-review` when code changes require new or updated test coverage.
- Accepts work from `spec-writing` when acceptance criteria need test-case translation; `spec-writing` owns criteria authoring.

## Error Handling

1. Local: If target behavior is unclear, clarify or revise the test plan before drafting cases.
2. Flow: If the test environment is unavailable, defer E2E tests in the plan and note the coverage gap explicitly.
3. Recovery: If proposed tests expose an unexpected failure, revise the plan and its assumptions; do not revert the stable test suite as a planning response.

## Validation Checklist

- [ ] Happy-path, failure, and edge-case cases all present.
- [ ] E2E tests deferred with explicit re-enable condition if environment unavailable.
- [ ] Coverage gaps listed explicitly.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — read when formatting the final test-plan artifact.
- `assets/examples/happy-path.md` — read when a concrete happy-path test-plan example is needed.
- `assets/examples/edge-case.md` — read when documenting an unavailable E2E environment scenario.
- `scripts/validate-output.py` — run when validating the output contract, only with explicit test execution authorization.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to validate the skill output.
- `tests/validation-checklist.md` — read when reviewing the skill's validation requirements.

## References

- See `references/examples.md` when sample test plans are needed.

## Rules

- `rules/behavior-over-implementation.md` — read when choosing behavior-level assertions over implementation details.
- `rules/meaningful-coverage.md` — read when assessing whether coverage is meaningful.
- `rules/edge-cases.md` — read when identifying boundary and invalid-input cases.
- `rules/e2e-stability.md` — read when designing or reviewing E2E stability.
- `rules/flaky-test-reduction.md` — read when diagnosing or reducing flaky tests.
