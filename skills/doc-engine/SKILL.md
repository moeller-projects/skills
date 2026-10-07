---
name: doc-engine
description: Use when creating or improving README, AGENTS.md, architecture, workflow, or decision-record docs. Do not use when the primary need is repository discovery or architecture mapping before authoring docs, or when the request is pure code implementation.
allowed-tools:
  - read_file
title: Doc Engine
version: 5.1.1
summary: Create accurate technical docs, READMEs, AGENTS.md files, and developer guides with clear structure.
---

# Doc Engine

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

## Use When

- Writing or improving a README.
- Writing or refining AGENTS.md guidance.
- Documenting architecture or developer workflows.
- Creating usage docs or technical notes.
- Explaining how a system should be used or maintained.
- Capturing an architectural decision, reusable pattern, or failure lesson as a durable decision record.

## Avoid When

- The user wants implementation only.
- Documentation would duplicate obvious code.

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

changes:
- ...

gaps:
- ...
```

## Handoffs

- Accepts work from `repo-engine` once the documentation surface is identified.
- Accepts work from `code-quality-engine` or `test-engine` when code or test changes require documentation updates.
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

## Assets

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — new README creation scenario
- `assets/examples/edge-case.md` — missing source material scenario
- `assets/examples/decision-record.md` — decision record scenario and expected output
- `assets/examples/mode-mixed.md` — multi-mode README with Diátaxis mode tags
- `scripts/validate-output.py` — validates output structure

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/examples.md` for sample documentation outputs.

## Rules

- `rules/_sections.md`
- `rules/audience-first.md`
- `rules/command-accuracy.md`
- `rules/structure-over-prose.md`
- `rules/agentsmd-specificity.md`
- `rules/readme-completeness.md`
- `rules/decision-capture.md`
- `rules/diataxis-mode.md`
