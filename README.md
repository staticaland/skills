# Staticaland Skills

Skills and hooks for Claude Code, distributed as a marketplace of small, single-purpose plugins. Install only the plugins you want - each one is an independent bundle.

## Install

Add the marketplace, then install individual plugins:

```
/plugin marketplace add staticaland/skills
/plugin install writing-tools@staticaland-skills
/plugin install learning-tools@staticaland-skills
/plugin install devops-tools@staticaland-skills
```

## Plugins

### [writing-tools](./writing-tools/README.md)

Revise prose for clarity and busy readers, with automatic Vale linting of Markdown files on every edit.

- **[writing-revision](./writing-tools/skills/writing-revision/SKILL.md)** (skill) - Makes text clear, scannable, and action-oriented for busy readers.
- **[Kontrollert norsk](./writing-tools/skills/kontrollert-norsk/SKILL.md)** (skill) - Writes or revises documentation in controlled technical Norwegian (klarspråk per NS-ISO 24495-1 with ASD-STE100 principles).
- **Vale lint** (hook) - Runs [Vale](https://vale.sh/) on Markdown files after Claude writes or edits them. Requires the `vale` CLI.

### [learning-tools](./learning-tools/README.md)

Turn text, notes, code, or images into Anki flashcards built on Andy Matuschak's prompt-writing principles.

- **[anki-flashcards](./learning-tools/skills/anki-flashcards/SKILL.md)** (skill) - Creates concise Anki flashcards from text, documents, or images for spaced repetition learning.

### [devops-tools](./devops-tools/README.md)

Pin GitHub Actions to commit SHAs on workflow edits, parallelize workflow steps, set up dependency cooldowns and mise toolchains, freeze install commands to their lock files, deny install-time script execution, analyze skills to split scriptable work from judgment work, and refactor skill references for progressive disclosure.

- **[dependency-cooldown](./devops-tools/skills/dependency-cooldown/SKILL.md)** (skill) - Sets up a minimum release age across a project's package managers and update bots, so a compromised release is caught before it resolves. Per-ecosystem references from [cooldowns.dev](https://cooldowns.dev/).
- **[frozen-install](./devops-tools/skills/frozen-install/SKILL.md)** (skill) - Rewrites resolving install commands as frozen ones (`npm ci`, `uv sync --locked`) at every site meant to reproduce a lockfile - CI, image builds, task runners, docs - and proves the lockfile check fires.
- **[install-scripts](./devops-tools/skills/install-scripts/SKILL.md)** (skill) - Denies dependency install scripts by default (`ignore-scripts`, `uv sync --no-build`), then allowlists by name the packages that build something, and proves a fresh install runs nothing else.
- **[mise-setup](./devops-tools/skills/mise-setup/SKILL.md)** (skill) - Inventories the tools a project already uses across CI, containers, task runners, and per-language version files, then pins each one to a [mise](https://mise.jdx.dev/) backend and version in a committed `mise.toml` with a lockfile.
- **[parallel-steps](./devops-tools/skills/parallel-steps/SKILL.md)** (skill) - Makes GitHub Actions workflow steps run in parallel with the `background`, `wait`, `cancel`, and `parallel` keywords, written in ASD-STE100 Simplified Technical English.
- **[progressive-disclosure](./devops-tools/skills/progressive-disclosure/SKILL.md)** (skill) - Refactors a skill to load only relevant guidance by splitting broad references and mapping concrete project markers to focused files.
- **[skill-analyzer](./devops-tools/skills/skill-analyzer/SKILL.md)** (skill) - Splits a skill into scriptable and judgment work: classifies each step as deterministic or LLM, proposes a script interface and a simplified SKILL.md.
- **pinact** (hook) - Pins GitHub Actions references to full commit SHAs with [pinact](https://github.com/suzuki-shunsuke/pinact) after Claude writes or edits workflow files. Requires the `pinact` CLI.

## Repo layout

- Each top-level plugin directory is one marketplace entry.
- [`in-progress/`](./in-progress/README.md) holds drafts still in development.
- [`deprecated/`](./deprecated/README.md) holds retired plugins kept for reference.

## Development

Validate before committing:

```bash
claude plugin validate .
```

## License

MIT
