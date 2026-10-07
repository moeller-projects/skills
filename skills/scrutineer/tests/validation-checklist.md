# Scrutineer — Validation Checklist

Run this checklist before accepting a pull request review as complete.

## Trigger Check

- [ ] Task is reviewing a pull request, diff, patch, or changeset.
- [ ] Task is NOT whole-codebase review (mechanic), test coverage review (test-driver), or infrastructure review (pit-crew).

## Diff Check

- [ ] Review started from the diff, not from a repository walk.
- [ ] Every finding references a file and line inside the changeset.
- [ ] Unverifiable suspicions are phrased as questions, not defects.
- [ ] Oversized diffs were reviewed in explicitly stated passes.

## Findings Check

- [ ] Findings are sorted by severity: blocker → major → minor → nit.
- [ ] Each finding states the issue, why it matters, and a concrete suggestion.
- [ ] Nits are labeled nit and do not influence the verdict.
- [ ] No fabricated nits when the changeset is clean (`- none`).

## Verdict Check

- [ ] Exactly one verdict line is present.
- [ ] `approve` has zero blocker and zero major findings.
- [ ] `request-changes` has at least one blocker or major finding.
- [ ] Re-reviews close prior findings explicitly.

## Scope Check

- [ ] Pre-existing issues live under out-of-scope with a one-line reason.
- [ ] Follow-up work is named explicitly.

## Risk Check

- [ ] Residual risk after merge is stated, including on approve.

## Approval Gate Check

- [ ] External posting of comments or verdicts had explicit user approval.
- [ ] Approvals on auth, payments, or data-deletion paths had explicit user approval.
