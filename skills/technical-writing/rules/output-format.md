# Rule: Output Format Selection

> Impact: high

## Description

Select output format based on how artifact will be consumed, not authoring convenience.

## Apply When

- Creating new documentation artifacts.
- Producing reports, summaries, reviews, or stakeholder documents.

## Rules

Use Markdown for:
- README.md
- AGENTS.md
- CONTRIBUTING.md
- developer guides maintained in repositories
- configuration-adjacent documentation
- documents requiring frequent line-based review

Use HTML for:
- executive summaries
- status reports
- dashboards
- retrospectives
- client-facing documents
- review-ready plans
- circulated decision records
- printable documents

## HTML Requirements

When generating HTML:

- Produce a single self-contained file by default.
- Include semantic HTML structure.
- Keep CSS inline.
- Avoid external dependencies.
- Include print styles.
- Optimize for readability and accessibility.
- Use restrained styling.

## Anti-Pattern

Generating HTML README files or AGENTS.md files that should be maintained as repository source.
