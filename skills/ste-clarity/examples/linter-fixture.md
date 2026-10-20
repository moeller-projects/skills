# Linter Test Fixture

This file violates the linter rules on purpose. Run:

```bash
python3 scripts/ste_lint.py examples/linter-fixture.md
```

Expected: findings for semicolon, phrasal-verb, marketing-adjective,
nominalization, complex-preposition, long-sentence, synonym-rotation, and
dangling-conjunction, plus advisory findings for passive-voice and
present-perfect. The fenced code block below must produce no findings.

## Prose violations

The report is generated; spin up the worker to utilize the seamless pipeline.
Perform an analysis of the log prior to the deployment.
We have received the confirmation from the upstream service.
This sentence is deliberately written to be far too long because it keeps adding more and more clauses and ideas until it clearly exceeds the twenty five word hard cap that the structural rules impose on descriptive text.
Use the configuration file. Then utilize the output.

## Incomplete list items

- Set the target and
- Record the result or

## Fenced code (no findings expected)

~~~text
- This line ends with and
x = a; y = b
~~~
