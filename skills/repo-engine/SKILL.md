---
name: repo-engine
description: Use when onboarding to a repository, mapping architecture, or extracting entry points, conventions, hotspots, and agent artifacts. Do not use when exact files are already known, the question is strategic rather than repository-specific, or the request is to author onboarding or AGENTS.md docs.
allowed-tools:
  - list_dir
  - read_file
title: Repo Engine
version: 5.0.1
summary: Map repository architecture, entry points, conventions, hotspots, and onboarding artifacts for fast execution.
---

# Repo Engine

## Purpose

Scan repositories, infer architecture, detect entry points, extract conventions, identify hotspots, and produce onboarding artifacts that accelerate future work.

## Use When

- Onboarding into a repository or monorepo.
- Understanding architecture before making changes.
- Mapping entry points and execution flows.
- Extracting conventions and development hotspots.
- Producing agent-ready onboarding artifacts.

## Avoid When

- The user already provided exact files for a small patch.
- Only code quality review is needed.

## Workflow

1. Scan the repo layout, build system, and major domains; if access is restricted, note the gap and continue with available areas.
2. Identify entry points, ownership seams, and runtime paths.
3. Extract conventions, workflows, and recurring patterns.
4. Highlight hotspots, risks, and likely change surfaces.
5. Package the findings into reusable onboarding artifacts.

## Output Contract

Default:

```text
repo_map:
- ...

entrypoints:
- ...

conventions:
- ...

hotspots:
- ...

agent_artifacts:
- ...
```

## Handoffs

- Hand off to `code-quality-engine`, `test-engine`, `doc-engine`, or `ops-engine` once the repository map identifies the concrete code, test, documentation, or operational surface to change.
- Hand off to `thinking-engine` instead when the next question is strategic or cross-repository rather than repository-specific.

## Error Handling

1. Local: If a directory or file is inaccessible, note the gap and continue scanning available areas.
2. Flow: Skip restricted paths; flag each one in the output artifact.
3. Recovery: Restart the scan from the top-level structure if partial output is inconsistent.

## Validation Checklist

- [ ] Every major domain listed with a one-line description.
- [ ] Inaccessible paths flagged explicitly, not silently skipped.
- [ ] Conventions are observed from actual files, not assumed.
- [ ] Each hotspot has a concrete reason.
- [ ] Agent artifacts are immediately usable without further clarification.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — monorepo onboarding scenario
- `assets/examples/edge-case.md` — partial access / restricted paths scenario
- `scripts/validate-output.py` — validates output structure

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/artifact-schema.md` for the output schema.
- See `references/examples.md` for sample repo maps.

## Rules

- `rules/_sections.md`
- `rules/architecture-map.md`
- `rules/entrypoint-detection.md`
- `rules/convention-extraction.md`
- `rules/hotspot-identification.md`
