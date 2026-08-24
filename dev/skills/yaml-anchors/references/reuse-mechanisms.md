# Reuse mechanisms

Every mechanism a repeated block routes to, except the anchor.
[Reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)
is the source of truth. If a rule here disagrees with that page, obey the page.

## Workflow-level `env`

A value that every job reads belongs in the workflow's own `env` block, where
each job inherits it and a reader finds it at the top of the file. An anchor on
the same value buys nothing and costs a jump.

```yaml
env:
  NODE_VERSION: "24"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "$NODE_VERSION"
```

A value that outlives the file belongs in an organization, repository, or
environment variable, read through the `vars` context.

## `strategy.matrix`

Copies of a job that differ in one or two values belong in a matrix, which varies
those values across runs. An alias copies a node without change.

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [22, 24]
```

## Composite action

A run of steps repeated across files becomes a composite action in
`.github/actions/<name>/action.yml`. Each form that calls it costs something.

- `uses: ./.github/actions/<name>` resolves against the runner's workspace,
  which stays empty until `actions/checkout` runs. A job that calls the action
  first fails on the missing `action.yml`, so an opening sequence that starts
  with checkout cannot move into a `./` action whole: leave the checkout in the
  caller and move the steps that follow it.
- `uses: $/.github/actions/<name>` names the repository of the running workflow
  at the running commit, so a job can call the action before it checks out
  anything. It takes no `@ref`, and GitHub Enterprise Server does not have it.
  `actionlint` 1.7.12 rejects the form as an invalid `uses` value, so a
  repository that lints its workflows pays for this one at the linter.
- A composite action holds steps. Job-level keys - `runs-on`, `services`,
  `strategy`, `permissions` - stay in the calling job.
- Declare the values it needs as `inputs` in `action.yml` and pass them through
  `with`.
- The `secrets` context is unavailable inside a composite action. A secret
  reaches it as an input.
- The `background`, `wait`, `wait-all`, `cancel`, and `parallel` keywords of the
  [parallel-steps](../../parallel-steps/SKILL.md) skill are unavailable inside a
  composite action.

## Reusable workflow

A whole job repeated across files becomes a reusable workflow, called at job
level.

```yaml
jobs:
  call-test:
    uses: octo-org/repo/.github/workflows/test.yml@v1
    with:
      node-version: "24"
    secrets: inherit
```

- The called workflow declares `on.workflow_call` with its `inputs`, `secrets`,
  and `outputs`.
- The calling job accepts these keys only: `name`, `uses`, `with`, `secrets`,
  `strategy`, `needs`, `if`, `concurrency`, and `permissions`.
- The caller's workflow-level `env` does not reach the called workflow, and the
  called workflow's `env` does not reach the caller. Pass values as `inputs` and
  read results as `outputs`.
- `GITHUB_TOKEN` permissions narrow down the chain. A called workflow holds the
  caller's permissions or fewer.
- A workflow file calls at most 50 unique reusable workflows, counting every
  nested tree, and nests at most 10 levels deep. GitHub Enterprise Server allows
  20 and 4.
- A caller reaches a reusable workflow in its own repository, in a public
  repository, or in an internal or private repository whose Actions access
  policy names the caller's repository.

## Workflow template

The workflow a new repository starts from lives in the organization's `.github`
repository, under `workflow-templates/`.

- Each template is a workflow file plus a metadata file of the same name ending
  in `.properties.json`, both in `workflow-templates/`.
- `$default-branch` in the template is replaced with the repository's default
  branch when somebody creates the workflow.
- A template seeds a copy. The copy doesn't link back, so editing the template
  leaves every workflow already created from it untouched. Reach for a reusable
  workflow when the logic must stay shared.

Since the
[18 September 2025 changelog](https://github.blog/changelog/2025-09-18-actions-yaml-anchors-and-non-public-workflow-templates/),
a non-public `.github` repository can hold workflow templates. A template is
available to repositories that match the template repository's visibility or are
more restricted.

| `.github` repository | Repositories that can use its templates |
| -------------------- | --------------------------------------- |
| public               | public, internal, and private           |
| internal             | internal and private                    |
| private              | private                                 |

- Grant Read on a private or internal `.github` repository to the users and
  teams who should see its templates.
- The rule covers Actions. Other GitHub products still read templates from a
  public `.github` repository.
- Enterprise Managed Users own no public repositories, so public workflow
  templates are unavailable to them.
