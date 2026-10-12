# Agent skills

Reusable instructions for coding agents. Each skill's `SKILL.md` describes when to use it and how to work; supporting rules, references, examples, scripts, and checks live alongside it.

## Get started

1. Choose a skill from the catalog below and copy its entire `skills/<name>/` directory into the skills directory supported by your agent. The destination depends on the agent; this repository does not provide an installer.
2. Open the copied `SKILL.md` and use its `description` to decide when it applies. Follow its workflow and consult linked files relative to that skill directory.
3. Keep the whole directory together: some skills use `rules/`, `references/`, `assets/`, or `scripts/` in addition to `SKILL.md`.

## Skill catalog

| Skill | Use it for |
| --- | --- |
| [azure-devops](skills/azure-devops/) | Azure DevOps work-item fields, comments, change history, related work, and PR discussion; guarded, approved writes |
| [concise-output](skills/concise-output/) | Action-first, concise response style that preserves accuracy and safety |
| [code-review](skills/code-review/) | Code review, refactoring, security, and evidence-backed performance |
| [task-planning](skills/task-planning/) | Breaking confirmed scope into tasks, dependencies, and done criteria |
| [technical-writing](skills/technical-writing/) | READMEs, agent instructions, developer guides, and decision records |
| [operations](skills/operations/) | CI/CD, infrastructure, rollout safety, and operational risk |
| [codebase-onboarding](skills/codebase-onboarding/) | Repository discovery, conventions, entry points, and hotspots |
| [spec-writing](skills/spec-writing/) | Requirements, acceptance criteria, and OpenSpec proposals |
| [test-strategy](skills/test-strategy/) | Test strategy, coverage, E2E flows, and flaky-test reduction |
| [discovery](skills/discovery/) | Clarifying vague problems and comparing options before commitment |

## Renames

| Original | Production |
| --- | --- |
| `thinking-engine` | `discovery` |
| `spec-engine` | `spec-writing` |
| `delivery-engine` | `task-planning` |
| `repo-engine` | `codebase-onboarding` |
| `code-quality-engine` | `code-review` |
| `test-engine` | `test-strategy` |
| `doc-engine` | `technical-writing` |
| `ops-engine` | `operations` |
| `ado-gateway` | `azure-devops` |
| `bluf` | `concise-output` |
| `scrutineer` | `pr-review` |
| `safety-car` | `incident-response` |

`skills/caveman/` contains only partial supporting files and is not a usable skill directory yet.

## Contributing

See [AGENTS.md](AGENTS.md) for the skill layout, version rules, and change workflow. Skills with `tests/run-validation.py` include their own validation runner; run it from the skill directory when validating a change. Concise Output has no validation runner. There is no repository-wide build or test command in this tree.

## License

[MIT](LICENSE).
