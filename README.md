# Agent skills

Reusable instructions for coding agents. Each skill's `SKILL.md` describes when to use it and how to work; supporting rules, references, examples, scripts, and checks live alongside it.

Skills are named after race crew roles — each name reflects the skill's job in the delivery pipeline.

## Get started

1. Choose a skill from the catalog below and copy its entire `skills/<name>/` directory into the skills directory supported by your agent. The destination depends on the agent; this repository does not provide an installer.
2. Open the copied `SKILL.md` and use its `description` to decide when it applies. Follow its workflow and consult linked files relative to that skill directory.
3. Keep the whole directory together: some skills use `rules/`, `references/`, `assets/`, or `scripts/` in addition to `SKILL.md`.

## Skill catalog

| Skill | Role | Use it for |
| --- | --- | --- |
| [spotter](skills/spotter/) | strategy | Clarifying vague problems and comparing options before commitment |
| [race-engineer](skills/race-engineer/) | strategy | Requirements, acceptance criteria, and OpenSpec proposals |
| [crew-chief](skills/crew-chief/) | strategy | Breaking confirmed scope into tasks, dependencies, and done criteria |
| [co-driver](skills/co-driver/) | recon | Repository discovery, conventions, entry points, and hotspots |
| [mechanic](skills/mechanic/) | car | Code review, refactoring, security, and evidence-backed performance |
| [scrutineer](skills/scrutineer/) | compliance | Pull request and changeset review with author-facing verdicts |
| [test-driver](skills/test-driver/) | car | Test strategy, coverage, E2E flows, and flaky-test reduction |
| [press-officer](skills/press-officer/) | comms | READMEs, agent instructions, developer guides, and decision records |
| [pit-crew](skills/pit-crew/) | trackside | CI/CD, infrastructure, rollout safety, and operational risk |
| [safety-car](skills/safety-car/) | trackside | Live incident response: triage, mitigation, timeline, postmortem follow-ups |
| [radio](skills/radio/) | comms | Azure DevOps work items and PR discussion; guarded, approved writes |
| [pit-board](skills/pit-board/) | comms | Action-first, concise response style that preserves accuracy and safety |

### Renames in 2.0.0

All skills were renamed from their 1.x `*-engine` / gateway names:

| 1.x name | 2.0.0 name |
| --- | --- |
| thinking-engine | spotter |
| spec-engine | race-engineer |
| delivery-engine | crew-chief |
| repo-engine | co-driver |
| code-quality-engine | mechanic |
| test-engine | test-driver |
| doc-engine | press-officer |
| ops-engine | pit-crew |
| ado-gateway | radio |
| bluf | pit-board |

`scrutineer` and `safety-car` are new in 2.0.0.

## Contributing

See [AGENTS.md](AGENTS.md) for the skill layout, version rules, and change workflow. All skills except `pit-board` include a `tests/run-validation.py` script; run it from the skill directory when validating a change to that skill. There is no repository-wide build or test command in this tree.

## License

[MIT](LICENSE).
