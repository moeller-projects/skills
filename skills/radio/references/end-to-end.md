# End-to-End Python Flow

Set `AZURE_DEVOPS_PAT` in the environment using your platform's shell, then run:

```text
python scripts/generate-handoff.py --pull-request-url "https://dev.azure.com/example-org/example-project/_git/example-repo/pullrequest/123" --work-item-id 456 > ado-handoff.json
```

The emitted JSON can be passed directly to `race-engineer` for spec generation. Requires Python 3.9+; standard library only.
