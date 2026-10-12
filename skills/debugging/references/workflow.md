# Debugging Workflow

## 1. Capture and Reproduce

Record the exact command, arguments, input, expected result, observed result, exit code, working directory, dependency/runtime versions, configuration, and relevant state. Reduce to the smallest deterministic reproduction before forming a theory. If it is intermittent, capture repeated runs and timing/state differences.

## 2. Read and Rank Evidence

Read stack traces from the bottom (the initiating exception or causal frame) upward through wrappers and handlers. Treat the top-level error as a symptom until lower-level evidence supports causality. Rank hypotheses by direct observations, changed code, and experiment cost; label assumptions.

## 3. Isolate and Bisect

Change one variable at a time: input, environment, configuration, dependency, or code path. Use `git bisect` for a known-good/known-bad commit range; binary-search inputs or configuration when commits are not the axis. Record each result and keep the repro unchanged while narrowing.

## 4. Confirm, Fix, Verify

Design a falsifiable experiment: the suspected cause must disappear when removed or must recreate the failure when reintroduced. Apply the narrowest fix, rerun the original repro, check adjacent behavior, and add a regression check that captures the causal contract.

## 5. Stop and Escalate

Stop when the issue requires production-only intervention, privileged state, unavailable ownership, unsafe changes, or evidence that cannot distinguish hypotheses locally. Report what was attempted, the last known state, the evidence gap, impact, and the concrete owner/action needed.
