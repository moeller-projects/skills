# Agent skills

Reusable instructions for coding agents. Each skill's `SKILL.md` describes when to use it and how to work; supporting rules, references, examples, scripts, and checks live alongside it.

## Get started

1. Choose a skill from the catalog below and copy its entire `skills/<name>/` directory into the skills directory supported by your agent. The destination depends on the agent; this repository does not provide an installer.
2. Open the copied `SKILL.md` and use its `description` to decide when it applies. Follow its workflow and consult linked files relative to that skill directory.
3. Keep the whole directory together: some skills use `rules/`, `references/`, `assets/`, or `scripts/` in addition to `SKILL.md`.

Skills compose other skills by name. Copy the model-invoked primitives named in
the selected skill's Handoffs/workflow too; those instructions are not bundled
automatically. User-invoked recommendations remain the human's decision.
Tool names and `allowed-tools` support differ between harnesses: map supported
capabilities at installation, and do not turn a read-only declaration into
permission to edit or execute. Workflow authorization gates still apply.

## Skill catalog

| Skill | Use it for |
| --- | --- |
| [azure-devops](skills/azure-devops/) | Azure DevOps work-item fields, comments, change history, related work, and PR discussion; guarded, approved writes |
| [concise-output](skills/concise-output/) | Action-first, concise response style that preserves accuracy and safety |
| [code-review](skills/code-review/) | Whole-codebase or subsystem review: quality, refactoring, security, evidence-backed performance (not PR/diff review — use `pr-review`) |
| [task-planning](skills/task-planning/) | Breaking confirmed scope into tasks, dependencies, and done criteria |
| [plan-execution](skills/plan-execution/) | Executing a confirmed plan to completion: per-task proof, review gates, subagent or inline modes |
| [technical-writing](skills/technical-writing/) | READMEs, agent instructions, developer guides, and decision records |
| [ste-clarity](skills/ste-clarity/) | STE-inspired rewriting, explanation, and linting for technical English |
| [operations](skills/operations/) | CI/CD, infrastructure, rollout safety, and operational risk |
| [codebase-onboarding](skills/codebase-onboarding/) | Repository discovery, conventions, entry points, and hotspots |
| [spec-writing](skills/spec-writing/) | Requirements, acceptance criteria, and OpenSpec proposals |
| [test-strategy](skills/test-strategy/) | Test strategy, coverage, E2E flows, and flaky-test reduction |
| [discovery](skills/discovery/) | Clarifying vague problems and comparing options before commitment |
| [incident-response](skills/incident-response/) | Mitigation-first response to live production incidents, timeline capture, and postmortem follow-ups |
| [pr-review](skills/pr-review/) | Pull request and changeset reviews with actionable findings and a clear verdict |
| [review-response](skills/review-response/) | Handling incoming review feedback: verify against the codebase, implement or push back with reasoning |
| [skill-forge](skills/skill-forge/) | Creating, auditing, refactoring, validating, and packaging Agent Skills |
| [debugging](skills/debugging/) | Root-cause diagnosis of local failures: repro-first, hypothesis ranking, and bisection |
| [git-workflow](skills/git-workflow/) | Conventional commits, branching, rebasing, stacked PRs, and safe history recovery |
| [gh-stack](skills/gh-stack/) | Stacked pull requests with the `gh stack` CLI: create, sync, submit, and merge dependent PR layers |
| [git-worktrees](skills/git-worktrees/) | Isolated workspaces for implementation: detection, native tools, git worktree fallback, clean baseline |
| [branch-integration](skills/branch-integration/) | Landing finished work: merge, PR, keep, or discard with verified tests and safe cleanup |
| [test-driven-development](skills/test-driven-development/) | Red/green/refactor discipline: failing test first, minimal pass, refactor on green |
| [verification-before-completion](skills/verification-before-completion/) | Evidence-before-claims gate for completion, fixed, and passing claims |
| [pr-body](skills/pr-body/) | Pull request bodies: smallest clarifying visual, before/after evidence, merge-danger call |
| [session-handoff](skills/session-handoff/) | Compacting a session into a portable handoff document (user-invoked) |
| [session-retro](skills/session-retro/) | Retrospectives that improve the agent's environment: checks, standards, pointers (user-invoked) |
| [domain-modeling](skills/domain-modeling/) | Shared project language: GLOSSARY.md terms and ADRs, updated inline as decisions land |
| [codebase-design](skills/codebase-design/) | Deep-module vocabulary for interface, seam, and testability decisions |
| [prototype](skills/prototype/) | Throwaway code that answers one design question, captured as a primary source |
| [research](skills/research/) | Cited findings from primary sources, delegated to a background agent |
| [setup-wizard](skills/setup-wizard/) | Interactive bash wizards for procedures only a human can perform |
| [decision-mapping](skills/decision-mapping/) | Charting huge foggy efforts as decision maps, one decision per session (user-invoked) |
| [guided-learning](skills/guided-learning/) | Teaching a topic across sessions from a stateful workspace (user-invoked) |
| [ask-lukas](skills/ask-lukas/) | Router: which skill or flow fits your situation (user-invoked) |

## Invocation classes

Skills come in two classes, recorded as `invocation` in each skill's `metadata`:

- **Model-invoked** (the default) — the agent reaches for them autonomously when the task fits. Their descriptions carry the triggering burden.
- **User-invoked** — orchestrators that fire only when you name them: `ask-lukas`, `session-handoff`, `session-retro`, `decision-mapping`, `guided-learning`. User-invoked skills compose model-invoked ones, never each other.

When you can't remember which skill fits, ask the router: `ask-lukas`.

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

## Contributing

See [AGENTS.md](AGENTS.md) for the skill layout, version rules, and change workflow. Skills with `tests/run-validation.py` include their own validation runner; execute it only when test execution is explicitly authorized. Restore, build, and packaging remain independently gated. Concise Output has no validation runner. There is no repository-wide build or test command in this tree.

For authorized static checks, run
`python skills/skill-forge/scripts/validate_skill.py skills/<name> --strict --json`.
It checks frontmatter, synchronized manifests, and resource discovery; a clean
report does not prove behavioral correctness. Skill Forge's test runner accepts
`--include-packaging` only with separate packaging authorization and uses
disposable archives.

For prompt-level checks, [Ask Lukas](skills/ask-lukas/SKILL.md#evaluation-resources)
bundles fresh-context activation and workflow-decision cases plus a captured-result
checker. Run those only with evaluation/test authorization. Inspect actual model
rationales as well as expected fields; decision evaluations do not exercise live
Git, production, or Azure DevOps actions.

## License

[MIT](LICENSE).
