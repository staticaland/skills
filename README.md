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

Add sourced footnotes, revise prose for clarity and busy readers, strip
references the reader cannot see, write controlled technical Norwegian, and
lint Markdown with Vale.

- **[writing-revision](./writing/skills/writing-revision/SKILL.md)**
  (skill) - Makes text clear, scannable, and action-oriented for busy readers.
- **[Kontrollert norsk](./writing/skills/kontrollert-norsk/SKILL.md)**
  (skill) - Writes or revises documentation in controlled technical Norwegian
  (klarspråk per NS-ISO 24495-1 with ASD-STE100 principles).
- **[Auto-cite Factual Claims](./writing/skills/auto-cite-factual-claims/SKILL.md)**
  (skill) - Finds web sources for factual claims and adds them as Markdown
  footnotes.
- **[standalone](./writing/skills/standalone/SKILL.md)** (skill) - Strips
  references the reader cannot see - "as discussed", "the old handler" - from
  prose and code comments.
- **Vale lint** (hook) - Runs [Vale](https://vale.sh/) on Markdown files after
  Claude writes or edits them. Requires the `vale` CLI.

### `dev`

#### [dev](./dev/README.md)

Automate browsers and Electron apps with the agent-browser CLI, pin GitHub
Actions to commit SHAs on workflow edits, parallelize workflow steps, set up
dependency cooldowns, Renovate, and mise toolchains, freeze install commands to
their lock files, deny install-time script execution, manage stacked pull
requests, open pull requests, run Git hooks with prek, grill a plan until its
design tree holds, look at a module with fresh eyes and keep the simplest
redesigns that survive its constraints, and pin down a project's domain terms
and decisions.

- **[agent-browser](./dev/skills/agent-browser/SKILL.md)** (skill) - Drives
  Chrome, web apps, and Electron apps from the command line with
  [agent-browser](https://github.com/vercel-labs/agent-browser) - navigating,
  filling forms, clicking, taking screenshots, and extracting data.
- **[create-pr](./dev/skills/create-pr/SKILL.md)** (skill) - Opens a GitHub
  pull request with `gh`, filling the repo's PR template or the skill's bundled
  one.
- **[dependency-cooldown](./dev/skills/dependency-cooldown/SKILL.md)**
  (skill) - Sets up a minimum release age across a project's package managers
  and update bots, so a compromised release is caught before it resolves.
  Per-ecosystem references from [cooldowns.dev](https://cooldowns.dev/).
- **[domain-modeling](./dev/skills/domain-modeling/SKILL.md)** (skill) - Pins
  down the words a project uses for its domain in a `CONTEXT.md`, and records
  the decisions behind them as ADRs.
- **[fresh-eyes](./dev/skills/fresh-eyes/SKILL.md)** (skill) - Ignores how a
  module, config, workflow, or design currently works, proposes the simplest
  design that could serve the same purpose, and keeps the proposals that
  survive the constraints that shaped the current one.
- **[frozen-install](./dev/skills/frozen-install/SKILL.md)** (skill) -
  Rewrites resolving install commands as frozen ones (`npm ci`,
  `uv sync --locked`) at every site meant to reproduce a lockfile - CI, image
  builds, task runners, docs - and proves the lockfile check fires.
- **[gh-stack](./dev/skills/gh-stack/SKILL.md)** (skill) - Manages stacked
  branches and pull requests with the
  [gh-stack](https://github.com/github/gh-stack) GitHub CLI extension: create,
  view, push, submit, sync, rebase, merge, and check out a stack.
- **[grill-me](./dev/skills/grill-me/SKILL.md)** (skill) - Starts a grilling
  session on the plan or design at hand.
- **[grill-with-docs](./dev/skills/grill-with-docs/SKILL.md)** (skill) -
  Starts a grilling session that writes the outcome up as ADRs and domain terms
  while it runs.
- **[grilling](./dev/skills/grilling/SKILL.md)** (skill) - Interviews you about
  a plan, decision, or idea, mapping it as a design tree and attacking each
  branch until the thinking holds.
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
- **[prek](./dev/skills/prek/SKILL.md)** (skill) - Sets up and runs Git hooks
  with [prek](https://prek.j178.dev/), the Rust drop-in alternative to
  pre-commit: workspace mode, built-in hooks, and shared toolchains.
- **[Renovate setup](./dev/skills/renovate-setup/SKILL.md)** (skill) -
  Configures Renovate with a seven-day minimum release age and immutable updates
  through lock files, integrity hashes, action SHAs, and image digests.
- **pinact** (hook) - Pins GitHub Actions references to full commit SHAs with
  [pinact](https://github.com/suzuki-shunsuke/pinact) after Claude writes or
  edits workflow files. Requires the `pinact` CLI.
- **pr-create guard** (hook) - Blocks a direct `gh pr create` and tells Claude
  to invoke the create-pr skill instead. Other `git` and `gh` commands are
  untouched.

### `ai`

#### [ai](./ai/README.md)

Analyze skills, prune no-op prose, refactor references, and write documents for
agents.

- **[progressive-disclosure](./ai/skills/progressive-disclosure/SKILL.md)**
  (skill) - Refactors a skill to load only relevant guidance by splitting broad
  references and mapping concrete project markers to focused files.
- **[prune-no-ops](./ai/skills/prune-no-ops/SKILL.md)** (skill) - Deletes the
  sentences in a skill that change no behavior: asides, justification,
  emphasis, and restated defaults.
- **[skill-analyzer](./ai/skills/skill-analyzer/SKILL.md)** (skill) -
  Splits a skill into scriptable and judgment work: classifies each step as
  deterministic or LLM, proposes a script interface and a simplified SKILL.md.
- **[writing-for-agents](./ai/skills/writing-for-agents/SKILL.md)** (skill) -
  Guides writing skills, agent instructions, and documents reached through
  context pointers.

### `other`

#### [other](./other/README.md)

Turn text, notes, code, or images into Anki flashcards built on Andy Matuschak's
prompt-writing principles, and ask for a message again in plain language when it
does not land.

- **[anki-flashcards](./other/skills/anki-flashcards/SKILL.md)**
  (skill) - Creates concise Anki flashcards from text, documents, or images for
  spaced repetition learning.
- **[bro](./other/skills/bro/SKILL.md)**
  (skill) - Restates the last message in plain human language, with no jargon.
- **[wait-what](./other/skills/wait-what/SKILL.md)**
  (skill) - Asks for a re-pitch of the last message, in Simplified Technical
  English and the project's own domain terms.

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
`prek.toml`. Install the pre-commit and commit-message hooks:

```bash
mise exec -- prek install --hook-type pre-commit --hook-type commit-msg
```

Run all pre-commit checks against tracked files:

```bash
mise exec -- prek run --all-files
```

## License

MIT
