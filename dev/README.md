# dev

Automate browsers and Electron apps with the agent-browser CLI, pin GitHub
Actions to commit SHAs on workflow edits, parallelize workflow steps, set up
dependency cooldowns, Renovate, and mise toolchains, freeze install commands to
their lock files, deny install-time script execution, grill a plan until its
design tree holds, and pin down a project's domain terms and decisions.

Category: `dev`

## Skills

Model-invoked - Claude activates these automatically when the request matches.

- **[agent-browser](./skills/agent-browser/SKILL.md)** - Drives Chrome,
  web apps, and Electron apps from the command line with
  [agent-browser](https://github.com/vercel-labs/agent-browser) - navigating,
  filling forms, clicking, taking screenshots, and extracting data.
- **[dependency-cooldown](./skills/dependency-cooldown/SKILL.md)** - Sets up a
  minimum release age across a project's package managers and update bots, so a
  compromised release is caught before it resolves. Per-ecosystem references
  from [cooldowns.dev](https://cooldowns.dev/).
- **[domain-modeling](./skills/domain-modeling/SKILL.md)** - Pins down the words
  a project uses for its domain in a `CONTEXT.md`, and records the decisions
  behind them as ADRs.
- **[frozen-install](./skills/frozen-install/SKILL.md)** - Rewrites resolving
  install commands as frozen ones (`npm ci`, `uv sync --locked`) at every site
  meant to reproduce a lockfile - CI, image builds, task runners, docs - and
  proves the lockfile check fires.
- **[grilling](./skills/grilling/SKILL.md)** - Interviews you about a plan,
  decision, or idea, mapping it as a design tree and attacking each branch until
  the thinking holds.
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

User-invoked - run these by name.

- **[grill-me](./skills/grill-me/SKILL.md)** - Starts a grilling session on the
  plan or design at hand.
- **[grill-with-docs](./skills/grill-with-docs/SKILL.md)** - Starts a grilling
  session that writes the outcome up as ADRs and domain terms while it runs.

### Install individual skills

```bash
npx skills add staticaland/skills --skill agent-browser
npx skills add staticaland/skills --skill dependency-cooldown
npx skills add staticaland/skills --skill domain-modeling
npx skills add staticaland/skills --skill frozen-install
npx skills add staticaland/skills --skill grill-me
npx skills add staticaland/skills --skill grill-with-docs
npx skills add staticaland/skills --skill grilling
npx skills add staticaland/skills --skill install-scripts
npx skills add staticaland/skills --skill mise-setup
npx skills add staticaland/skills --skill parallel-steps
npx skills add staticaland/skills --skill renovate-setup
```

## Hooks

- **pinact** (`hooks/pinact_actions.py`, PostToolUse on Write|Edit) - Runs
  [pinact](https://github.com/suzuki-shunsuke/pinact) on GitHub Actions workflow
  files (`.github/workflows/`, `.github/actions/`) after Claude writes or edits
  them, pinning action references to full commit SHAs. Requires the `pinact` CLI
  on your PATH.
