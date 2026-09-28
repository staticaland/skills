---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This CI job is slow. The dependency scan and the tests each take about five
minutes. Make the job faster by running steps concurrently where it is safe.
Keep it as one job. Reply with the full updated file in one YAML code block.

```yaml
name: CI

on: [push]

jobs:
  check:
    name: Check
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repository
        uses: actions/checkout@v4
      - name: Install dependencies
        run: npm ci
      - name: Scan the dependencies
        id: scan
        run: echo "findings=$(./scripts/scan.sh | wc -l)" >> "$GITHUB_OUTPUT"
      - name: Run the tests
        run: npm test
      - name: Report the scan findings
        run: echo "Found ${{ steps.scan.outputs.findings }} issues" >> "$GITHUB_STEP_SUMMARY"
```
