# Skills Marketplace

This repo is a multi-plugin Claude Code marketplace. Each directory under
`plugins/` is an independently installable plugin with its own
`.claude-plugin/plugin.json`. Plugins are small on purpose: a plugin holds the
skills someone would want together, so installing one drags in as little as
possible.

## Structure rules

- Every available plugin directory under `plugins/` must have an entry in
  `.claude-plugin/marketplace.json` and a section in the top-level `README.md`
  catalog.
- Every plugin has its own `README.md` listing each of its skills and hooks with
  a one-line description. Skill names link to their `SKILL.md`, both in the
  plugin README and in the top-level catalog.
- Every marketplace entry has one lowercase category: `writing`, `dev`, `ai`, or
  `other`. The category groups plugins in the catalog and nothing else. Plugins
  share categories, and a category is not a plugin's directory name.
- A plugin may hold one skill. Prefer that over a catch-all bucket: a skill with
  no siblings is its own plugin, not filler for `other`.
- Draft and retired plugins must NOT appear in `marketplace.json` or the
  top-level README catalog.
- Never bump a plugin's `version` in a feature PR. release-please computes the
  bump from the conventional commit history and opens a release PR that writes
  it into `plugin.json`; merging that PR is what publishes the update to
  installed users.
- Every plugin sits below 1.0.0, and `bump-minor-pre-major` in
  `release-please-config.json` keeps it there. A breaking change bumps the
  minor, so a `feat!` commit moves a plugin from 0.1.0 to 0.2.0, not to 1.0.0.
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
  directory: `vendir sync -d plugins/grilling/skills/grilling`. Commit
  `vendir.lock.yml` with the synced files.
- Do not name an upstream commit outside `vendir.yml` and `vendir.lock.yml`. A version
  repeated in an `UPSTREAM.md` goes stale the next time a `ref` moves.
- A new vendored path goes in four lists, or a check will fight the next
  sync: `.prettierignore`, `exclude` in `.rumdl.toml`, the
  empty-styles section in `.vale.ini`, and `exclude_path` in `lychee.toml`.

## Validation

Run every check through prek - `prek.toml` already wraps each tool (formatting,
linting, plugin validation) and installs the pinned toolchain first, so prek is
the one entrypoint instead of invoking tools directly:

```bash
mise exec -- prek run --all-files
```

prek reads the git index, so `git add` a new file before you run it. The hooks
skip a file outside the index, and the run reports success without checking it.

To re-run one hook, name its id from `prek.toml`:
`mise exec -- prek run vale --all-files`.
