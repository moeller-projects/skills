# Rule: Performance When Real

> Impact: medium

## Description

Treat performance recommendations as evidence-driven work tied to a measured bottleneck, scale concern, or user-visible latency.

## Apply When

- Performance is raised as a goal or a likely problem.

## Checks

- MUST name the bottleneck, symptom, or metric behind the recommendation.
- MUST NOT trade readability for speculative micro-optimizations.

## Anti-Pattern

Suggesting low-value micro-optimizations with no signal that performance is actually constrained.
