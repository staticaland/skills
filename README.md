# Skills

Skills and hooks for Claude Code, distributed as a marketplace of small,
single-purpose plugins. Install only the plugins you want - each one is an
independent bundle.

## Install

Add the marketplace, then install individual plugins:

```text
/plugin marketplace add staticaland/skills
/plugin install writing@staticaland-skills
/plugin install dev@staticaland-skills
/plugin install ai@staticaland-skills
/plugin install other@staticaland-skills
```

To install an individual skill in another supported agent, use its name with
the skills CLI:

```bash
npx skills add staticaland/skills --skill writing-revision
```

Each plugin README lists the command for every available skill. The skills CLI
does not install plugin hooks.

## Plugins

### `writing`

#### [writing](./writing/README.md)

Add sourced footnotes, revise prose for clarity and busy readers, write
controlled technical Norwegian, and lint Markdown with Vale.

- **[writing-revision](./writing/skills/writing-revision/SKILL.md)**
  (skill) - Makes text clear, scannable, and action-oriented for busy readers.
- **[Kontrollert norsk](./writing/skills/kontrollert-norsk/SKILL.md)**
  (skill) - Writes or revises documentation in controlled technical Norwegian
  (klarspråk per NS-ISO 24495-1 with ASD-STE100 principles).
- **[Auto-cite Factual Claims](./writing/skills/auto-cite-factual-claims/SKILL.md)**
  (skill) - Finds web sources for factual claims and adds them as Markdown
  footnotes.
- **Vale lint** (hook) - Runs [Vale](https://vale.sh/) on Markdown files after
  Claude writes or edits them. Requires the `vale` CLI.

### `dev`

#### [dev](./dev/README.md)

Pin GitHub Actions to commit SHAs on workflow edits, parallelize workflow steps,
set up dependency cooldowns, Renovate, and mise toolchains, freeze install
commands to their lock files, and deny install-time script execution.

- **[dependency-cooldown](./dev/skills/dependency-cooldown/SKILL.md)**
  (skill) - Sets up a minimum release age across a project's package managers
  and update bots, so a compromised release is caught before it resolves.
  Per-ecosystem references from [cooldowns.dev](https://cooldowns.dev/).
- **[frozen-install](./dev/skills/frozen-install/SKILL.md)** (skill) -
  Rewrites resolving install commands as frozen ones (`npm ci`,
  `uv sync --locked`) at every site meant to reproduce a lockfile - CI, image
  builds, task runners, docs - and proves the lockfile check fires.
- **[install-scripts](./dev/skills/install-scripts/SKILL.md)**
  (skill) - Denies dependency install scripts by default (`ignore-scripts`,
  `uv sync --no-build`), then allowlists by name the packages that build
  something, and proves a fresh install runs nothing else.
- **[mise-setup](./dev/skills/mise-setup/SKILL.md)** (skill) -
  Inventories the tools a project already uses across CI, containers, task
  runners, and per-language version files, then pins each one to a
  [mise](https://mise.jdx.dev/) backend and version in a committed `mise.toml`
  with a lockfile.
- **[parallel-steps](./dev/skills/parallel-steps/SKILL.md)** (skill) -
  Makes GitHub Actions workflow steps run in parallel with the `background`,
  `wait`, `cancel`, and `parallel` keywords, written in ASD-STE100 Simplified
  Technical English.
- **[Renovate setup](./dev/skills/renovate-setup/SKILL.md)** (skill) -
  Configures Renovate with a seven-day minimum release age and immutable updates
  through lock files, integrity hashes, action SHAs, and image digests.
- **pinact** (hook) - Pins GitHub Actions references to full commit SHAs with
  [pinact](https://github.com/suzuki-shunsuke/pinact) after Claude writes or
  edits workflow files. Requires the `pinact` CLI.

### `ai`

#### [ai](./ai/README.md)

Analyze skills, refactor references, and write documents for agents.

- **[progressive-disclosure](./ai/skills/progressive-disclosure/SKILL.md)**
  (skill) - Refactors a skill to load only relevant guidance by splitting broad
  references and mapping concrete project markers to focused files.
- **[skill-analyzer](./ai/skills/skill-analyzer/SKILL.md)** (skill) -
  Splits a skill into scriptable and judgment work: classifies each step as
  deterministic or LLM, proposes a script interface and a simplified SKILL.md.
- **[writing-for-agents](./ai/skills/writing-for-agents/SKILL.md)** (skill) -
  Guides writing skills, agent instructions, and documents reached through
  context pointers.

### `other`

#### [other](./other/README.md)

Turn text, notes, code, or images into Anki flashcards built on Andy Matuschak's
prompt-writing principles.

- **[anki-flashcards](./other/skills/anki-flashcards/SKILL.md)**
  (skill) - Creates concise Anki flashcards from text, documents, or images for
  spaced repetition learning.
- **[bro](./other/skills/bro/SKILL.md)**
  (skill) - Restates the last message in plain human language, with no jargon.

## Repo layout

- Each top-level plugin directory is one marketplace entry.

## Development

Install [mise](https://mise.jdx.dev/) and the Claude Code CLI, then install the
repository tools from the locked configuration:

```bash
mise trust
mise install --locked
```

Use mise shell activation or prefix repository-tool commands with
`mise exec --`.

The repository's [Git hook manager](https://prek.j178.dev/) reads
`.pre-commit-config.yaml`. Install the pre-commit and commit-message hooks:

```bash
mise exec -- prek install --hook-type pre-commit --hook-type commit-msg
```

Run all pre-commit checks against tracked files:

```bash
mise exec -- prek run --all-files
```

## License

MIT
