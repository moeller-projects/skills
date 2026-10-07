# Agent skills

Reusable instructions for coding agents. Each skill's `SKILL.md` describes when to use it and how to work; supporting rules, references, examples, scripts, and checks live alongside it.

## Get started

1. Choose a skill from the catalog below and copy its entire `skills/<name>/` directory into the skills directory supported by your agent. The destination depends on the agent; this repository does not provide an installer.
2. Open the copied `SKILL.md` and use its `description` to decide when it applies. Follow its workflow and consult linked files relative to that skill directory.
3. Keep the whole directory together: some skills use `rules/`, `references/`, `assets/`, or `scripts/` in addition to `SKILL.md`.

## Skill catalog

| Skill | Use it for |
| --- | --- |
| [ado-gateway](skills/ado-gateway/) | Azure DevOps work items and PR discussion; guarded, approved writes |
| [bluf](skills/bluf/) | Action-first, concise response style that preserves accuracy and safety |
| [code-quality-engine](skills/code-quality-engine/) | Code review, refactoring, security, and evidence-backed performance |
| [delivery-engine](skills/delivery-engine/) | Breaking confirmed scope into tasks, dependencies, and done criteria |
| [doc-engine](skills/doc-engine/) | READMEs, agent instructions, developer guides, and decision records |
| [ops-engine](skills/ops-engine/) | CI/CD, infrastructure, rollout safety, and operational risk |
| [repo-engine](skills/repo-engine/) | Repository discovery, conventions, entry points, and hotspots |
| [spec-engine](skills/spec-engine/) | Requirements, acceptance criteria, and OpenSpec proposals |
| [test-engine](skills/test-engine/) | Test strategy, coverage, E2E flows, and flaky-test reduction |
| [thinking-engine](skills/thinking-engine/) | Clarifying vague problems and comparing options before commitment |

`skills/caveman/` contains only partial supporting files and is not a usable skill directory yet.

## Contributing

See [AGENTS.md](AGENTS.md) for the skill layout, version rules, and change workflow. Gateway and engine skills include a `tests/run-validation.py` script; run it from the skill directory when validating a change to that skill. BLUF has no validation runner. There is no repository-wide build or test command in this tree.

## License

[MIT](LICENSE).
