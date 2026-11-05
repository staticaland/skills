# dependencies

Harden how dependencies arrive with cooldowns, Renovate, frozen installs, and
denied install scripts, and adopt barely used ones into the repo.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install dependencies@staticaland-skills
```

## Skills

- **[dependency-cooldown](./skills/dependency-cooldown/SKILL.md)**
  (skill) - Sets up a minimum release age across a project's package
  managers and update bots, so a compromised release is caught before it
  resolves. Per-ecosystem references from
  [cooldowns.dev](https://cooldowns.dev/).
- **[Renovate setup](./skills/renovate-setup/SKILL.md)** (skill) -
  Configures Renovate with a seven-day minimum release age and immutable updates
  through lock files, integrity hashes, action SHAs, and image digests.
- **[frozen-install](./skills/frozen-install/SKILL.md)** (skill) -
  Rewrites resolving install commands as frozen ones (`npm ci`,
  `uv sync --locked`) at every site meant to reproduce a
  lockfile - CI, image builds, task runners, docs - and proves the
  lockfile check fails when the lockfile drifts.
- **[install-scripts](./skills/install-scripts/SKILL.md)** (skill) -
  Denies dependency install scripts by default (`ignore-scripts`,
  `uv sync --no-build`), then allowlists by name the packages that
  build something, and proves a fresh install runs nothing else.
- **[adopt-small-dependencies](./skills/adopt-small-dependencies/SKILL.md)**
  (skill) - Finds dependencies the repo uses for a function or two, then
  copies that code in with its source and licence, or rewrites it with the
  standard library, and drops the dependency.

## License

MIT
