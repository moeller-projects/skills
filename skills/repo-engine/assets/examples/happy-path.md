# Happy-Path Example — Repo Engine

## Scenario

Agent is dropped into an unfamiliar monorepo with three packages: `api`, `worker`, `shared`.

## Input Context

- Root `package.json` with workspaces: `packages/api`, `packages/worker`, `packages/shared`.
- `packages/api/src/index.ts` — Express app entry point.
- `packages/worker/src/index.ts` — BullMQ job processor entry point.
- `packages/shared/src/` — shared DTOs and utilities.
- CI: GitHub Actions in `.github/workflows/ci.yml`.
- Tests: `vitest` in each package.

## Expected Output

```text
repo_map:
- packages/api: HTTP API layer — Express routes, controllers, middleware
- packages/worker: Async job processor — BullMQ consumers and handlers
- packages/shared: Shared types, DTOs, and utility functions

entrypoints:
- packages/api/src/index.ts: starts Express HTTP server on PORT env var
- packages/worker/src/index.ts: registers BullMQ processors and starts listening

conventions:
- TypeScript strict mode: tsconfig.json at repo root with strict: true
- Tests: vitest; test files colocated with source as *.test.ts
- Shared types imported from @repo/shared; no cross-package circular deps observed
- CI: lint → test → build in that order per .github/workflows/ci.yml

hotspots:
- packages/shared/src/types.ts: central DTO definitions; changes here affect all packages
- packages/api/src/middleware/auth.ts: auth middleware wired to every route; high blast radius
- packages/worker/src/handlers/: job handler registration; frequently extended

agent_artifacts:
- AGENTS.md (if present): check for agent-specific guidance before making changes
- .github/workflows/ci.yml: defines exact lint/test/build commands for this repo
```

## Why This Is Correct

- Covers all three domains without fabricating missing information.
- Entrypoints are file-level and command-accurate.
- Conventions are observed, not assumed.
- Hotspots have concrete reasons.
- Agent artifacts point to immediately actionable resources.
