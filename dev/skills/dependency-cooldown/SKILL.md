---
name: dependency-cooldown
description:
  Set up dependency cooldowns - a minimum release age that holds back freshly
  published package versions - across a project's package managers and update
  bots. Use when the user wants protection from compromised releases, or
  mentions cooldown, minimum release age, or exclude-newer.
version: 0.2.0
---

# Dependency Cooldown

A cooldown holds back package versions published less than N days ago, so
researchers catch a compromised release before it reaches the project.
[An analysis of ten prominent supply-chain attacks](https://blog.yossarian.net/2025/11/21/We-should-all-be-using-dependency-cooldowns)
found eight had exploitation windows under one week; a three-day cooldown would
have blocked most of them.

A cooldown binds at **resolution** - the moment a version range becomes a
concrete version. Installing from an existing lockfile resolves nothing, and an
update bot's cooldown only delays its pull requests. Cover every site that
resolves, not only the one the user asked about.

[cooldowns.dev](https://cooldowns.dev/) is the source of truth. Consult it when
a reference file below disagrees or omits a manager.

## Procedure

### 1. Inventory the resolution sites

List the candidate files:

```bash
git ls-files | grep -Ei '(^|/)(package\.json|package-lock\.json|pnpm-workspace\.yaml|pnpm-lock\.yaml|\.npmrc|\.yarnrc\.yml|yarn\.lock|bunfig\.toml|bun\.lockb?|deno\.jsonc?|deno\.lock|pyproject\.toml|uv\.lock|uv\.toml|requirements.*\.txt|Pipfile|poetry\.lock|pdm\.lock|pixi\.toml|pixi\.lock|environment\.ya?ml|Gemfile|mix\.exs|Cargo\.toml|pom\.xml|build\.(sbt|gradle|gradle\.kts|mill)|go\.mod|composer\.json|pubspec\.yaml|Package\.swift|.*\.csproj|mise\.toml|\.tool-versions|renovate\.json5?|dependabot\.yml|\.scala-steward\.conf|Dockerfile[^/]*|Containerfile)$|\.github/workflows/|\.vscode/'
```

Then find the resolvers among the hits: update bot configs, CI workflows and
Dockerfiles that install without a committed lockfile or run an update command,
and tool-version managers.

Single-file scripts declare dependencies inline instead of in a manifest, so no
filename matches them. Add `git grep -ln '/// script'` for
[PEP 723](https://peps.python.org/pep-0723/) Python scripts.

Done when every manager in the repo appears in a list with its resolution sites,
and each site is marked covered by a cooldown or not.

### 2. Load the references for what you found

Read only the files for the managers present:

| Marker                                                                                 | Reference                                                                                              |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `uv.lock`, `uv.toml`, `[tool.uv]`, `/// script`                                        | [python_uv.md](references/python_uv.md) - `uv`                                                         |
| `requirements*.txt`, `pip.conf`, `pip install`                                         | [python_pip.md](references/python_pip.md) - `pip`, pip-tools                                           |
| `Pipfile`                                                                              | [python_pipenv.md](references/python_pipenv.md) - `pipenv`                                             |
| `poetry.lock`, `[tool.poetry]`                                                         | [python_poetry.md](references/python_poetry.md) - Poetry                                               |
| `pdm.lock`, `[tool.pdm]`                                                               | [python_pdm.md](references/python_pdm.md) - PDM                                                        |
| `pixi.toml`, `pixi.lock`                                                               | [python_pixi.md](references/python_pixi.md) - `pixi`                                                   |
| `environment.yml`, `environment.yaml`                                                  | [python_conda.md](references/python_conda.md) - `conda`                                                |
| Private PyPI index                                                                     | [python_private_registries.md](references/python_private_registries.md) - missing upload-time behavior |
| `package-lock.json`, `min-release-age` in `.npmrc`, `npm install`/`npm ci`             | [javascript_npm.md](references/javascript_npm.md) - `npm`                                              |
| `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `packageManager: pnpm@`                       | [javascript_pnpm.md](references/javascript_pnpm.md) - `pnpm`                                           |
| `yarn.lock`, `.yarnrc.yml`                                                             | [javascript_yarn.md](references/javascript_yarn.md) - Yarn                                             |
| `bun.lock`, `bunfig.toml`                                                              | [javascript_bun.md](references/javascript_bun.md) - Bun                                                |
| `deno.json`, `deno.jsonc`, `deno.lock`                                                 | [javascript_deno.md](references/javascript_deno.md) - Deno                                             |
| `Cargo.toml`                                                                           | [rust.md](references/rust.md) - Cargo, cargo-cooldown                                                  |
| `Gemfile`                                                                              | [ruby.md](references/ruby.md) - Bundler                                                                |
| `mix.exs`                                                                              | [elixir.md](references/elixir.md) - Hex                                                                |
| `.scala-steward.conf`, `pom.xml`, `build.sbt`, `build.mill`                            | [jvm_scala_steward.md](references/jvm_scala_steward.md) - Scala Steward                                |
| `mise.toml`, `.tool-versions`                                                          | [mise.md](references/mise.md) - mise                                                                   |
| `.vscode/extensions.json`, `.vscode/settings.json`                                     | [vscode.md](references/vscode.md) - VS Code extensions                                                 |
| `.github/workflows/`                                                                   | [github-actions.md](references/github-actions.md) - actions-up, SHA pinning                            |
| `renovate.json`, `renovate.json5`                                                      | [bot_renovate.md](references/bot_renovate.md) - Renovate                                               |
| `dependabot.yml`                                                                       | [bot_github.md](references/bot_github.md) - GitHub Dependabot                                          |
| `go.mod`, `*.csproj`, `composer.json`, `pubspec.yaml`, `Package.swift`, `build.gradle` | [ecosystems_no_native.md](references/ecosystems_no_native.md) - no native cooldown; bot gate only      |
| `Dockerfile`, `Containerfile`                                                          | [containers.md](references/containers.md) - baking a cooldown into an image                            |
| A registry URL that is not the public one                                              | [registry_proxies.md](references/registry_proxies.md) - Artifactory, Nexus, Verdaccio                  |
| The user asks for a user-wide or machine-wide gate                                     | [cooldowns_sh.md](references/cooldowns_sh.md) - the `cooldowns.sh` helper                              |

Done when every manager from step 1 maps to a reference or to a recorded "no
cooldown available".

A `pyproject.toml` names no tool on its own. It can configure `uv`, Poetry, or
PDM, so inspect its tool tables and load only the matching rows. A
`package.json` with no lockfile and no `packageManager` field identifies no
JavaScript manager either - read the CI workflow's install command first, and
load nothing until one names a manager.

### 3. Check the version gate

Get the installed version of each manager and compare it against the minimum in
its reference. **A tool below the minimum ignores the setting and reports no
error** - the config reads correctly and does nothing. Check the versions CI and
the container images use, not only the local one.

Done when every manager has a verdict: supported, upgrade first, or no native
support.

### 4. Choose the duration

Default to 3 days unless the user gives a constraint.

- **12-24 hours** - covers the fast-exploitation window at the least friction.
- **3 days** - matches the new defaults of Dependabot and Renovate's `npm`
  best-practices preset.
- **7 days** - catches nearly every historical incident. Expect friction on
  fast-moving dependencies.

Use one duration everywhere. Each tool takes it in its own unit - days, minutes,
seconds, or ISO 8601 - and each reference gives the form per tool. Sibling
managers in one ecosystem disagree: `npm` counts days where `pnpm` counts
minutes and Bun counts seconds. Convert the duration into each tool's own unit.
Do not copy the number across.

### 5. Write the config

Write project-level committed config, not user-level (`~/.config/...`), so CI,
containers, and teammates share the same gate.

Beside each setting, add a comment naming that manager's **bypass** - the
per-package escape hatch for an urgent security fix - and the reminder to revert
it afterwards. A cooldown with no documented bypass gets deleted the first time
it blocks a hotfix.

Done when every uncovered resolution site from step 1 has a committed setting or
a recorded reason it has none.

### 6. Verify enforcement

Prove the gate is live instead of trusting that the file took effect. Read the
setting back through the tool itself (`npm config get min-release-age`,
`poetry config solver.min-release-age`, `bundle config get cooldown`), then run
one resolution in dry-run mode and confirm the tool holds back a version
published inside the window.

Done when every manager from step 1 shows an observed hold-back or a stated
reason verification was impossible.

Report the covered managers, the duration, and what the cooldown leaves open:
typosquatting, a long-term maintainer compromise, and vulnerabilities in
versions already installed. Pair it with `npm audit`, `pip-audit`, or Dependabot
security alerts.
