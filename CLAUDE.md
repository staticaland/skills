# Skills Marketplace

This repo is a multi-plugin Claude Code marketplace. Each category directory
(`writing/`, `dev/`, `ai/`, or `other/`) is an
independently installable plugin with its own `.claude-plugin/plugin.json`.

## Structure rules

- Every available plugin directory must have an entry in
  `.claude-plugin/marketplace.json` and a section in the top-level `README.md`
  catalog.
- Every plugin has its own `README.md` listing each of its skills and hooks with
  a one-line description. Skill names link to their `SKILL.md`, both in the
  plugin README and in the top-level catalog.
- Every marketplace entry has one lowercase category: `writing`, `dev`, `ai`, or
  `other`. Every published skill and hook in a plugin must belong to that
  category.
- Draft and retired plugins must NOT appear in `marketplace.json` or the
  top-level README catalog.
- Never bump a plugin's `version` in a feature PR. release-please computes the
  bump from the conventional commit history and opens a release PR that writes
  it into `plugin.json`; merging that PR is what publishes the update to
  installed users.
- `plugin.json` is the source of truth for a plugin's `version` and
  `description`. Its entry in `marketplace.json` and any
  `.codex-plugin/plugin.json` (the manifest Codex requires) are derived: after
  editing a description, run `scripts/sync-manifests.py`. The sync-manifests
  prek hook fails while a derived file is stale.

## Vendored skills

Some skills come from another repository. [`vendir.yml`](vendir.yml) lists them,
and each one keeps an `UPSTREAM.md` naming its source and license.

- Never hand-edit a vendored skill. `vendir sync` overwrites every path
  `vendir.yml` lists, except the `ignorePaths` that hold `UPSTREAM.md`.
- To update one, change its `ref` to a new upstream commit and sync that
  directory: `vendir sync -d dev/skills/grilling`. Commit `vendir.lock.yml`
  with the synced files.
- Name no upstream commit outside `vendir.yml` and `vendir.lock.yml`. A version
  repeated in an `UPSTREAM.md` goes stale the next time a `ref` moves.
- A new vendored path goes in three lists, or a check will fight the next
  sync: `.prettierignore`, `ignores` in `.markdownlint-cli2.yaml`, and the
  empty-styles section in `.vale.ini`.

## Validation

Run every check through prek - `prek.toml` already wraps each tool (formatting,
linting, plugin validation) and installs the pinned toolchain first, so prek is
the one entrypoint instead of invoking tools directly:

```bash
mise exec -- prek run --all-files
```

To re-run one hook, name its id from `prek.toml`:
`mise exec -- prek run vale --all-files`.
