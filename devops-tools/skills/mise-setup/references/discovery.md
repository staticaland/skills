# Where a project's tools and versions already hide

Each marker answers one of two questions: **which tools** the project needs, and **which version** the repo already states. A marker in the second column makes that version an owner; a tool with no version source anywhere becomes a new owner in `mise.toml`.

## Language runtimes

| Marker | Tool | Version already stated in |
| --- | --- | --- |
| `package.json` | `node`, and a package manager | `engines.node`, `packageManager` (Corepack), `volta` |
| `.nvmrc`, `.node-version` | `node` | the file itself |
| `pyproject.toml` | `python`, and `uv`, `poetry`, `pdm`, or `hatch` | `requires-python`, `[tool.uv] required-version` |
| `.python-version` | `python` | the file itself, or `uv`'s pin |
| `go.mod` | `go` | the `go` directive, and `toolchain` |
| `Cargo.toml` | `rust` | `rust-version`, `rust-toolchain.toml` |
| `Gemfile` | `ruby` | the `ruby` directive, `.ruby-version` |
| `pom.xml`, `build.gradle`, `build.sbt` | `java`, and `maven`, `gradle`, `sbt` | `maven.compiler.release`, Gradle toolchain block, `.java-version`, `.sdkmanrc`, `gradle/wrapper/gradle-wrapper.properties` |
| `mix.exs` | `elixir`, `erlang` | `elixir` requirement in `mix.exs`, `.tool-versions` |
| `composer.json` | `php` | `require.php`, `config.platform.php` |
| `pubspec.yaml` | `dart`, `flutter` | `environment.sdk` |
| `*.csproj`, `global.json` | `dotnet` | `TargetFramework`, `sdk.version` in `global.json` |
| `deno.json`, `bunfig.toml` | `deno`, `bun` | rarely pinned — usually a new owner |

## CI

CI names tools that no version file mentions. Read every workflow.

- `uses: actions/setup-*@v4` with a `*-version` input — the version CI runs, which the local toolchain has to match.
- `uses: hashicorp/setup-terraform`, `astral-sh/setup-uv`, `pnpm/action-setup`, and the rest of the per-tool actions.
- Bare installs in `run:` blocks: `brew install`, `apt-get install`, `go install`, `pipx install`, `npm install -g`, `cargo install`, `curl … | sh`. These pin nothing and are the strongest reason to adopt mise.
- A container `image:` on the job or a service — the tools baked into that image.
- `.gitlab-ci.yml`, `.circleci/config.yml`, `azure-pipelines.yml`, `Jenkinsfile` carry the same three shapes.

## Task runners and hooks

The commands contributors type reveal the tools those commands need:

- `Makefile`, `magefile.go`, `justfile`, `Taskfile.yml`, `package.json` scripts, `noxfile.py`, `tox.ini`.
- `.pre-commit-config.yaml`, `lefthook.yml`, `.husky/` — each hook's binary is a tool a contributor needs.
- The shipped program's own runtime dependencies: `exec.Command`, `subprocess.run`, and backtick calls name binaries that must exist at run time, not build time. `grep -rE "exec\.(Command|LookPath)\(" .` finds them in Go.

## Containers, editors, and packaging

| Marker | What to read |
| --- | --- |
| `Dockerfile`, `Containerfile` | The base image tag pins a runtime; each `RUN … install` line names a tool |
| `.devcontainer/devcontainer.json` | `features` and `image` |
| `Brewfile`, a Homebrew formula, `flake.nix`, `shell.nix` | The distribution's declared dependencies — the closest thing to a finished inventory |
| `.vscode/extensions.json`, `.idea/` | Language servers and formatters the editor expects on PATH |
| `README.md`, `CONTRIBUTING.md` | The prerequisites section, which states the intent even where it has gone stale |

## Existing version managers

| Marker | Manager it belongs to |
| --- | --- |
| `.tool-versions` | asdf — mise reads this file with no setting |
| `.nvmrc`, `.node-version` | nvm, fnm, nodenv |
| `.python-version` | pyenv, uv |
| `.ruby-version` | rbenv, rvm |
| `.terraform-version` | tfenv |
| `.java-version`, `.sdkmanrc` | jenv, SDKMAN |
| `.tfswitchrc`, `.crenv-version`, `.exenv-version` | the matching `*env` manager |
| `volta` in `package.json` | Volta |

mise keeps reading these files only for tools listed in `idiomatic_version_file_enable_tools`, and `.tool-versions` unconditionally. Migration paths: [ci-and-migration.md](ci-and-migration.md).
