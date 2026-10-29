---
name: ask-lukas
description: "User-invoked only: Ask which skill or flow fits your situation. A router over the skills in this catalog — it helps you choose the right route when you know what you want to achieve but not which skill to reach for."
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Ask Lukas
  version: "1.1.0"
  summary: Route any situation to the right skill or flow in this catalog.
  invocation: user
---

# Ask Lukas

You don't remember every skill, so ask. This skill routes a situation to the right skill or flow.

Before stating what a skill does or recommending a step be skipped, read that skill's `SKILL.md` — the summaries here are for orientation only.

## The main flow: idea → ship

1. **Vague idea or underspecified problem** → `discovery` (pressure-test assumptions, compare options).
2. **Requirements need writing down** → `spec-writing` (acceptance criteria, OpenSpec proposals).
3. **Confirmed scope needs decomposition** → `task-planning` (atomic tasks, dependencies, done criteria).
4. **Plan approved, ready to build** → `plan-execution` (inline or subagent modes), which pulls in `git-worktrees` for isolation, `test-driven-development` per task, and `debugging` when things fail.
5. **About to claim it works** → `verification-before-completion` (evidence before claims).
6. **Work is green and needs landing** → `branch-integration` (merge / PR / keep), then `pr-body` for the pull request write-up.
7. **Code needs review** → `pr-review` (changesets) or `code-review` (deeper quality/security). **Received review feedback** → `review-response`. For feedback on your own Azure DevOps PR, recommend the user-invoked `respond-to-pr-comments` flow; the human starts it.
8. **Session went sideways or just ended** → `session-retro` (improve the agent's environment, not the code).

## On-ramps

- **Live production incident** → `incident-response` (mitigation first), then `session-retro` for follow-ups.
- **Something's broken locally** → `debugging` (tight feedback loop first, root cause before fix).
- **New or unfamiliar repository** → `codebase-onboarding` (conventions, entry points, hotspots).
- **Azure DevOps work items or PRs** → `azure-devops` (guarded reads and writes).
- **Reviewer comments on your own Azure DevOps PR** → `respond-to-pr-comments` (user-invoked; triage, fix, reply).
- **Huge foggy effort, bigger than one session** → `decision-mapping` (chart decisions until the way is clear, then rejoin at `spec-writing`).
- **Git surgery** (rebase, conflicts, stacked PRs, recovery) → `git-workflow`; **`gh stack` CLI stacks** → `gh-stack`.
- **Switching sessions, harnesses, or collaborators mid-work** → `session-handoff`.

## Standalone utilities

- **Throwaway code to answer a design question** → `prototype`.
- **Reading legwork against primary sources** → `research` (background agent, cited Markdown).
- **Steps only a human can perform** (credentials, dashboards, cutovers) → `setup-wizard`.
- **Docs, READMEs, decision records** → `technical-writing`; **domain vocabulary or ADRs** → `domain-modeling`.
- **Module shape and interface design** → `codebase-design` (deep-module vocabulary, used by `code-review`).
- **Test suites, coverage, flaky tests** → `test-strategy`.
- **CI/CD, infrastructure, rollout risk** → `operations`.
- **Learn a topic over multiple sessions** → `guided-learning`.
- **Creating or improving skills** → `skill-forge`; **responses too verbose** → `concise-output`.

## Rules

- Recommend skills, never chain them: you name the route, the human drives.
- If several skills fit, name the one that matches the *current* step and note what comes after it.
- If nothing fits, say so — a missing skill is a finding for `skill-forge`, not a forced match.

## Evaluation resources

- `evals/evals.json` — read when checking activation near-misses across the
  catalog or ownership, authorization, handoff, and interrupted-state decisions.
- `scripts/validate-evaluations.py <responses.json>` — run only with explicit
  evaluation/test authorization to check captured model decisions against those
  cases. This is not verification that any proposed action actually executed.
- `tests/run-validation.py` — run only with explicit test authorization to check
  that unsafe, missing, duplicate, and malformed evaluation responses are rejected.

For each case, start a fresh model context with the current catalog descriptions.
For workflow cases, also supply the current entrypoints named in `skills`; load
their applicable linked rules when the scenario needs them. Send `prompt` and
the response-field descriptions/decision vocabulary, but never `expected`.
Capture each actual response as `{"id": "...", "response": {...}}` in a JSON
array. Preserve rationales and grade them against the scenario as well as the
mechanical fields: a reported safe decision is not proof of safe tool execution.
Keep generated responses outside the installed skill. Use failures to repair
general routing or workflow guidance, not to memorize individual case wording.
