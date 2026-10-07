# Repo Engine — Output Template

## Default (repo_map + entrypoints + conventions + hotspots + agent_artifacts)

```text
repo_map:
- <domain or package> — <one-line description of responsibility>

entrypoints:
- <file or command> — <what it starts or exposes>

conventions:
- <area> — <rule or pattern observed>

hotspots:
- <file or area> — <reason it is high-change or high-risk>

agent_artifacts:
- <artifact name> — <what it contains and how to use it>
```

## Compact (same contract, fewer entries)

```text
repo_map:
- <repo or package> — <stack and structure summary>

entrypoints:
- <main entry point> — <what it starts>

conventions:
- build/test/lint — <verified commands or "unavailable">

hotspots:
- <top file or area> — <why it matters first>

agent_artifacts:
- <artifact> — <how it accelerates onboarding>
```

## Rules

- State inaccessible paths explicitly; do not silently skip them.
- Base conventions only on observed patterns, not assumptions.
- Hotspots must have a concrete reason (high churn, cross-cutting, critical path).
- Agent artifacts must be immediately usable without further clarification.
