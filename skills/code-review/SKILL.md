---
name: code-review
description: Use when reviewing a whole codebase or subsystem for systemic code quality, security, refactoring, or evidence-backed performance concerns. Inspect application and library code for correctness, maintainability, injection flaws, authorization gaps, secrets, unsafe input handling, complexity, legacy modernization, and measured bottlenecks. Do not use for pull request, diff, patch, changeset, or merge-request review or author-facing feedback; use `pr-review` instead. Do not use for test quality or coverage, documentation, or infrastructure or deployment review.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Code Review
  version: "1.2.4"
  summary: Improve correctness, readability, maintainability, performance, and legacy modernization with minimal mutation.
---

# Code Review

## Purpose

Improve code correctness, readability, maintainability, performance, and modernization safety with the smallest reasonable change set.

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
  why: why it matters, grounded in observed behavior or evidence
  fix: exact actionable change

patch-plan:
1. ordered step naming the file/surface and action

risk:
- residual risk, or none
```

Each finding MUST include a precise location, issue, why, and fix. If no supported finding exists, write `- none` rather than inventing one. The patch plan MUST be ordered and substantive even for a clean review (for example, record the checks performed). Risk MUST state residual risk or explicit `none`. A performance concern without profiling, benchmark, or production measurements is an evidence gap and MUST NOT be presented as a severity-ranked defect.

## Handoffs

- Accepts work from `codebase-onboarding` once the code surface to review or refactor is identified.
- Accepts work from `discovery` when analysis resolves into a concrete code quality or security concern.
- Hand off to `test-strategy` when fixes require new or updated test coverage.
- Hand off to `task-planning` when the patch plan needs an executable task breakdown with dependencies and done criteria.
- Consult `codebase-design` for module-shape findings (depth, seams, interfaces) — use its vocabulary in the finding.

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

- `assets/templates/output.md` — read when formatting the review output.
- `assets/examples/happy-path.md` — read for a mixed bug/cleanup review example.
- `assets/examples/edge-case.md` — read when performance is requested without profiling data.
- `scripts/validate-output.py` — run when validating a generated review output.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to validate skill output.
- `tests/validation-checklist.md` — read when checking the skill's validation requirements.

## References

- `references/examples.md` — read for sample findings and patch plans.

## Rules

- `rules/correctness-first.md` — read when assessing correctness.
- `rules/minimal-mutation.md` — read when selecting the smallest safe patch.
- `rules/complexity-reduction.md` — read when evaluating complexity.
- `rules/performance-when-real.md` — read for evidence-based performance concerns.
- `rules/legacy-safety.md` — read when reviewing legacy modernization.
- `rules/injection-safety.md` — read when assessing injection risks.
- `rules/secrets-in-source.md` — read when checking for exposed secrets.
- `rules/authz-checks.md` — read when checking authorization boundaries.
