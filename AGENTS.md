# Working on this repository

This repository contains reusable agent skills under `skills/<kebab-case-name>/`. The root [README](README.md) is the user-facing catalog; each skill's `SKILL.md` is its agent-facing entry point.

## Skill layout

- A complete skill has `SKILL.md`, `README.md`, and `metadata.json` in its directory. Keep its name consistent across the directory, frontmatter, and metadata.
- Keep the version in `SKILL.md` frontmatter, the `Version:` line in `README.md`, and `metadata.json` identical when changing a skill.
- Keep `SKILL.md` concise. Put detailed workflows in `references/`, focused guidance in `rules/`, examples/templates in `assets/`, and executable helpers in `scripts/` where needed. Not every skill needs every supporting directory.
- Make minimal, skill-scoped changes; update links and descriptions in the root README if the catalog or use cases change.

## Change workflow

1. Read the affected skill's `SKILL.md`, `README.md`, and `metadata.json`, plus the relevant supporting files, before editing.
2. Update the skill's entry point, supporting material, and manifest together. Preserve accurate activation guidance (`use_when` and `avoid_when`) and output contracts.
3. Review paths, commands, and versions against the files in the tree. All skills except `pit-board` have `tests/run-validation.py`; from the affected skill directory, run `python tests/run-validation.py` when test execution is authorized. Pit Board has no validation runner; check its manifest, links, and version manually. There is no root-level suite.

## Naming

Skills are named after race crew roles (spotter, race-engineer, crew-chief, co-driver, mechanic, scrutineer, test-driver, press-officer, pit-crew, safety-car, radio, pit-board). New skills must follow the same race crew theme and stay kebab-case.
