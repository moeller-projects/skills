# Working on this repository

This repository contains reusable agent skills under `skills/<kebab-case-name>/`. The root [README](README.md) is the user-facing catalog; each skill's `SKILL.md` is its agent-facing entry point.

## Skill layout

- A skill directory MUST contain `SKILL.md`. Add supporting directories only when used. Do not add `README.md`, `CHANGELOG.md`, or installation/process documents to a skill directory.
- Keep `SKILL.md` frontmatter limited to Agent Skills specification fields: `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. Store repository-specific `title`, `version`, and `summary` inside the `metadata` mapping; keep `metadata.json` synchronized.
- `allowed-tools`, when present, MUST be a space-separated string of pre-approved tools, not a YAML list.
- Keep `SKILL.md` concise. Put detailed workflows in `references/`, focused guidance in `rules/`, examples/templates in `assets/`, and executable helpers in `scripts/` where needed. Every bundled resource MUST be linked directly from `SKILL.md` with a stated use condition. Avoid reference chains.
- Make minimal, skill-scoped changes; update links and descriptions in the root README if the catalog or use cases change.

## Change workflow

1. Read the affected skill's `SKILL.md`, `metadata.json`, and every relevant bundled file before editing.
2. Update the entrypoint and manifest together. Preserve accurate activation guidance (`use_when` and `avoid_when`) and output contracts.
3. Review paths, commands, links, and versions against the tree. Gateway and engine skills have `tests/run-validation.py`; run it only when test execution is explicitly authorized. Concise Output has no validation runner. There is no root-level suite.
