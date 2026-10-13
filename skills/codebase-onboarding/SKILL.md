---
name: codebase-onboarding
description: Use when onboarding to a repository, mapping architecture, or extracting entry points, conventions, hotspots, and agent artifacts. Do not use when exact files are already known, the question is strategic rather than repository-specific, or the request is to author onboarding or AGENTS.md docs.
metadata:
  title: Codebase Onboarding
  version: "1.0.5"
  summary: Map repository architecture, entry points, conventions, hotspots, and onboarding artifacts for fast execution.
---

# Codebase Onboarding

## Purpose

Scan repositories, infer architecture, detect entry points, extract conventions, identify hotspots, and produce onboarding artifacts that accelerate future work.

## Workflow
1. Scan the repo layout, build system, and major domains; if access is restricted, note the gap and continue with available areas.
2. Identify entry points, ownership seams, and runtime paths.
3. Extract conventions, workflows, and recurring patterns.
4. Highlight hotspots, risks, and likely change surfaces.
5. Package the findings into reusable onboarding artifacts.

## Output Contract

The canonical output is sectioned text (not JSON):

```text
repo_map:
- area or package — one-line responsibility and observed scope

entrypoints:
- path or command — why it matters and kind (runtime, build, test, or CI)

conventions:
- observed convention with a concrete source or example

hotspots:
- area — concrete change risk and reason

agent_artifacts:
- artifact — how to use it
```

Every section MUST contain substantive entries. If a section genuinely has no applicable content, use exactly `- none`; do not use empty lists or infer absence from omitted sections. Each section is validated independently, and entries MUST describe observed repository content rather than generic advice.

## Handoffs

- Hand off to `code-review`, `test-strategy`, `technical-writing`, or `operations` once the repository map identifies the concrete code, test, documentation, or operational surface to change.
- Hand off to `discovery` instead when the next question is strategic or cross-repository rather than repository-specific.

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

- `assets/templates/output.md` — read when formatting the onboarding artifact.
- `assets/examples/happy-path.md` — read for a monorepo onboarding example.
- `assets/examples/edge-case.md` — read when access is partial or paths are restricted.
- `scripts/validate-output.py` — run when validating an onboarding artifact.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to validate skill output.
- `tests/validation-checklist.md` — read when checking the skill's validation requirements.

## References

- `references/examples.md` — read for sample repository maps.
- `references/artifact-schema.md` — read when producing or checking the output schema.

## Rules

- `rules/_sections.md` — read when structuring rule content.
- `rules/architecture-map.md` — read when mapping architecture.
- `rules/entrypoint-detection.md` — read when detecting entry points.
- `rules/convention-extraction.md` — read when extracting conventions.
- `rules/hotspot-identification.md` — read when identifying hotspots.
