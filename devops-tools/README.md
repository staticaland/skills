# devops-tools

Pin GitHub Actions to commit SHAs on workflow edits, parallelize workflow steps, set up dependency cooldowns and mise toolchains, freeze install commands to their lockfiles, deny install-time script execution, analyze skills to split scriptable work from judgment work, and refactor skill references for progressive disclosure.

## Skills

- **[dependency-cooldown](./skills/dependency-cooldown/SKILL.md)** — Sets up a minimum release age across a project's package managers and update bots, so a compromised release is caught before it resolves; per-ecosystem references from [cooldowns.dev](https://cooldowns.dev/).
- **[frozen-install](./skills/frozen-install/SKILL.md)** — Rewrites resolving install commands as frozen ones (`npm ci`, `uv sync --locked`) at every site meant to reproduce a lockfile — CI, image builds, task runners, docs — and proves the lockfile check fires.
- **[install-scripts](./skills/install-scripts/SKILL.md)** — Denies dependency install scripts by default (`ignore-scripts`, `uv sync --no-build`), then allowlists by name the packages that genuinely build something, and proves a fresh install runs nothing else.
- **[mise-setup](./skills/mise-setup/SKILL.md)** — Inventories the tools a project already uses across CI, containers, task runners, and per-language version files, then pins each one to a [mise](https://mise.jdx.dev/) backend and version in a committed `mise.toml` with a lockfile.
- **[parallel-steps](./skills/parallel-steps/SKILL.md)** — Makes GitHub Actions workflow steps run in parallel with the `background`, `wait`, `cancel`, and `parallel` keywords; written in ASD-STE100 Simplified Technical English.
- **[progressive-disclosure](./skills/progressive-disclosure/SKILL.md)** — Refactors a skill to load only relevant guidance by splitting broad references and mapping concrete project markers to focused files.
- **[skill-analyzer](./skills/skill-analyzer/SKILL.md)** — Splits a skill into scriptable and judgment work: classifies each step as deterministic or LLM, proposes a script interface and a simplified SKILL.md.

## Hooks

- **pinact** (`hooks/pinact_actions.py`, PostToolUse on Write|Edit) — Runs [pinact](https://github.com/suzuki-shunsuke/pinact) on GitHub Actions workflow files (`.github/workflows/`, `.github/actions/`) after Claude writes or edits them, pinning action references to full commit SHAs. Requires the `pinact` CLI on your PATH.
