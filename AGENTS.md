# Working on this repository

This repository contains reusable agent skills under `skills/<kebab-case-name>/`. The root [README](README.md) is the user-facing catalog; each skill's `SKILL.md` is its agent-facing entry point.

## Skill layout

- A skill directory MUST contain `SKILL.md`. Add supporting directories only when used. Do not add `README.md`, `CHANGELOG.md`, or installation/process documents to a skill directory.
- Keep `SKILL.md` frontmatter limited to Agent Skills specification fields: `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. Store repository-specific `title`, `version`, `summary`, and `invocation` inside the `metadata` mapping. `metadata.json` is generated from that frontmatter plus `catalog.json`; regenerate it with `sync_manifests.py`.
- `allowed-tools`, when present, MUST be a space-separated string of pre-approved tools, not a YAML list.
- Keep `SKILL.md` concise. Put detailed workflows in `references/`, focused guidance in `rules/`, examples/templates in `assets/`, and executable helpers in `scripts/` where needed. Every bundled resource MUST be linked directly from `SKILL.md` with a stated use condition. Avoid reference chains.
- Make minimal, skill-scoped changes; update links and descriptions in the root README if the catalog or use cases change.

## Invocation classes

Every skill is exactly one of two invocation classes, recorded as `metadata.invocation` (default `model`):

- **Model-invoked** (`invocation: "model"`): reusable discipline the agent reaches for autonomously when the task fits. The `description` carries the full triggering burden: what it does, when to use it, and when not to. Most skills are model-invoked.
- **User-invoked** (`invocation: "user"`): an orchestrator that fires only when the human names it (e.g. `ask-lukas`, `session-retro`, `session-handoff`). Its `description` is human-facing orientation, not a trigger; do not stuff it with model-facing trigger clauses. On harnesses that support it, apply `disable-model-invocation: true` at install time.

A user-invoked skill may compose model-invoked skills, but MUST NOT invoke another user-invoked skill — chaining orchestrators is the human's job. When the catalog grows past what a human can remember, add or update a user-invoked router skill (`ask-lukas`) instead of making everything model-invoked.

## Composition over duplication

Shared discipline lives in exactly one model-invoked primitive; other skills link to it by name in their Handoffs section. A skill that mostly forwards to one or two primitives should be a thin wrapper that says so in one line, not a copy of the primitive's content. Duplicated doctrine across skills is a defect: fix it by extracting the primitive, not by editing both copies.

Fix at the source. When an eval or review fails, repair the one canonical rule and replace any restatement with a pointer. Record a Gotcha once.

## Versioning

`metadata.version` is a semver string, mirrored into `metadata.json` by `sync_manifests.py`.

- **Patch** — wording, formatting, link, or hygiene changes with no behavior change.
- **Minor** — new optional behavior, a new bundled resource, or a new handoff that existing users can ignore.
- **Major** — a broken contract, renamed field, changed CLI, or removed flag.

## Generated files

`metadata.json`, the README skill table, and the validation-runner lists are generated. Edit the source — `SKILL.md` frontmatter, `catalog.json`, or the README row order — then regenerate with `sync_manifests.py` and `sync_readme.py`. Do not hand-edit generated output; `--check` fails on drift.

## Change workflow

1. Read the affected skill's `SKILL.md`, `metadata.json`, and every relevant bundled file before editing.
2. Update the entrypoint and regenerate the manifest. The `description` carries activation; preserve the output contract. Run `sync_manifests.py` after editing frontmatter.
3. Review paths, commands, links, and versions against the tree.

<!-- generated:agents-validation-runners -->
Skills with `tests/run-validation.py` are `ask-lukas`, `azure-devops`, `code-review`, `codebase-onboarding`, `debugging`, `discovery`, `git-workflow`, `incident-response`, `operations`, `pr-review`, `skill-forge`, `spec-writing`, `task-planning`, `technical-writing`, `test-strategy`; run one only when test execution is explicitly authorized.
<!-- /generated:agents-validation-runners -->

There is no root-level suite.
