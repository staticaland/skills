---
name: parallel-steps
description:
  Run GitHub Actions steps in parallel with the background, wait, wait-all,
  cancel, and parallel keywords. Use when the user wants a faster job.
version: 0.2.0
---

# Parallel Steps

Keywords: `background: true`, `wait: <id>`, `wait-all:`, `cancel: <id>`, and a bare `- parallel:` item of steps.

Parallelize steps that do not read each other's output. Background a server with an `id`, then `cancel` it. Background a step nothing reads. If none can move, change nothing and say why.
