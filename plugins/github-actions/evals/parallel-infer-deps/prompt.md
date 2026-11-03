---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This CI job is slow. Make it faster by running steps concurrently where it is
safe. Keep it as one job. Reply with the full updated file in one YAML code
block.

```yaml
name: CI

on: [push]

jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repository
        uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22
      - name: Install dependencies
        run: npm ci
      - name: Build the app into dist
        run: npm run build
      - name: Lint the source
        run: npm run lint
      - name: Run the unit tests
        run: npm test
      - name: Upload dist
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist
```
