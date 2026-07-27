# Keyword reference

This document obeys ASD-STE100 Simplified Technical English. Write all prose that you add to it in the same style.

The [workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) is the source of truth. If a keyword does not agree with this document, obey the reference.

## `background`

`background: true` runs a step asynchronously. The job continues to the next step and does not wait for the step to finish. Use it for a long-running process, for example a database, a server, or a monitoring task, that must run at the same time as other steps.

You can use `background` on a step that uses `run` or a step that uses `uses`. To refer to a background step from `wait` or `cancel`, give the step an `id`.

A maximum of 10 background steps run at the same time in one job. The runner queues the other background steps until a slot is free.

The outputs and the environment changes of a background step become available only after a `wait` step or a `wait-all` step that includes it. If a background step fails, the job fails at the next `wait` or `wait-all` that includes it, unless `continue-on-error` is set on that step. An implicit `wait-all` runs before the post-job cleanup.

You cannot use `background` on a step inside a composite action. A composite action can run as a background step, but it cannot declare background steps inside itself.

```yaml
steps:
  - name: Start server
    id: server
    run: npm start
    background: true

  - name: Run tests against the server
    run: npm test

  - name: Wait for the server step to finish
    wait: server
```

## `wait`

`wait` stops the job until one or more background steps complete. A `wait` step does no work. It only blocks until the named background steps finish. Give one step `id` as a string, or more than one step `id` as an array.

After a `wait` step completes, the outputs of the named background steps become available to the steps that come after. If a named background step failed, the `wait` step also fails.

A `wait` step always runs. It does not support the `if` conditional.

```yaml
steps:
  - name: Build frontend
    id: build-frontend
    run: npm run build:frontend
    background: true

  - name: Build backend
    id: build-backend
    run: npm run build:backend
    background: true

  - name: Run linter while builds run
    run: npm run lint

  - name: Wait for both builds to finish
    wait: [build-frontend, build-backend]

  - name: Run tests
    run: npm test
```

## `wait-all`

`wait-all` stops the job until all the active background steps complete. Use it when more than one background step runs and all of them must finish before the job continues. Like `wait`, the `wait-all` step fails if a background step that it waits on failed, unless you set `continue-on-error` to true.

The `wait-all` keyword takes no arguments.

A `wait-all` step always runs. It does not support the `if` conditional.

```yaml
steps:
  - name: Start database
    id: db
    run: docker run -d postgres:15
    background: true

  - name: Start cache
    id: cache
    run: docker run -d redis:7
    background: true

  - name: Run integration tests
    run: npm run test:integration

  - name: Wait for all services to stop
    wait-all:
```

## `cancel`

`cancel` stops a running background step in a controlled way. The runner sends the process of the step a termination signal (`SIGTERM`) so that it can clean up. The runner forcibly stops the process (`SIGKILL`) if it does not exit in a short grace period. The `cancel` keyword targets one background step by its `id`.

A `cancel` step always runs. It does not support the `if` conditional.

```yaml
steps:
  - name: Start long-running monitor
    id: monitor
    run: ./scripts/monitor.sh
    background: true

  - name: Run the main task
    run: npm test

  - name: Stop the monitor
    cancel: monitor
```

## `parallel`

`parallel` runs a group of steps at the same time, then waits for all of them to finish before the job continues. The `parallel` keyword is shorthand: every step in the group runs as a background step, with an implicit `wait` at the end of the group. Use it when you have an independent group of steps that can run at the same time and you do not need to refer to them one at a time.

Use `parallel` for a self-contained group of steps that must all finish before the job continues, for example a build of the frontend, the backend, and the docs at the same time. Use `background` when you need finer control: a long-running process that stays up while later steps run, a reference to one specific step with `wait` or `cancel`, or background work between other steps. In short, `parallel` is more limited but more convenient for the "run this group at once" case. `background` is the general-purpose primitive.

Each step in the group has the same 10-step concurrency limit as the other background steps.

You cannot use `parallel` inside a composite action.

```yaml
steps:
  - uses: actions/checkout@v6

  - parallel:
      - name: Build frontend
        run: npm run build:frontend

      - name: Build backend
        run: npm run build:backend

      - name: Build docs
        run: npm run build:docs

  - name: Run tests after all builds complete
    run: npm test
```

The group above is equal to a declaration of each step with `background: true`, then a `wait` step.

## Tool support

`actionlint` does not support these keywords yet. See [rhysd/actionlint#693](https://github.com/rhysd/actionlint/issues/693). The tool can report an error or a warning on a workflow that uses `background`, `wait`, `wait-all`, `cancel`, or `parallel`. Do not remove a keyword that agrees with this reference because of an `actionlint` message.
