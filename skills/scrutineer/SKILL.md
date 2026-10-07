---
name: scrutineer
description: Use when reviewing a pull request, diff, or changeset and producing author-facing review feedback with an approve / request-changes / comment verdict. Do not use when the task is whole-codebase quality or security review (use mechanic), test coverage review (use test-driver), or infrastructure review (use pit-crew).
allowed-tools:
  - read_file
title: Scrutineer
version: 2.0.0
summary: Review pull requests and changesets against the diff, deliver actionable author-facing findings, and issue a clear verdict.
---

# Scrutineer

## Purpose

Review pull requests, diffs, and changesets. Inspect what actually changed, produce author-facing findings that are specific and actionable, and close with a verdict the author can act on.

## Use When

- Reviewing a pull request or merge request.
- Reviewing a diff, patch, or staged changeset before merge.
- Writing review comments for an author.
- Deciding between approve, request-changes, and comment verdicts.
- Re-reviewing a changeset after the author addressed feedback.

## Avoid When

- The task is whole-codebase quality, refactoring, or security review — use `mechanic`.
- The task is test quality or coverage review — use `test-driver`.
- The task is infrastructure or deployment review — use `pit-crew`.
- The task is fetching Azure DevOps PR discussion data — use `radio` for the fetch, then return here for the review.

## Workflow

1. MUST scope the review to the changeset: read the diff first; open surrounding files only to understand the changed lines. If the diff is unavailable or truncated, ask for it before reviewing.
2. MUST verify each finding against the actual code before reporting it; if a finding cannot be confirmed from the available context, mark it as a question, not a defect.
3. MUST sort findings by severity: blocker → major → minor → nit.
4. MUST keep pre-existing, untouched code out of findings; list it under out-of-scope instead.
5. MUST issue exactly one verdict: `approve` only when no blocker or major findings remain; `request-changes` when any blocker or major finding exists; `comment` for informational reviews.
6. MUST state residual risk that remains even if the changeset merges as-is.

## Output Contract

Default:

```text
verdict: approve | request-changes | comment
summary: <one line describing the changeset and overall quality>

findings:
- [blocker|major|minor|nit] path:line — issue
  why:
  suggestion:

out-of-scope:
- ...

risk:
- ...
```

When the changeset is clean, `findings:` contains a single `- none` line instead of fabricated nits.

## Handoffs

- Accepts work from `co-driver` once the changeset to review is identified.
- Accepts GitHub or Azure DevOps pull request review requests routed from `radio`.
- Hand off to `mechanic` when the review surfaces systemic code issues beyond the diff.
- Hand off to `test-driver` when the changeset lacks meaningful coverage for its behavior.
- Terminal skill for the review artifact itself — the verdict and findings are the final output.

## Error Handling

1. Local: If a hunk lacks context to judge, request the surrounding file rather than guessing.
2. Flow: If the diff is too large to review responsibly in one pass, review by commit or by directory and state the split explicitly.
3. Recovery: If the author disputes a finding with evidence, re-verify against the code and either withdraw it with a one-line reason or keep it with the counter-evidence cited.

## Human-in-the-Loop

Request explicit approval before:

- Posting review comments or a verdict to an external system (GitHub, Azure DevOps).
- Approving a changeset that touches authentication, authorization, payments, or data deletion paths.

## Validation Checklist

- [ ] Every finding references a file and line inside the changeset.
- [ ] Findings sorted by severity: blocker → major → minor → nit.
- [ ] Verdict is consistent with the findings (no approve with open blockers).
- [ ] Pre-existing issues live under out-of-scope, not findings.
- [ ] Residual risk is stated.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — feature PR with blocker and nit findings
- `assets/examples/edge-case.md` — oversized diff reviewed in stated passes
- `scripts/validate-output.py` — validates output structure

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/examples.md` for sample reviews.

## Rules

- `rules/_sections.md`
- `rules/diff-first.md`
- `rules/verdict-discipline.md`
- `rules/comment-quality.md`
- `rules/scope-guard.md`
