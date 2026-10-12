# Authoring craft: writing skills that work

Read this when creating a new skill or rewriting a skill's content.

## Ground the skill in real expertise

The top failure mode is a skill synthesized from generic knowledge — it produces
vague filler ("handle errors appropriately"). Feed the creation process real
material: internal docs, runbooks, API specs, code review comments, git history,
past failure cases, transcripts of tasks done by hand. Extract the reusable
pattern: steps that worked, corrections the human made, input/output formats,
context the agent could not have known.

## Spend context wisely

The SKILL.md body competes for attention with the conversation, system prompt,
and other skills. For every sentence ask: "Would the agent get this wrong
without it?" If no — cut. Do not explain what a PDF is or how HTTP works. Aim
for moderate detail: concise stepwise guidance plus one working example beats
exhaustive documentation.

## Scope coherent units

A skill should encapsulate one coherent unit of work, like a well-designed
function. Too narrow → multiple skills must load for one task (overhead,
conflicting instructions). Too broad → imprecise triggering. If a skill needs
another skill to be useful, consider merging; if its description cannot say
when it applies in two sentences, consider splitting.

## Calibrate degrees of freedom per part

- **High freedom** (prose guidance): multiple valid approaches, context-dependent
  decisions. Explain *why* — reasoning-based instructions ("Do X because Y
  causes Z") are followed more reliably than rigid ALWAYS/NEVER rules.
- **Medium freedom** (pseudocode, parameterized scripts): a preferred pattern
  exists with acceptable variation.
- **Low freedom** (exact commands/scripts): fragile operations where consistency
  is critical. "Run exactly this; do not modify."

## Descriptions that trigger

The description is the only thing loaded at discovery time.

- Use imperative framing: "Use this skill when..." rather than "This skill does..."
- Describe user intent, not internal mechanics.
- Be pushy: include cases where the user doesn't name the domain ("even if they
  don't mention CSV"). List synonyms and task verbs users actually type.
- A few sentences; hard limit 1024 chars.
- Boundary clauses prevent false triggers: state what the skill does NOT do when
  adjacent skills exist.

Bad → good:

```yaml
# Bad
description: Helps with PDFs.
# Good
description: Extracts text and tables from PDF files, fills forms, merges PDFs.
  Use when working with PDF documents or when the user mentions PDFs, forms, or
  document extraction.
```

## Instruction patterns (use what fits)

- **Gotchas section**: concrete environment-specific traps with their fixes —
  the highest-value content in most skills. Keep in SKILL.md (agent may not
  recognize when to load an external gotchas file).
- **Templates**: for fixed output formats, give a concrete template, not prose
  describing the format. Short templates inline; long ones in `assets/`.
- **Checklists**: `- [ ]` step lists for multi-step workflows with dependencies.
- **Validation loops**: do work → run a validator script → fix → repeat until
  clean. Include this pattern whenever a checkable output exists.
- **Plan-validate-execute**: for batch/destructive operations, produce an
  intermediate plan file, validate it against a source of truth with a script,
  then execute. Error messages should name what was expected vs received.
- **Defaults, not menus**: pick one default tool/approach, mention alternatives
  in one subordinate sentence.

## Progressive disclosure structure

When SKILL.md approaches 500 lines: keep the core workflow + selection guidance
in SKILL.md, move variant/domain-specific detail into `references/` files
(one per domain, framework, or provider), and link each from SKILL.md with its
trigger condition ("Read `references/api-errors.md` if the API returns non-200").
A bare "see references/ for details" is a defect. All reference files link
directly from SKILL.md — one level deep, no chains.

## Bundled scripts

Bundle a script when the same logic would otherwise be rewritten each run, or
when deterministic reliability matters. Requirements for agent-facing scripts:

- Non-interactive — input only via flags/env/stdin; never prompt.
- `--help` with concise usage and examples (it enters the agent's context).
- Errors that say what went wrong, what was expected, what to try.
- Structured output (JSON/CSV) on stdout; diagnostics on stderr.
- Self-contained: prefer PEP 723 inline dependencies (`uv run script.py`) or
  one-off tools via `uvx`/`npx` with pinned versions.
- Idempotent, safe defaults, meaningful exit codes, `--dry-run` for destructive
  operations, bounded output size (`--output` file or pagination for large data).

State runtime prerequisites in SKILL.md; use the `compatibility` frontmatter
field for hard environment requirements. Test every script by running it.

## What never belongs in a skill

README.md, CHANGELOG.md, installation guides, process notes about how the skill
was built. Only what helps the agent do the job.
