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
- When a plugin's contents change, bump its `version` in both its `plugin.json`
  and its entry in `marketplace.json` - installed users only see updates when
  the version changes.

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
- A new vendored path goes in four lists, or a check will fight the next sync:
  `.prettierignore`, `ignores` in `.markdownlint-cli2.yaml`, the vale `exclude`
  in `.pre-commit-config.yaml`, and the vale `glob` in
  `.github/workflows/vale.yml`.

## Validation

Validate the marketplace structure before committing:

```bash
claude plugin validate .
```
