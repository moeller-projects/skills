---
name: skill-forge
description: Create new Agent Skills and refactor existing ones to production grade, compliant with the agentskills.io open specification. Use when the user asks to create, build, scaffold, write, improve, refactor, audit, review, fix, validate, or package a skill (a directory containing SKILL.md with YAML frontmatter). Covers spec-compliant frontmatter (name/description limits), triggering-optimized descriptions, progressive disclosure structure, scripts/references/assets organization, validation, and .skill packaging — even when the user just says "make this skill better" or "check my skill".
compatibility: Requires Python 3.8+ to run the bundled scripts (stdlib only; PyYAML optional). The guidance in SKILL.md and references/ works without it.
metadata:
  version: "1.2"
  spec: agentskills.io
---

# Skill Forge

Create and refactor Agent Skills to production grade. Ground every skill in real
domain material (existing docs, code, task transcripts) rather than generic
knowledge — generic instructions are the most common failure mode.

## Choose the workflow

- **Creating a new skill** → follow "Create" below. For authoring craft
  (context budget, degrees of freedom, description formula, instruction
  patterns), read [references/authoring.md](references/authoring.md).
- **Refactoring or auditing an existing skill** → follow "Refactor" below.
  For the audit rubric and evaluation-driven iteration, read
  [references/refactoring.md](references/refactoring.md).
- **Unsure about a format rule** → check
  [references/specification.md](references/specification.md) (condensed normative
  spec + validator behavior).

## Create

1. **Gather concrete usage examples.** Ask the user (or infer from provided
   material) what prompts should trigger this skill and what tasks it performs.
   Prefer real project artifacts — docs, runbooks, schemas, past corrections —
   over imagined requirements. Skip only if the scope is already unambiguous.
2. **Plan reusable contents.** For each example, decide what belongs in
   `scripts/` (deterministic or repeatedly rewritten logic), `references/`
   (docs loaded on demand), or `assets/` (files used in output). Most skills
   need only a subset; create no empty directories.
3. **Initialize:** `python3 scripts/init_skill.py <skill-name> --path <dir>`
4. **Write the skill.** Replace every `[TODO]` in the generated SKILL.md:
   - Frontmatter: `name` (must equal directory name) and `description`. The
     description is the only triggering signal — write what the skill does AND
     when to use it, with concrete trigger contexts. Optional fields
     (`license`, `compatibility`, `metadata`, `allowed-tools`) only when needed.
   - Body: imperative instructions; under 500 lines. Add only what the agent
     would get wrong without the skill; move detail into `references/` and
     state in SKILL.md exactly when to read each file.
   - Test every bundled script by actually running it before packaging.
5. **Validate:** `python3 scripts/validate_skill.py <skill-dir>` — fix all
   ERRORs; treat WARNINGs as production-grade checklist items.
6. **Package:** `python3 scripts/package_skill.py <skill-dir> [output-dir]`
7. **Iterate.** After real use, fold user corrections into a `## Gotchas`
   section and re-validate. For systematic quality testing (test cases,
   assertions, with/without-skill benchmarks), see
   [references/refactoring.md](references/refactoring.md#evaluation-driven-iteration).

## Refactor

1. **Read the whole skill first** — SKILL.md plus every bundled file — before
   changing anything. Snapshot it (`cp -r`) if the refactor is large.
2. **Audit** with `python3 scripts/validate_skill.py <skill-dir> --strict`,
   then apply the rubric in [references/refactoring.md](references/refactoring.md):
   spec compliance, description triggering, context budget, structure, scripts,
   anti-patterns.
3. **Apply changes in priority order:** spec errors → description (triggering)
   → context bloat (split/trim) → structure → scripts → style. Generalize
   fixes; do not patch narrow cases.
4. **Re-validate and package** (steps 5-6 of Create). When the user can run
   evals, compare old vs new with the evaluation loop in
   [references/refactoring.md](references/refactoring.md#evaluation-driven-iteration).

## Scripts

- **`scripts/init_skill.py <name> --path <dir>`** — scaffold a compliant
  SKILL.md template. Validates the name against spec rules.
- **`scripts/validate_skill.py <skill-dir> [--json] [--strict]`** — checks all
  spec rules (exit 1 on violation) plus production warnings: oversized SKILL.md,
  unreferenced or deeply nested bundled files, forbidden README/CHANGELOG-style
  docs, missing or weak trigger clauses, absolute paths, dead links.
- **`scripts/package_skill.py <skill-dir> [out-dir] [--strict]`** — validates,
  then zips to `<name>.skill`. Refuses to package when spec errors exist.

## Gotchas

- The `description` field carries the entire triggering burden — never bury
  "when to use" information in the body, where it is invisible at discovery
  time. Hard limit: 1024 chars.
- `name` must exactly match the parent directory name; lowercase letters,
  digits, single hyphens only; max 64 chars.
- Only these frontmatter fields are allowed: `name`, `description`, `license`,
  `compatibility`, `metadata`, `allowed-tools`.
- Reference files are discovered by reading SKILL.md — any bundled file not
  linked from SKILL.md (with a stated trigger condition) is effectively dead.
- Never add README.md, CHANGELOG.md, or similar docs to a skill — SKILL.md is
  the only documentation the agent reads.
- Skills must teach a reusable *approach*, not a one-off answer; and scripts
  must be non-interactive with `--help`, clear errors, and structured output.
