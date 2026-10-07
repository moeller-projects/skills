# Rule Order

Read output should preserve these stages in order:

1. Input resolution
2. Auth validation
3. Fetch
4. Normalize
5. Emit contract or blocker

Write output should preserve these stages in order:

1. Input resolution
2. Safety gate
3. Dry-run action plan
4. Optional execute
5. Azure DevOps response or structured error
