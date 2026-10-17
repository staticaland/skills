---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

`actionlint` fails on this workflow. Fix it so that CI is green. Reply with the
full `ci.yml` in one YAML code block, and with each other file that you change.

```yaml
name: CI

on: [push]

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repository
        uses: actions/checkout@v4
      - name: Install dependencies
        run: npm ci
      - name: Start the test server
        id: server
        run: npm run start
        background: true
      - parallel:
          - name: Run the E2E tests
            run: npm run e2e
          - name: Run the unit tests
            run: npm test
      - name: Stop the server
        cancel: server
```

The `actionlint` output:

```text
.github/workflows/ci.yml:17:9: unexpected key "background" for step to run shell command. expected one of "continue-on-error", "env", "id", "if", "name", "run", "shell", "timeout-minutes", "working-directory" [syntax-check]
.github/workflows/ci.yml:18:9: step must run script with "run" section or run action with "uses" section [syntax-check]
.github/workflows/ci.yml:23:9: step must run script with "run" section or run action with "uses" section [syntax-check]
```
