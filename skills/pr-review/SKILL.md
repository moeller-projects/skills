---
name: pr-review
description: Use when reviewing a pull request, diff, or changeset and producing author-facing review feedback with an approve / request-changes / comment verdict. Do not use for whole-codebase quality or security review (use `code-review`), test coverage review (use `test-strategy`), infrastructure review (use `operations`), or fetching Azure DevOps PR discussion data (use `azure-devops` for the fetch, then return here for the review).
allowed-tools: read_file
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: PR Review
  version: "2.1.3"
  summary: Review pull requests and changesets against the diff, deliver actionable author-facing findings, and issue a clear verdict.
---

# PR Review

## Purpose

Review pull requests, diffs, and changesets. Inspect what actually changed, produce author-facing findings that are specific and actionable, and close with a verdict the author can act on.


## Workflow

1. MUST scope the review to the changeset: read the diff first; open surrounding files only to understand the changed lines. If the diff is unavailable or truncated, ask for it before reviewing.
2. MUST verify each finding against the actual code before reporting it; if a finding cannot be confirmed from the available context, mark it as a question, not a defect.
3. MUST sort findings by severity: blocker → major → minor → nit.
4. MUST keep pre-existing, untouched code out of findings; list it under out-of-scope instead.
5. MUST issue exactly one verdict: `approve` only when no blocker or major findings remain; `request-changes` whenever any blocker or major finding exists; `comment` only for informational reviews with no blocker or major finding. A clean review MUST use `findings: - none` and still provide a substantive summary and residual-risk statement.
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

- Accepts work from `codebase-onboarding` once the changeset to review is identified.
- Accepts GitHub or Azure DevOps pull request review requests routed from `azure-devops`.
- Hand off to `code-review` when the review surfaces systemic code issues beyond the diff.
- Hand off to `test-strategy` when the changeset lacks meaningful coverage for its behavior.
- Hand off to `review-response` when the author asks you to act on review feedback received from others.
- Terminal skill for the review artifact itself — the verdict and findings are the final output.

## Error Handling

1. Local: If a hunk lacks context to judge, request the surrounding file rather than guessing.
2. Flow: If the diff is too large to review responsibly in one pass, review by commit or by directory and state the split explicitly.
3. Recovery: If the author disputes a finding with evidence, re-verify against the code and either withdraw it with a one-line reason or keep it with the counter-evidence cited.

## Human-in-the-Loop

Request explicit approval before:

- Posting review comments or a verdict to an external system (GitHub, Azure DevOps).
- Approving a changeset that touches authentication, authorization, payments, or data deletion paths.

## Validation

Apply the operating rules above when finalizing every review. For the detailed checklist, read `tests/validation-checklist.md` only when validating a completed review; run `tests/run-validation.py` only when the user explicitly requests test execution.

## Bundled resources

- Read `assets/templates/output.md` when formatting the review artifact.
- Read `assets/examples/happy-path.md` when a concrete standard review example is useful.
- Read `assets/examples/edge-case.md` when reviewing an oversized diff.
- Run `scripts/validate-output.py` when checking a generated review against the output contract.
- Read `references/workflow.md` when the review needs detailed step-by-step workflow guidance.
- Read `references/examples.md` when sample reviews beyond the templates are needed.
- Read `rules/diff-first.md` when applying detailed diff-scope guidance.
- Read `rules/verdict-discipline.md` when resolving verdict consistency.
- Read `rules/comment-quality.md` when drafting or revising findings.
- Read `rules/scope-guard.md` when separating changed code from out-of-scope observations.
- Run `tests/run-validation.py` only when the user explicitly requests test execution; it validates the bundled output validator.
