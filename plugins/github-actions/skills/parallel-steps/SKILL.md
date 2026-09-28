---
name: parallel-steps
description:
  Make GitHub Actions steps run in parallel with the background, wait, wait-all,
  cancel, and parallel keywords. Use when the user wants a faster job, starts a
  service in a job, or asks for background or parallel steps.
version: 0.2.0
---

# Parallel Steps

Use step keywords, not shell `&`:

- Put independent steps in one `parallel:` block.
- Give a service an `id` and `background: true`. Stop it with `cancel: <id>`.
- Give a step that nothing reads, such as telemetry, `background: true`.
- Put `wait: <id>` before a step that reads a background step.

```yaml
steps:
  - parallel:
      - name: Build
        run: npm run build
      - name: Lint
        run: npm run lint
  - name: Upload metrics
    run: ./metrics.sh
    background: true
  - name: Start server
    id: server
    run: npm run start
    background: true
  - name: Test
    run: npm test
  - name: Stop server
    cancel: server
```
