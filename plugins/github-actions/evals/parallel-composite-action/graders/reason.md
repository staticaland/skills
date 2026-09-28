---
type: llm
weight: 1
---

These facts are true, so do not fail a response because it states them:

- GitHub Actions has the `background`, `wait`, `wait-all`, `cancel`, and
  `parallel` step keywords. They run steps concurrently in a workflow job.
- A composite action cannot use these keywords.

The response keeps the steps of the composite action in sequence. It says that
the reason is that a composite action cannot use the `background` or `parallel`
keywords. The response can also suggest that the user moves the steps into a
workflow job, where the keywords are available. A response that gives only
dependencies between the lint and the tests as the reason fails.
