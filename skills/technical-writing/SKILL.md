---
name: technical-writing
description: Use when creating or improving README, AGENTS.md, architecture, workflow, or decision-record docs. Do not use when the primary need is repository discovery or architecture mapping before authoring docs, or when the request is pure code implementation.
metadata:
  title: Technical Writing
  version: "1.0.5"
  summary: Create accurate technical docs, READMEs, AGENTS.md files, and developer guides with clear structure.
---

# Technical Writing

## Purpose

Create and improve technical documentation, README files, AGENTS.md files, architecture notes, diagrams, and usage docs that help people act correctly.

## Output Format Selection

Choose artifact format based on reader's primary activity.

Use Markdown when artifact is:
- maintained inside repository
- reviewed through diffs
- expected to be edited by developers
- source document for future changes

Use self-contained HTML when artifact is:
- primarily read rather than edited
- shared outside repository
- presented to stakeholders
- printed or archived
- review-ready artifact

Decision question:

"Will this artifact mainly be edited or mainly be read?"

- Edited → Markdown
- Read → HTML

## Workflow
 
1. Identify the audience, task, and missing decisions the doc must support; if audience is unclear, state the assumption explicitly.
2. Build a clear structure before expanding prose; tag each section with its Diátaxis mode (tutorial, how-to, reference, explanation).
3. If the target file already exists, default to a diff-only update; stop and request explicit approval before replacing the full document or overwriting a top-level README.md, AGENTS.md, or workflow guide.
4. Keep commands, file paths, and workflow steps accurate; verify each before including.
5. Add only the context needed to make the reader effective.
6. Note remaining gaps, assumptions, or follow-up docs.

## Output Contract

Default:
```text
doc:
- purpose:
- audience:
- structure:
  1. <section> [tutorial|how-to|reference|explanation] — <scope>
- format:
  - type: markdown|html
  - reason:
- artifact:
  - <filename>

changes:
- ...

gaps:
- ...
```

## Handoffs

- Accepts work from `codebase-onboarding` once the documentation surface is identified.
- Accepts work from `code-review` or `test-strategy` when code or test changes require documentation updates.
- Terminal skill — output is the final artifact; no downstream handoff.

## Error Handling

1. Local: If audience or purpose is unclear, ask one question before drafting.
2. Flow: Skip sections where source material is missing; note each gap explicitly. If an existing document would be replaced wholesale, block until explicit overwrite approval is provided.
3. Recovery: Preserve original text by presenting changes as a diff, not a full replacement.

## Human-in-the-Loop

Request explicit approval before:

- Overwriting an existing README.md, AGENTS.md, or top-level workflow document.
- Replacing an existing document wholesale instead of presenting a diff.

## Validation Checklist

- [ ] Purpose and audience stated before any prose.
- [ ] Document structure defined before expanding sections.
- [ ] Each section in `structure:` tagged with one Diátaxis mode.
- [ ] Every command, path, and step verified accurate.
- [ ] All gaps listed explicitly; none silently omitted.
- [ ] Existing docs stay in diff form unless explicit overwrite approval is granted.

See `tests/validation-checklist.md` for the full checklist.

- `assets/templates/output.md` — read when producing the standard output structure.
- `assets/examples/happy-path.md` — read when creating a new README.
- `assets/examples/edge-case.md` — read when source material is missing.
- `assets/examples/decision-record.md` — read when producing a decision record.
- `assets/examples/mode-mixed.md` — read when producing a multi-mode README.
- `scripts/validate-output.py` — run when validating output structure. For HTML, pass `--html-artifact path/to/file.html` to validate the actual artifact; without it, validation is metadata-only and MUST NOT claim the HTML was checked.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to validate skill output.
- `tests/validation-checklist.md` — read when reviewing the skill's validation requirements.
- `assets/examples/html-report.md` — read when producing a standalone HTML artifact.
- `assets/templates/html-document.html` — read when selecting HTML output; escape substituted title/header text as HTML text, and use the template's inline style/print rules for self-containment.

## References

- See `references/examples.md` for sample documentation outputs.

## Rules

- `rules/_sections.md` — read when organizing document sections.
- `rules/audience-first.md` — read when identifying audience and purpose.
- `rules/command-accuracy.md` — read when documenting commands or paths.
- `rules/structure-over-prose.md` — read when designing document structure.
- `rules/agentsmd-specificity.md` — read when writing AGENTS.md guidance.
- `rules/readme-completeness.md` — read when writing or reviewing a README.
- `rules/decision-capture.md` — read when recording architectural decisions.
- `rules/diataxis-mode.md` — read when assigning Diátaxis modes.
- `rules/output-format.md` — read when selecting Markdown versus HTML output.
