# Example — Multi-Mode Artifact (README with Diátaxis Mode Tags)

## Scenario

Developer asks: "Write a README for our new `payments-service`."

## Input Context

- Service: payment processing microservice, Go + Stripe SDK.
- Endpoints: `POST /charge`, `POST /refund`, `GET /charges/:id`.
- Audience: backend engineers onboarding to the service.
- No existing README.

## Expected Output

```text
doc:
- purpose: enable a backend engineer to install, run, and call payments-service endpoints, and understand why charges are idempotent
- audience: backend engineer, familiar with REST and Go, unfamiliar with this service or Stripe specifics
- structure:
  1. Overview [explanation] — what the service does and why it exists
  2. Prerequisites [reference] — Go version, env vars, Stripe keys
  3. Running locally [tutorial] — first install, configure, start, make a test charge
  4. Common operations [how-to] — refund a charge, retry a failed charge, rotate keys
  5. Endpoint reference [reference] — POST /charge, POST /refund, GET /charges/:id
  6. Idempotency model [explanation] — why charges use idempotency keys, what guarantees are made

changes:
- README.md — created from scratch

gaps:
- production deployment guide (separate doc needed)
- on-call runbook for Stripe outages (separate doc needed)
```

## Why This Is Correct

- Each section is tagged with exactly one mode.
- The artifact is multi-mode (README is a landing page), but no individual section mixes modes.
- "Running locally" is correctly a tutorial — it walks a newcomer through a first success, end-to-end with a test charge.
- "Common operations" is correctly how-to — it assumes the reader knows the service exists and wants to perform a specific task.
- "Idempotency model" is correctly explanation — it answers why, separated from the reference page that simply documents the `Idempotency-Key` header.

## What Would Be Wrong

A single section called "Running and operating the service" combining tutorial steps, refund how-to, and an aside about why idempotency works. Each mode interrupts the others — a newcomer gets ambushed by operational guidance, an operator wades through onboarding material, and the idempotency explanation is buried where no one looking for it will find it. Split into three sections with explicit mode tags.
