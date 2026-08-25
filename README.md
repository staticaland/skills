# Skills

Skills and hooks for Claude Code, distributed as a marketplace of small,
single-purpose plugins. Install only the plugins you want - each one is an
independent bundle.

## Install

Add the marketplace, then install individual plugins:

```text
/plugin marketplace add staticaland/skills
/plugin install prose@staticaland-skills
/plugin install toolchain@staticaland-skills
```

The catalog below lists every plugin. Each one installs on its own, so you take
the ones you want and leave the rest.

To install an individual skill in another supported agent, use its name with
the skills CLI:

```bash
npx skills add staticaland/skills --skill writing-revision
```

Each plugin README lists the command for every available skill. The skills CLI
does not install plugin hooks.

Each plugin also has a `plugin.json` manifest at its root per the
[Agent Plugins](https://agent-plugins.org/) specification, and its skills
follow the [Agent Skills](https://agentskills.io/) format, so any client that
supports those specifications can install the plugins too.

## Plugins

### `writing`

#### [prose](./plugins/prose/README.md)

Revise prose for clarity and busy readers, add sourced footnotes, strip
references the reader cannot see, and lint Markdown with Vale.

- **[writing-revision](./plugins/prose/skills/writing-revision/SKILL.md)**
  (skill) - Makes text clear, scannable, and action-oriented for busy
  readers.
- **[Auto-cite Factual Claims](./plugins/prose/skills/auto-cite-factual-claims/SKILL.md)**
  (skill) - Finds web sources for factual claims and adds them as
  Markdown footnotes.
- **[standalone](./plugins/prose/skills/standalone/SKILL.md)** (skill) -
  Strips references the reader cannot see - "as discussed", "the old
  handler" - from prose and code comments.
- **Vale lint** (hook) - Runs [Vale](https://vale.sh/) on Markdown files
  after Claude writes or edits them. Requires the `vale` CLI.

#### [norsk](./plugins/norsk/README.md)

Write and revise documentation in controlled technical Norwegian -
klarspråk per NS-ISO 24495-1 with ASD-STE100 principles.

- **[Kontrollert norsk](./plugins/norsk/skills/kontrollert-norsk/SKILL.md)**
  (skill) - Writes or revises documentation in controlled technical
  Norwegian (klarspråk per NS-ISO 24495-1 with ASD-STE100 principles).

#### [plain-language](./plugins/plain-language/README.md)

Restate a message in plain human language, or ask for a re-pitch when it
does not land.

- **[bro](./plugins/plain-language/skills/bro/SKILL.md)** (skill) -
  Restates the last message in plain human language, with no jargon.
- **[wait-what](./plugins/plain-language/skills/wait-what/SKILL.md)**
  (skill) - Asks for a re-pitch of the last message, in Simplified
  Technical English and the project's own domain terms.

### `dev`

#### [pull-requests](./plugins/pull-requests/README.md)

Open a GitHub pull request from the repository's own template, manage stacked
branches and pull requests with gh-stack, and attach images and videos to
issues and pull requests.

- **[create-pr](./plugins/pull-requests/skills/create-pr/SKILL.md)**
  (skill) - Opens a GitHub pull request with `gh`, filling the repo's PR
  template or the skill's bundled one.
- **[gh-attach](./plugins/pull-requests/skills/gh-attach/SKILL.md)**
  (skill) - Uploads an image or video to a GitHub issue, pull request, or
  comment with the `gh --attach` flag, and controls where it renders in the
  body.
- **[gh-stack](./plugins/pull-requests/skills/gh-stack/SKILL.md)**
  (skill) - Manages stacked branches and pull requests with the
  [gh-stack](https://github.com/github/gh-stack) GitHub CLI extension: create,
  view, push, submit, sync, rebase, merge, and check out a stack.
- **pr-create guard** (hook) - Blocks a direct
  `gh pr create` and tells Claude to invoke the create-pr skill
  instead. Other `git` and `gh` commands are untouched.

#### [github-actions](./plugins/github-actions/README.md)

Run GitHub Actions workflow steps in parallel, replace repeated workflow
configuration with YAML anchors, name every workflow, job, and step, and pin
every action reference to a commit SHA on workflow edits.

- **[parallel-steps](./plugins/github-actions/skills/parallel-steps/SKILL.md)**
  (skill) - Makes GitHub Actions workflow steps run in parallel with the
  `background`, `wait`, `cancel`, and `parallel` keywords, written in ASD-STE100
  Simplified Technical English.
- **[yaml-anchors](./plugins/github-actions/skills/yaml-anchors/SKILL.md)**
  (skill) - Finds the configuration a workflow writes twice in the same file and
  replaces the identical copies with YAML anchors and aliases.
- **[workflow-names](./plugins/github-actions/skills/workflow-names/SKILL.md)**
  (skill) - Checks that every GitHub Actions workflow, job, and step has a
  name, and writes the missing ones in imperative, sentence-case style.
- **pinact** (hook) - Pins GitHub Actions references to full commit SHAs
  with [pinact](https://github.com/suzuki-shunsuke/pinact) after Claude writes
  or edits workflow files. Requires the `pinact` CLI.

#### [dependencies](./plugins/dependencies/README.md)

Hold new dependency releases for a cooldown, configure Renovate, freeze
install commands to their lock files, and deny install-time script execution.

- **[dependency-cooldown](./plugins/dependencies/skills/dependency-cooldown/SKILL.md)**
  (skill) - Sets up a minimum release age across a project's package
  managers and update bots, so a compromised release is caught before it
  resolves. Per-ecosystem references from
  [cooldowns.dev](https://cooldowns.dev/).
- **[Renovate setup](./plugins/dependencies/skills/renovate-setup/SKILL.md)**
  (skill) - Configures Renovate with a seven-day minimum release age and
  immutable updates through lock files, integrity hashes, action SHAs, and image
  digests.
- **[frozen-install](./plugins/dependencies/skills/frozen-install/SKILL.md)**
  (skill) - Rewrites resolving install commands as frozen ones
  (`npm ci`, `uv sync --locked`) at every site meant to
  reproduce a lockfile - CI, image builds, task runners, docs -
  and proves the lockfile check fails when the lockfile drifts.
- **[install-scripts](./plugins/dependencies/skills/install-scripts/SKILL.md)**
  (skill) - Denies dependency install scripts by default
  (`ignore-scripts`, `uv sync --no-build`), then allowlists by
  name the packages that build something, and proves a fresh install runs
  nothing else.

#### [toolchain](./plugins/toolchain/README.md)

Pin a project's tools to a mise toolchain, and run Git hooks with prek.

- **[mise-setup](./plugins/toolchain/skills/mise-setup/SKILL.md)**
  (skill) - Inventories the tools a project already uses across CI,
  containers, task runners, and per-language version files, then pins each one
  to a [mise](https://mise.jdx.dev/) backend and version in a committed
  `mise.toml` with a lockfile.
- **[prek](./plugins/toolchain/skills/prek/SKILL.md)** (skill) - Sets up
  and runs Git hooks with [prek](https://prek.j178.dev/), the Rust drop-in
  alternative to pre-commit: workspace mode, built-in hooks, and shared
  toolchains.

#### [grilling](./plugins/grilling/README.md)

Grill a plan until its design tree holds, and write the outcome up as domain
terms and architecture decisions.

- **[grilling](./plugins/grilling/skills/grilling/SKILL.md)** (skill) -
  Interviews you about a plan, decision, or idea, mapping it as a design tree
  and attacking each branch until the thinking holds.
- **[grill-me](./plugins/grilling/skills/grill-me/SKILL.md)** (skill) -
  Starts a grilling session on the plan or design at hand.
- **[grill-with-docs](./plugins/grilling/skills/grill-with-docs/SKILL.md)**
  (skill) - Starts a grilling session that writes the outcome up as ADRs
  and domain terms while it runs.
- **[domain-modeling](./plugins/grilling/skills/domain-modeling/SKILL.md)**
  (skill) - Pins down the words a project uses for its domain in a
  `CONTEXT.md`, and records the decisions behind them as ADRs.

#### [fresh-eyes](./plugins/fresh-eyes/README.md)

<!-- vale Skills.WeakVerbs = NO -->
<!-- "look at ... with fresh eyes" is the skill's own idiom. -->

Look at a module with fresh eyes and keep the simplest redesigns that survive
its constraints.

<!-- vale Skills.WeakVerbs = YES -->

- **[fresh-eyes](./plugins/fresh-eyes/skills/fresh-eyes/SKILL.md)**
  (skill) - Ignores how a module, config, workflow, or design currently
  works, proposes the simplest design that could serve the same purpose, and
  keeps the proposals that survive the constraints that shaped the current one.

#### [browser](./plugins/browser/README.md)

Drive Chrome, web apps, and Electron apps from the command line with the
agent-browser CLI.

- **[agent-browser](./plugins/browser/skills/agent-browser/SKILL.md)**
  (skill) - Drives Chrome, web apps, and Electron apps from the command
  line with
  [agent-browser](https://github.com/vercel-labs/agent-browser) -
  navigating, filling forms, clicking, taking screenshots, and extracting data.

### `ai`

#### [skill-authoring](./plugins/skill-authoring/README.md)

Write documents for agents, analyze a skill, prune the prose that changes no
behavior, and split broad references into focused files.

- **[writing-for-agents](./plugins/skill-authoring/skills/writing-for-agents/SKILL.md)**
  (skill) - Guides writing skills, agent instructions, and documents
  reached through context pointers.
- **[skill-analyzer](./plugins/skill-authoring/skills/skill-analyzer/SKILL.md)**
  (skill) - Splits a skill into scriptable and judgment work: classifies
  each step as deterministic or LLM, proposes a script interface and a
  simplified SKILL.md.
- **[prune-no-ops](./plugins/skill-authoring/skills/prune-no-ops/SKILL.md)**
  (skill) - Deletes the sentences in a skill that don't change behavior:
  asides, justification, emphasis, and restated defaults.
- **[progressive-disclosure](./plugins/skill-authoring/skills/progressive-disclosure/SKILL.md)**
  (skill) - Refactors a skill to load only relevant guidance by splitting
  broad references and mapping concrete project markers to focused files.

#### [retro](./plugins/retro/README.md)

Retrospect on a coding session to improve the environment the next one runs
in.

- **[retro](./plugins/retro/skills/retro/SKILL.md)** (skill) - Reviews a
  coding session and ranks the changes that would make the next one go better:
  navigation pointers, automated checks, coding standards, and tool economy.

### `other`

#### [flashcards](./plugins/flashcards/README.md)

Turn text, notes, code, or images into Anki flashcards built on Andy
Matuschak's prompt-writing principles.

- **[anki-flashcards](./plugins/flashcards/skills/anki-flashcards/SKILL.md)**
  (skill) - Creates concise Anki flashcards from text, documents, or
  images for spaced repetition learning.

## Repo layout

- Each directory under `plugins/` is one marketplace entry.
- A plugin's `category` groups it in the catalog above. Plugins share
  categories, and a category is not a directory name.

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
