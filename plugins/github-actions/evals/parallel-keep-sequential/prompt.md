---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This release job is slow. Make it faster by running steps concurrently where it
is safe. Keep it as one job. Reply with the full updated file in one YAML code
block, and give the reason for each step that stays in sequence.

```yaml
name: Release

on:
  push:
    tags: ["v*"]

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repository
        uses: actions/checkout@v4
      - name: Install dependencies
        run: npm ci
      - name: Build the package
        run: npm run build
      - name: Pack the package into a tarball
        run: npm pack
      - name: Publish the tarball
        run: npm publish ./*.tgz
```
