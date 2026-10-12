# Rule: Standard Sections

> Impact: medium

## Description

Structure output as verdict, summary, findings, out-of-scope, and risk so the author can triage the review in seconds.

## Apply When

- Returning any pull request or changeset review.

## Checks

- Exactly one verdict line is present.
- Findings are separated from out-of-scope observations.
- Residual risk is called out explicitly.

## Anti-Pattern

A stream-of-consciousness review where the author cannot tell whether the changeset may merge.
