---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This CI job is slow. Make it faster by running steps concurrently where it is
safe. Keep it as one job. Reply with the full updated file in one YAML code
block.

Facts about the steps:

- `npm run start` starts a server that serves the built app. It runs until
  something stops it.
- The E2E tests need the built app and the running server.
- The docs build reads only the source files.
- No step reads anything that the telemetry step produces.

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
      - name: Build the app
        run: npm run build
      - name: Build the docs
        run: npm run docs
      - name: Start the test server
        run: npm run start
      - name: Run the E2E tests
        run: npm run e2e
      - name: Send usage telemetry
        run: ./scripts/send-telemetry.sh
```
