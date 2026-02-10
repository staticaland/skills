# Extended Patterns and Examples

## Before and After Pinning

### Basic CI Workflow

**Before (mutable tags):**

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm ci
      - run: npm test
```

**After (pinned to SHAs):**

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
        with:
          node-version: "20"
      - run: npm ci
      - run: npm test
```

### Docker Build and Push

**Before:**

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

**After:**

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: docker/setup-buildx-action@b5ca514318bd6ebac0fb2aedd5d36ec1b5c232a2 # v3.10.0
      - uses: docker/login-action@74a5d142397b4f367a81961eba4e8cd7edddf772 # v3.4.0
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@263435318d21b8e681c14492fe198e19c816612b # v6.18.0
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

### Release with GitHub Pages

**Before:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install mkdocs-material
      - run: mkdocs build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site/
      - uses: actions/deploy-pages@v4
```

**After:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0
        with:
          python-version: "3.12"
      - run: pip install mkdocs-material
      - run: mkdocs build
      - uses: actions/upload-pages-artifact@56afc609e74202658d3ffba0e8f6dda462b719fa # v3.0.1
        with:
          path: site/
      - uses: actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac2b3c603fc # v4.0.5
```

## Hook Script Behavior

### What Gets Pinned

The hook triggers on files matching these paths:

- `.github/workflows/*.yml`
- `.github/workflows/*.yaml`
- `.github/actions/*.yml`
- `.github/actions/*.yaml`

### What Gets Skipped

The hook does **not** modify:

- Non-YAML files
- Files outside `.github/workflows/` and `.github/actions/`
- Actions already pinned to full SHAs
- Refs like `@main`, `@master`, or branch names (non-semantic versions)
- Local actions (`uses: ./`)

## Common Patterns

### Third-Party Actions

Third-party actions are the highest-risk targets for supply chain attacks. Always pin these:

```yaml
# Before
- uses: aws-actions/configure-aws-credentials@v4
- uses: google-github-actions/auth@v2

# After
- uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502 # v4.0.2
- uses: google-github-actions/auth@ba79af03959ebeac9769e648f473a284504d9193 # v2.1.10
```

### Composite Actions

Composite actions in `.github/actions/` also benefit from pinned dependencies:

```yaml
# .github/actions/setup/action.yml
runs:
  using: composite
  steps:
    # Before
    - uses: actions/setup-node@v4
    # After
    - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
```

### Reusable Workflows

Reusable workflow references should also be pinned:

```yaml
jobs:
  lint:
    # Before
    uses: organization/shared-workflows/.github/workflows/lint.yml@v1
    # After
    uses: organization/shared-workflows/.github/workflows/lint.yml@a1b2c3d4e5f6 # v1.3.0
```

## Troubleshooting

### Rate Limiting

If pinact fails with rate limit errors, set a GitHub token:

```bash
export GITHUB_TOKEN="ghp_..."
```

Or configure it in `~/.pinact.yaml`:

```yaml
github_token: ${GITHUB_TOKEN}
```

### Verification

Verify pinning worked correctly:

```bash
# Check a specific workflow
pinact run -u .github/workflows/ci.yml

# Check all workflows
pinact run -u .github/workflows/
```
