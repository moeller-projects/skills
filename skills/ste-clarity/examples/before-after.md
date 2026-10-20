# Before / After Examples

Consult these when a rewrite feels lossy and you are unsure whether the guard
rails permit it. Each example names what was flagged and — more important —
what was deliberately not changed.

## Example 1 — Tool description (Strict)

**Before:**
> This tool will attempt to synchronize state across the various backends that have been configured, and if a conflict is detected it may resolve it automatically depending on the strategy that has been set, or otherwise it will surface the conflict for manual review.

**Flagged:** two instructions in one sentence; present perfect in relative
clauses ("have been configured", "has been set"); 44 words, far over the cap.

**Not flagged:** "will attempt to" and "may resolve". Those are hedges, not
violations. The tool is not promised to succeed, and the rewrite must not
promise it either.

> The tool tries to synchronize state across the configured backends. If it detects a conflict, it may resolve the conflict automatically, depending on the configured strategy. Otherwise, it reports the conflict for manual review.

The rewrite keeps the source's conditional resolution and manual-review outcome.

## Example 2 — Error message (Strict): why the modality guard rail exists

**Before:**
> An error may have occurred while processing your request due to a possible mismatch in the expected data format, which could be caused by an outdated client version.

**Flagged:** one sentence carrying three claims; 28 words, over the cap.

**Not flagged:** "may have occurred" and "could be caused by". The system does
not know what went wrong. Both hedges accurately report that ignorance.

> Your request may have failed. The cause may be a mismatch between the data format and the expected format. An outdated client version could cause this mismatch.

The rewrite keeps the source's uncertainty about both the error and its possible cause. It does not recommend a check that the source did not request.

## Example 3 — Inter-agent instruction (Strict)

**Before:**
> Once the upstream job has completed and assuming no errors were raised, the downstream agent should proceed to consume the output artifact, though it is worth noting that partial artifacts are sometimes produced under timeout conditions.

**Flagged:** present perfect ("has completed"); stacked subordinate clauses;
one sentence, three facts; 36 words, over the instruction cap.

> After the upstream job completes with no errors, the downstream agent should read the output artifact. Timeout conditions sometimes produce partial artifacts.

The rewrite keeps the instruction's conditional scope, the original recommendation, and the timeout warning. It does not add a completeness check.

## Example 4 — README prose (Standard)

**Before:**
> Our caching layer is designed to slot seamlessly into your existing stack with minimal friction and no vendor lock-in; it leverages semantic similarity to dramatically reduce the cache misses that traditionally plague LLM workloads.

**Flagged:** marketing claims without measurement ("seamlessly", "minimal
friction", "dramatically"); semicolon joining two ideas; nominalization and
soft phrasing ("is designed to slot into", "leverages"); 34 words.

> The cache is designed to work with your existing stack, with minimal integration effort and no vendor lock-in. It uses semantic similarity to reduce cache misses in LLM workloads. The source says that the reduction is dramatic but gives no measurement.

Standard level kept the explanatory rhythm and did not force one fixed term
per concept. It still cut the marketing adjectives, the semicolon, and the
length.

## Example 5 — Official-style rule illustrations

Paraphrased illustrations of the standard's own rules (not quotes from it):

| Rule | Before | After | Why |
|---|---|---|---|
| One part of speech per word | "Oil the valve." | "Apply oil to the valve." | If "oil" is approved only as a noun, the verb use breaks the one-word-one-role guarantee. |
| Precise verb meaning | "Follow the safety instructions." | "Obey the safety instructions." | "Follow" can mean "come after" or "obey". |
| Simple tense only | "We have received the reports." | "We received the reports." | Present perfect adds a second parse that simple past avoids. |
| No phrasal verbs | "Take off the access panel." | "Remove the access panel." | "Take off" also means "depart" and "deduct". |
