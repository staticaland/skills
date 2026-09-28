---
type: llm
weight: 1
---

The response contains the full workflow in one YAML code block, and in it:

- The workflow has a top-level `name` that is a short noun phrase, such as `CI`.
- Every job has a `name`. The `test` job's name interpolates
  `${{ matrix.os }}`.
- Every step has a `name` that starts with an imperative verb and describes the
  outcome, not the tool (`Check out the repository`, not `actions/checkout`).
- Every name is in sentence case, has no trailing period, and stays under about
  50 characters. The existing `npm test.` step is rewritten to a name like
  `Run the tests`.
- Step names are unique within each job.
- Job ids (`test`, `lint`) and every `run`, `uses`, and `with` value are
  unchanged.
