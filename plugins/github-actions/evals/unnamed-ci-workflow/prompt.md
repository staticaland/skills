---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Add names to this GitHub Actions workflow. Reply with the full updated file in
one YAML code block.

```yaml
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - name: npm test.
        run: npm test
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
```
