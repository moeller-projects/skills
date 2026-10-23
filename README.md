# Agent skills

Reusable instructions for coding agents. Each skill's `SKILL.md` describes when to use it and how to work; supporting rules, references, examples, scripts, and checks live alongside it.

## Get started

1. Install a skill and the model-invoked primitives it requires:
   `python scripts/install.py --dest <your skills directory> --skill <name>`.
   It is a dry run until you add `--apply`; `--harness pi` also adds
   `disable-model-invocation: true` to user-invoked skills. Copying a skill
   directory by hand still works.
2. Open the installed `SKILL.md` and use its `description` to decide when it
   applies. Follow its workflow and consult linked files relative to that skill
   directory.
3. Keep the whole directory together: some skills use `rules/`, `references/`,
   `assets/`, or `scripts/` in addition to `SKILL.md`.

`metadata.json` `requires` lists the model-invoked primitives each skill
composes, so the installer copies them automatically. User-invoked
recommendations remain the human's decision. Tool names and `allowed-tools`
support differ between harnesses: map supported capabilities at installation,
and do not turn a read-only declaration into permission to edit or execute.
Workflow authorization gates still apply.

## Skill catalog

<!-- generated:skill-catalog -->
| Skill | Use it for |
| --- | --- |
| [azure-devops](skills/azure-devops/) | Read and safely write selected Azure DevOps work items and PR artifacts, and locate a branch's active PR, with deterministic dry-run, approval, and validation gates. |
| [concise-output](skills/concise-output/) | Deliver accurate, action-first responses with concise prose and explicit next steps. |
| [code-review](skills/code-review/) | Improve correctness, readability, maintainability, performance, and legacy modernization with minimal mutation. |
| [task-planning](skills/task-planning/) | Break work into atomic, shippable tasks with explicit dependencies, critical path, estimates, and definitions of done. |
| [plan-execution](skills/plan-execution/) | Execute a confirmed plan to completion with per-task proof, review gates, and ledgered rulings. |
| [technical-writing](skills/technical-writing/) | Create accurate technical docs, READMEs, AGENTS.md files, and developer guides with clear structure. |
| [ste-clarity](skills/ste-clarity/) | Rewrite and lint technical English with ASD-STE100-inspired clarity rules. |
| [operations](skills/operations/) | Plan safer delivery across CI/CD, containers, Kubernetes, reliability, threat modeling, and rollback decisions. |
| [codebase-onboarding](skills/codebase-onboarding/) | Map repository architecture, entry points, conventions, hotspots, and onboarding artifacts for fast execution. |
| [spec-writing](skills/spec-writing/) | Turn requests or azure-devops handoffs into structured, version-aware specs with risk tiers, acceptance criteria, policy gates, and optional OpenSpec proposal output. |
| [test-strategy](skills/test-strategy/) | Plan resilient test coverage by selecting levels, cases, and flake-risk remedies; route test writing and behavior implementation to test-driven-development. |
| [discovery](skills/discovery/) | Explore ambiguous problems, test assumptions, compare options, and produce decision-ready plans. |
| [incident-response](skills/incident-response/) | Respond to live production incidents with mitigation-first triage, disciplined timelines, clear comms, and durable follow-ups. |
| [pr-review](skills/pr-review/) | Review pull requests and changesets against the diff, deliver actionable author-facing findings, and issue a clear verdict. |
| [review-response](skills/review-response/) | Verify review feedback against the codebase, then implement or push back with technical reasoning; gate tests on explicit authorization and report unrun verification honestly. |
| [respond-to-pr-comments](skills/respond-to-pr-comments/) | Triage reviewer threads on your Azure DevOps PR, apply approved fixes as commits, and post replies that cite pushed commits, with approval before changes, pushes, and posts. |
| [skill-forge](skills/skill-forge/) | Create and refactor Agent Skills with explicit static validation, behavioral evaluation, and safe packaging. |
| [debugging](skills/debugging/) | Find and verify root causes of local development failures through deterministic reproduction and evidence. |
| [git-workflow](skills/git-workflow/) | Plan safe, disciplined Git history, branching, commit, rebase, recovery, and stacked PR operations. |
| [gh-stack](skills/gh-stack/) | Create, maintain, and merge stacked pull requests with the gh stack CLI extension. |
| [git-worktrees](skills/git-worktrees/) | Establish an isolated, verified-clean workspace before starting implementation work. |
| [branch-integration](skills/branch-integration/) | Land verified work through a user-chosen integration path with safe cleanup. |
| [test-driven-development](skills/test-driven-development/) | Drive behavior implementation with a failing test first, then minimal passing code and refactoring; use for feature, bugfix, and behavior-change tests. |
| [verification-before-completion](skills/verification-before-completion/) | Back every completion, fixed, or passing claim with fresh verification evidence, or an honest unverified status when execution is not authorized; use before reporting completion or success. |
| [pr-body](skills/pr-body/) | Write PR bodies with the smallest clarifying visual, before/after evidence, and an honest call on what merging risks, including explicit verification gaps when proof is not authorized. |
| [session-handoff](skills/session-handoff/) | Create a portable handoff document that lets a fresh agent or colleague continue work with its state, decisions, next action, and references. |
| [session-retro](skills/session-retro/) | Turn a completed session's observed failures into improvements to the agent environment—navigation, checks, standards, tooling, and steering. |
| [domain-modeling](skills/domain-modeling/) | Keep the project's shared language sharp; propose glossary terms and ADRs, and mutate artifacts only when explicitly requested. |
| [codebase-design](skills/codebase-design/) | Design deep modules — small interfaces over real behavior, at clean seams, testable through the interface. |
| [prototype](skills/prototype/) | Answer one design question with throwaway, trivially-runnable code, then record the verdict in its spec or ticket; production edits require a separate implementation scope. |
| [research](skills/research/) | Delegate investigation to a background agent; capture cited findings from primary sources as Markdown. |
| [setup-wizard](skills/setup-wizard/) | Turn human-only procedures into interactive bash wizards with captured values and confirmation gates. |
| [decision-mapping](skills/decision-mapping/) | Chart a large, uncertain effort as a decision map, resolve open questions, and hand off a clear route to specification. |
| [guided-learning](skills/guided-learning/) | Teach a topic across sessions with a stateful workspace of lessons, references, practice, and learning records. |
| [ask-lukas](skills/ask-lukas/) | Route any situation to the right skill or flow in this catalog. |
<!-- /generated:skill-catalog -->

## Invocation classes

Skills come in two classes, recorded as `invocation` in each skill's `metadata`:

- **Model-invoked** (the default) — the agent reaches for them autonomously when the task fits. Their descriptions carry the triggering burden.
- **User-invoked** — orchestrators that fire only when you name them: `ask-lukas`, `respond-to-pr-comments`, `session-handoff`, `session-retro`, `decision-mapping`, `guided-learning`. User-invoked skills compose model-invoked ones, never each other.

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

## Validation runners

<!-- generated:readme-validation-runners -->
Skills with `tests/run-validation.py` (15 of 35):

`ask-lukas`, `azure-devops`, `code-review`, `codebase-onboarding`, `debugging`, `discovery`, `git-workflow`, `incident-response`, `operations`, `pr-review`, `skill-forge`, `spec-writing`, `task-planning`, `technical-writing`, `test-strategy`.

Skills without a runner (20): `branch-integration`, `codebase-design`, `concise-output`, `decision-mapping`, `domain-modeling`, `gh-stack`, `git-worktrees`, `guided-learning`, `plan-execution`, `pr-body`, `prototype`, `research`, `respond-to-pr-comments`, `review-response`, `session-handoff`, `session-retro`, `setup-wizard`, `ste-clarity`, `test-driven-development`, `verification-before-completion`.
<!-- /generated:readme-validation-runners -->

Execute a runner only when test execution is explicitly authorized. Restore, build, and packaging remain independently gated. There is no repository-wide build or test command in this tree.

## Contributing

See [AGENTS.md](AGENTS.md) for the skill layout, version rules, and change workflow.

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
