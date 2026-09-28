---
type: llm
weight: 1
---

These facts are true, so do not fail a response because it states them:

- GitHub Actions has the `background`, `wait`, `wait-all`, `cancel`, and
  `parallel` step keywords. They are valid syntax.
- `actionlint` does not support these keywords yet, so it reports errors on
  them.
- An `.github/actionlint.yaml` file can ignore errors by message for each path.

The response says that the `actionlint` errors are false positives because
`actionlint` does not support these keywords yet. The fix that it recommends
keeps the keywords. It can add an `actionlint` configuration that ignores the
errors. It can mention the removal of the keywords as a fallback.
