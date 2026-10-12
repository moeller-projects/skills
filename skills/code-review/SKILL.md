---
name: code-review
description: Use when reviewing a whole codebase or subsystem for systemic code quality, security, refactoring, or evidence-backed performance concerns. Inspect application and library code for correctness, maintainability, injection flaws, authorization gaps, secrets, unsafe input handling, complexity, legacy modernization, and measured bottlenecks. Do not use for pull request, diff, patch, changeset, or merge-request review or author-facing feedback; use `pr-review` instead. Do not use for test quality or coverage, documentation, or infrastructure or deployment review.
allowed-tools: read_file
metadata:
  title: Code Review
  version: "1.1.0"
  summary: Improve correctness, readability, maintainability, performance, and legacy modernization with minimal mutation.
---

# Code Review

## Purpose

Improve code correctness, readability, maintainability, performance, and modernization safety with the smallest reasonable change set.

## Use When

- Reviewing a whole codebase or subsystem for systemic code quality or safety issues.
- Reviewing a whole codebase or subsystem for code-level security defects (injection, authorization gaps, secrets in source, unsafe input handling).
- Refactoring a codebase or subsystem for clarity or maintainability.
- Optimizing systemic performance with real evidence.
- Reducing complexity in fragile areas across a codebase or subsystem.
- Modernizing legacy code with minimal mutation.

## Avoid When

- Reviewing a pull request, diff, patch, changeset, or merge request, or writing author-facing review feedback — use `pr-review`.
- Only documentation is requested.
- Test design or coverage is the primary task.
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

- Accepts work from `codebase-onboarding` once the code surface to review or refactor is identified.
- Accepts work from `discovery` when analysis resolves into a concrete code quality or security concern.
- Hand off to `test-strategy` when fixes require new or updated test coverage.
- Hand off to `task-planning` when the patch plan needs an executable task breakdown with dependencies and done criteria.

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
- `tests/run-validation.py` — run only when test execution is explicitly authorized to validate skill output.
- `tests/validation-checklist.md` — consult when reviewing the skill's validation requirements.

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
