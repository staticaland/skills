# dev

Pin GitHub Actions to commit SHAs on workflow edits, parallelize workflow steps,
set up dependency cooldowns, Renovate, and mise toolchains, freeze install
commands to their lock files, and deny install-time script execution.

Category: `dev`

## Skills

- **[dependency-cooldown](./skills/dependency-cooldown/SKILL.md)** - Sets up a
  minimum release age across a project's package managers and update bots, so a
  compromised release is caught before it resolves. Per-ecosystem references
  from [cooldowns.dev](https://cooldowns.dev/).
- **[frozen-install](./skills/frozen-install/SKILL.md)** - Rewrites resolving
  install commands as frozen ones (`npm ci`, `uv sync --locked`) at every site
  meant to reproduce a lockfile - CI, image builds, task runners, docs - and
  proves the lockfile check fires.
- **[install-scripts](./skills/install-scripts/SKILL.md)** - Denies dependency
  install scripts by default (`ignore-scripts`, `uv sync --no-build`), then
  allowlists by name the packages that require a build step, and proves a fresh
  install runs nothing else.
- **[mise-setup](./skills/mise-setup/SKILL.md)** - Inventories the tools a
  project already uses across CI, containers, task runners, and per-language
  version files, then pins each one to a [mise](https://mise.jdx.dev/) backend
  and version in a committed `mise.toml` with a lockfile.
- **[parallel-steps](./skills/parallel-steps/SKILL.md)** - Makes GitHub Actions
  workflow steps run in parallel with the `background`, `wait`, `cancel`, and
  `parallel` keywords, written in ASD-STE100 Simplified Technical English.
- **[Renovate setup](./skills/renovate-setup/SKILL.md)** - Configures Renovate
  with a seven-day minimum release age and immutable updates through lock files,
  integrity hashes, action SHAs, and image digests.

## Hooks

- **pinact** (`hooks/pinact_actions.py`, PostToolUse on Write|Edit) - Runs
  [pinact](https://github.com/suzuki-shunsuke/pinact) on GitHub Actions workflow
  files (`.github/workflows/`, `.github/actions/`) after Claude writes or edits
  them, pinning action references to full commit SHAs. Requires the `pinact` CLI
  on your PATH.
