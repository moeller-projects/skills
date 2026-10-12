# Rule: Kubernetes Safety

> Impact: high

## Description

Favor least privilege, resource discipline, explicit probes, and clear operational ownership when changing Kubernetes workloads.

## Apply When

- The task includes Kubernetes manifests, clusters, or workload design.

## Checks

- Security context, probes, and resource expectations MUST be considered.
- Runtime assumptions such as networking or storage MUST be called out.

## Anti-Pattern

Shipping cluster changes that ignore permissions, health checks, or resource boundaries.
