---
type: llm
weight: 1
---

GitHub Actions has these step keywords. They are valid syntax, so do not
fail a response because it uses them:

- `background: true` starts a step and continues to the next step at once.
- `wait: <id>` or `wait: [<id>, ...]` stops until the background steps that it
  names complete. After it, their outputs are available.
- `wait-all:` stops until all the earlier background steps complete.
- `cancel: <id>` stops a background step.
- `parallel:` holds a list of steps that run concurrently. The job continues
  after the block only when all of them complete.

The response says that the steps must stay in sequence. It gives a reason for
each step. The reason names a result of the step before it that the step
needs, such as the checked-out files, the installed dependencies, the build
output, or the tarball.
