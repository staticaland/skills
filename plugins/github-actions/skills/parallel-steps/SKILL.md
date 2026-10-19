---
name: parallel-steps
description:
  Run GitHub Actions steps in parallel with the background, wait, wait-all,
  cancel, and parallel keywords. Use when the user wants a faster job, starts a
  service in a job, or asks for background or parallel steps.
version: 0.2.0
---

# Parallel Steps

Keywords: `background: true`, `wait: <id>`, `wait-all:`, `cancel: <id>`, and a bare `- parallel:` item of steps.

Parallelize steps that do not read each other's output. A background step's outputs exist only after a `wait` or `wait-all` that includes it. Background a server with an `id`, then stop it with a `cancel: <id>` step that has a `name`. Background a step nothing reads. If none can move, change nothing and say why.

<!-- vale ai-tells.NounString = NO -->
<!-- The rule counts the masked code spans as nouns. Evals show that this
     wording keeps the model from shell workarounds in a composite action. -->

A composite action cannot use `background` or `parallel`. `actionlint` does not know these keywords yet ([rhysd/actionlint#693](https://github.com/rhysd/actionlint/issues/693)), so keep the keywords when it reports them and ignore those errors in `.github/actionlint.yaml`. The [workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) is the source of truth.

<!-- vale ai-tells.NounString = YES -->
