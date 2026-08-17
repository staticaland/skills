# CI, containers, and migration

## GitHub Actions

`jdx/mise-action` installs mise and the configured tools. It caches both. Look
up its latest release instead of writing a major tag from memory - the version
below was current when this was written and the major has moved before:

```bash
gh api repos/jdx/mise-action/releases/latest --jq .tag_name   # v4.2.4
gh api repos/jdx/mise-action/commits/v4.2.4 --jq .sha
```

Pin the action to that release's commit SHA and put the tag in a trailing
comment, because a tag can be moved to other code and a SHA cannot:

```yaml
- uses: jdx/mise-action@7e36c90d9ab29c415a2384db3006f3ec8a8cc654 # v4.2.4
  with:
    version: 2026.8.2 # pin mise itself; defaults to latest
    install: true # runs mise install (default)
    cache: true # caches mise using GitHub's cache (default)
```

The comment is what Dependabot, Renovate, and `pinact` read to bump the pin, and
what tells a reviewer which release the SHA is.

Then delete every `actions/setup-*` step whose tool now lives in `mise.toml`. A
`setup-node` left beside a `node` entry means two versions and one of them wins
silently.

With `mise.lock` committed, add `--locked` so a missing lockfile entry fails the
job instead of resolving over the network:

```yaml
- uses: jdx/mise-action@7e36c90d9ab29c415a2384db3006f3ec8a8cc654 # v4.2.4
  with:
    install_args: --locked
```

`MISE_ENV=ci` loads `mise.ci.toml` on top of `mise.toml`, which is where CI-only
tools belong.

## Other CI and trust

mise assumes trust in detected CI unless `paranoid` is on. A config holding only
`min_version`, plain `[tools]` version strings, and template-free `[tasks]`
needs no trust anywhere, because nothing in it runs code at load time. A config
with `[env]` templates, hooks, or tool options does, so on a runner mise does
not detect, either mark it trusted or list the path:

```bash
mise trust --all
# or
export MISE_TRUSTED_CONFIG_PATHS=/builds/myorg/myproject
```

On GitLab CI and similar, cache `MISE_DATA_DIR` between jobs.

## Containers

`mise generate bootstrap --write bin/mise-bootstrap` writes a script that
downloads a pinned mise, so a Dockerfile or a fresh contributor needs no mise on
the image:

```bash
mise generate bootstrap --version 2026.8.2 --write bin/mise-bootstrap
```

`--localize` sandboxes `MISE_DATA_DIR` and `MISE_CACHE_DIR` into `.mise/` in the
project, which keeps a contributor's own mise out of the way.

In a `Dockerfile`, install and then reach the tools through shims instead of
shell activation, since `RUN` is non-interactive:

```dockerfile
COPY mise.toml mise.lock ./
RUN mise install --locked
ENV PATH="/root/.local/share/mise/shims:$PATH"
```

`mise generate devcontainer` writes a devcontainer that runs mise. `mise oci`
builds a container image from `mise.toml` and is experimental.

## Editors and other non-interactive contexts

`mise activate` modifies PATH per directory and needs a shell. An editor, a
`launchd` job, or a Makefile invoked from outside the shell gets the tools from
the shims directory instead:

```text
~/.local/share/mise/shims
```

Run `mise reshim` after installing a tool that adds binaries outside mise's
knowledge. The trade-offs: <https://mise.jdx.dev/dev-tools/shims.html>

## Migrating off another version manager

| From                           | Move                                                                                                                                                                             |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `asdf`                         | mise reads `.tool-versions` already. Translate it to `mise.toml` with `mise use`, replacing each `asdf:` plugin with an `aqua:` or `core:` backend, then delete `.tool-versions` |
| `nvm`, `nodenv`                | `mise sync node --nvm` or `--nodenv` symlinks the existing installs into mise, so nothing re-downloads. Then write `node` into `mise.toml`                                       |
| `pyenv`                        | `mise sync python --pyenv`                                                                                                                                                       |
| `uv`                           | `mise sync python --uv` keeps the two in sync both ways                                                                                                                          |
| Homebrew runtimes              | `mise sync node --brew`, `mise sync ruby --brew`                                                                                                                                 |
| `tfenv`, `jenv`, SDKMAN, Volta | No sync path. Read the version out of `.terraform-version`, `.java-version`, `.sdkmanrc`, or the `volta` block, write it into `mise.toml`, and delete the file                   |

`mise sync` symlinks versions into mise without overwriting installs. It imports
what is on the machine - it does not write `mise.toml`, so the project config
still has to state the version.

To keep a per-language version file as the owner instead of deleting it, list
its tool:

```bash
mise settings add idiomatic_version_file_enable_tools python
```

Every enabled file is a second place a version lives. Enable it where another
tool in the stack reads the same file, and delete it otherwise.

## Contributor hooks

```bash
mise generate git-pre-commit --write   # run a mise task from a pre-commit hook
mise generate task-stubs               # ./build style shims that call mise tasks
```
