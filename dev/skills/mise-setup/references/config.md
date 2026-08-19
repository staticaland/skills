# mise.toml

Verify any setting against the installed mise before writing it:
`mise settings --all | grep <name>`, then `mise settings get <name>`. Full list:
<https://mise.jdx.dev/configuration/settings.html>

## Which file to write

Precedence, highest first:

1. `mise.local.toml` - personal overrides, git-ignored
2. `mise.toml` - the committed project config
3. `mise/config.toml`, `.mise/config.toml`, `.config/mise.toml`,
   `.config/mise/config.toml`, `.config/mise/conf.d/*.toml`

`mise.<env>.toml` and `mise.<env>.local.toml` load when `MISE_ENV` is set - one
file per environment, layered on `mise.toml`. The global
`~/.config/mise/config.toml` and system `/etc/mise/config.toml` sit below all of
them.

Write `mise.toml` and commit it. Add `mise.local.toml` to `.gitignore` and tell
contributors it is theirs.

`mise cfg` lists the config files in play. `mise fmt` normalizes them.

## `[tools]`

```toml
[tools]
node = "24.19.0"                  # exact
python = "3.13"                   # prefix - newest 3.13.x
go = "latest"                     # newest release
java = "lts"                      # newest long-term-support release
"aqua:mikefarah/yq" = "4.53.3"    # backend-qualified
neovim = "ref:master"             # build from a git ref
mytool = "path:/opt/mytool"       # a directory already on disk
erlang = "sub-1:latest"           # one minor behind latest
```

Prefer exact versions with `lockfile = true`, and write them with
`mise use --pin`. `latest` and a bare prefix re-resolve on a new machine, which
is the drift the lockfile exists to prevent.

Long-form syntax carries tool options:

```toml
[tools.python]
version = "3.13.1"
# Skip this tool on Windows runners.
os = ["linux", "macos"]

[tools."ubi:BurntSushi/ripgrep"]
version = "14.1.1"
exe = "rg"                        # the binary's name differs from the package's
```

Per-tool overrides live in the same table, including `minimum_release_age`:

```toml
[tools.trivy]
version = "latest"
# Vulnerability databases are time-sensitive; take new releases immediately.
minimum_release_age = "0"
```

Ignore a tool the config declares without editing the file with
`disable_tools = ["node"]`.

## `[settings]`

The ones that change a project's behavior:

| Setting                                                        | Effect                                                                                                                                                                |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lockfile = true`                                              | Read and write `mise.lock`. Off by default                                                                                                                            |
| `locked = true`                                                | `mise install` fails when the lockfile has no pre-resolved URL for the platform, so no install calls GitHub or the aqua registry                                      |
| `locked_verify_provenance = true`                              | Re-verify SLSA provenance, Cosign, Minisign, and GitHub attestations at install time, even when the lockfile already holds a checksum and a provenance entry          |
| `minimum_release_age = "7d"`                                   | Ignore versions published inside the window. Defaults to `24h`. Takes a duration or an absolute date                                                                  |
| `minimum_release_age_excludes = ["trivy", "npm:*"]`            | Exempt a tool or a whole backend from the window                                                                                                                      |
| `pipx.uvx = true`                                              | Install `pipx:` tools with `uvx` when `uv` is on PATH. Already the default; write it to survive an older mise                                                         |
| `idiomatic_version_file_enable_tools = ["python"]`             | Read `.python-version`, `.node-version`, `.nvmrc`, `.ruby-version`, and `go.mod`. Disabled by default - list only the tools whose version file defines the constraint |
| `idiomatic_version_file_disable_files = ["node:package.json"]` | Stop reading one file for one tool                                                                                                                                    |
| `disable_backends = ["asdf", "vfox"]`                          | Block a backend for new installs                                                                                                                                      |
| `jobs = 8`                                                     | Parallel installs                                                                                                                                                     |
| `experimental = true`                                          | Required by features still behind the flag                                                                                                                            |
| `paranoid = true`, `safe = true`                               | Extra-secure behavior, and a hard boundary against code execution from repo-controlled config                                                                         |
| `trusted_config_paths = ["~/work"]`                            | Trust configs under these paths without the prompt                                                                                                                    |

Language-specific settings sit in their own tables: `python.uv_venv_auto`,
`python.default_packages_file`, `node.corepack`, `node.npm_shim`,
`go.set_goroot`, `java.shorthand_vendor`, `cargo.binstall`, `ruby.ruby_install`.

## `[env]`

`[env]` is how a tool gets the environment it needs, so it belongs to the
toolchain instead of beside it:

```toml
[env]
# Plain variables
GOFLAGS = "-mod=readonly"

# Prepend to PATH; tools = true delays resolution until installs finish
_.path = ["./bin", { path = ["{{ tools.go.path }}/bin"], tools = true }]

# Load a dotenv, JSON, YAML, or TOML file
_.file = ".env"

# Create and activate a virtualenv
_.python.venv = { path = ".venv", create = true }

# Point uv at the interpreter mise installed
UV_PYTHON = { value = "{{ tools.python.path }}", tools = true }
```

For a project with a `uv.lock`, `python.uv_venv_auto = "source"` under
`[settings]` activates the environment `uv` manages instead - a separate
mechanism from `_.python.venv`, so pick one. Details:
<https://mise.jdx.dev/lang/python.html>

Mark secrets with `redactions = ["*_TOKEN"]` at the top level to keep them out
of mise's output.

## Keeping versions current

```bash
mise outdated              # what has moved
mise upgrade               # newest version inside the range mise.toml states
mise upgrade --bump        # newest version, and rewrite mise.toml to match
mise lock --bump           # re-resolve fuzzy selectors in the lockfile, install nothing
```

`mise upgrade` updates `mise.lock` when `lockfile = true`.
