---
name: yaml-anchors
description:
  Replace repeated configuration in a GitHub Actions workflow with YAML anchors
  and aliases, and route the duplication an alias cannot reach to a matrix,
  composite action, reusable workflow, or workflow template. Use when the user
  wants a shorter workflow, mentions YAML anchors, or writes the same env,
  services, matrix, permissions, path filter, or steps in more than one job.
version: 0.1.0
---

# YAML Anchors

GitHub Actions parses workflow YAML with anchors and aliases since
[18 September 2025](https://github.blog/changelog/2025-09-18-actions-yaml-anchors-and-non-public-workflow-templates/).
An anchor (`&name`) marks a node and an alias (`*name`) copies that node whole.
GitHub rejects the merge key (`<<`), so an alias overrides nothing: a copy that
differs by one key is out of an anchor's reach.

An anchor also resolves inside one file. Duplication that spans files belongs to
a composite action, a reusable workflow, or a workflow template - the same
changelog opened templates to non-public `.github` repositories.

## Procedure

### 1. Inventory the repeated blocks

Read every workflow in `.github/workflows/`. Find the configuration written more
than once and record each copy's file, job, and key. These keys hold most of the
duplication.

- `env` maps shared by jobs
- `services` containers, such as a database or a cache
- `strategy.matrix`
- `permissions`
- `paths`, `paths-ignore`, and `branches` filters under `on.push` and
  `on.pull_request`
- `runs-on`, when it names a set of self-hosted labels
- the run of steps that opens each job: checkout, toolchain setup, cache restore
- a whole job

Compare the copies of each block key by key and mark them identical or
different. Done when every repeated block has a site list and that verdict.

### 2. Route each block

| Repeated block                            | Sites           | Mechanism                                                        |
| ----------------------------------------- | --------------- | ---------------------------------------------------------------- |
| A value every job in the file needs       | 1 file          | workflow-level `env`                                             |
| Identical copies                          | 1 file          | anchor and alias, in step 3                                      |
| Copies that differ                        | 1 file          | `strategy.matrix` over the key that differs, or leave the copies |
| A run of steps                            | 2+ files        | composite action                                                 |
| A whole job                               | 2+ files        | reusable workflow                                                |
| The workflow a new repository starts from | 2+ repositories | workflow template                                                |

Anchor a block of three lines or more. An alias to a one-line value saves one
line and costs the reader a jump to the definition, so write that value out.

[references/reuse-mechanisms.md](references/reuse-mechanisms.md) covers every
mechanism except the anchor. Read it before you write one. Done when every
repeated block has a mechanism.

### 3. Anchor the identical blocks

Copy each workflow before you change it, so step 4 compares against the file as
it stood. `git show HEAD:<file>` returns the committed file, which is a
different document whenever the working tree already carries an edit.

```bash
cp .github/workflows/ci.yml /tmp/before.yml
```

- **Define on the first copy.** Put `&name` on the first copy in document order
  and `*name` on each later copy. The parser resolves an alias against an anchor
  it has already read, so a definition under its own alias fails.
- **Anchor configuration that is already doing a job.** A workflow accepts eight
  top-level keys - `name`, `run-name`, `on`, `permissions`, `env`, `defaults`,
  `concurrency`, and `jobs` - so a workflow has nowhere to park a block of
  definitions.
- **Name the anchor after its content**, such as `&env_vars` or `&code_paths`.
  A reorder of the file moves the definition to a different site.
- **Alias whole nodes.** An alias replaces a node. It appends to no list and
  overrides no key.
- **Keep the anchored expressions context-free.** An alias copies `${{ ... }}`
  as text, and the expression evaluates against the job that holds the alias, so
  `${{ matrix.node }}` inside an anchor expands to nothing in a job that has no
  matrix.

Done when each anchor has at least one alias, and each alias resolves to an
anchor written earlier in the file.

### 4. Verify

Run `actionlint` on each changed workflow.

```bash
actionlint .github/workflows/ci.yml
```

It reads anchors and aliases, and it reports a merge key by name:
`GitHub Actions does not support YAML merge key "<<"`. A YAML library reports
nothing there, because PyYAML follows YAML 1.1 and expands `<<` in silence.

Then prove the rewrite didn't change behavior. The copy from step 3 and the new
file expand to the same data, or the rewrite dropped something.

```bash
python3 -c '
import sys, yaml
before, after = (yaml.safe_load(open(p)) for p in sys.argv[1:])
sys.exit(0 if before == after else "workflows differ")
' /tmp/before.yml .github/workflows/ci.yml
```

The comparison reads PyYAML, a third-party package. Where `import yaml` raises
`ModuleNotFoundError`, run the same script through
`uv run --with pyyaml python -c` instead.

`zizmor` 1.29 audits every alias site and prints each finding at the anchor's
line. A finding repeated on one line describes a different job each time.

Report the blocks that stay duplicated and the reason for each.

## Example

```yaml
on:
  push:
    paths: &code_paths
      - "src/**"
      - "package.json"
  pull_request:
    paths: *code_paths

jobs:
  test:
    runs-on: ubuntu-latest
    services: &postgres
      db:
        image: postgres:18
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v6
      - run: npm test

  integration:
    runs-on: ubuntu-latest
    services: *postgres
    steps:
      - uses: actions/checkout@v6
      - run: npm run test:integration
```

[Reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)
is the source of truth for anchors, reusable workflows, and workflow templates.
If a rule here disagrees with that page, obey the page.
