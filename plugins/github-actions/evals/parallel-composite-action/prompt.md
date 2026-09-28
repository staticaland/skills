---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This composite action is slow. The lint and the tests each take about three
minutes, and neither reads what the other produces. Make the action faster by
running steps concurrently where it is safe. Reply with the full updated file in
one YAML code block, and give the reason for each step that stays in sequence.

```yaml
name: Check
description: Lint and test the package

runs:
  using: composite
  steps:
    - name: Install dependencies
      run: npm ci
      shell: bash
    - name: Lint the source
      run: npm run lint
      shell: bash
    - name: Run the unit tests
      run: npm test
      shell: bash
```
