# Backends

A backend is the source mise downloads a tool from. `mise backends ls` prints the ones the installed version supports; `mise registry <tool>` prints the candidates for one tool, best first. Full docs: <https://mise.jdx.dev/dev-tools/backends/>

## The prefixes

| Prefix | Source | Notes |
| --- | --- | --- |
| `core:` | Built into mise | Language runtimes: `node`, `python`, `go`, `java`, `ruby`, `rust`, `deno`, `bun`, `erlang`, `elixir`, `zig`, `swift` |
| `aqua:` | The [aqua registry](https://github.com/aquaproj/aqua-registry) | Release binaries with verification metadata. The first choice for a CLI |
| `github:`, `gitlab:`, `forgejo:` | Release assets on a forge | For a tool no aqua package covers |
| `http:` | A URL you supply | Pair with `mise generate tool-stub` for an internal binary |
| `ubi:` | [ubi](https://github.com/houseabsolute/ubi) | Guesses the asset for the platform; no registry entry needed |
| `npm:`, `pipx:`, `cargo:`, `go:`, `gem:`, `spm:`, `dotnet:` | Language package managers | Resolution pulls transitive dependencies from that ecosystem |
| `conda:`, `s3:`, `pkgx:` | Conda, an S3 bucket, pkgx | `pkgx` is experimental |
| `asdf:`, `vfox:` | A plugin repository | mise runs the plugin's shell or Lua script on the machine |

## Which one to take

The registry's own tiers, from <https://mise.jdx.dev/registry.html>: `aqua` and `github` are preferred, `conda` comes next, and the language-specific backends (`pipx`, `npm`, `gem`, `go`, `cargo`, `dotnet`) are accepted only for tools that cannot ship as a single binary. Confirm what a candidate buys before taking it:

```bash
mise tool aqua:mikefarah/yq
# Backend:      aqua:mikefarah/yq
# Security:     checksum (sha256), cosign
```

Three reasons to move right in the list:

- The tool is a library-plus-CLI in one ecosystem (`npm:prettier`, `pipx:cogapp`) — a language backend is the only honest source.
- The aqua package lags the release you need. Compare `mise ls-remote aqua:owner/repo` against the upstream releases.
- Nothing carries it. Fall back to `ubi:owner/repo`, or write an `http:` tool stub.

An `asdf:` or `vfox:` plugin executes code from a third-party repository at install time. Prefer any other backend, and record why when one is unavoidable.

## Writing a backend-qualified name

`mise use yq` writes whatever the registry maps `yq` to today. Write the backend instead, so a registry change cannot move the tool:

```toml
[tools]
"aqua:mikefarah/yq" = "4.53.3"
"pipx:cogapp" = "3.6.0"
"npm:prettier" = "3.4.2"
```

Quote any name containing `:` or `/`. To keep the short name and still fix the backend, override the registry mapping:

```bash
export MISE_BACKENDS_YQ='aqua:mikefarah/yq'   # SHOUTY_SNAKE_CASE of the tool name
```

Block a backend for the whole project with `disable_backends`, which stops new installs without touching installed tools:

```toml
[settings]
disable_backends = ["asdf", "vfox"]
```

## Minimum release age coverage

`minimum_release_age` filters candidate versions on `aqua`, `cargo`, `github`, `gitlab`, `go`, `npm`, and `pipx`; `npm` and `pipx` also apply it to transitive dependencies. A pinned exact version installs regardless of the setting. Details: <https://mise.jdx.dev/security.html>

## Trying an unfamiliar package

```bash
mise search ripgrep                    # fuzzy search the registry
mise ls-remote aqua:BurntSushi/ripgrep # versions the backend offers
mise test-tool aqua:BurntSushi/ripgrep # install it and run its binary
mise where aqua:BurntSushi/ripgrep     # where it landed
mise which rg                          # which install PATH resolves to
```

`mise test-tool` installs and executes the tool, which answers whether the package's binary name matches the tool name — the failure that `mise install` alone hides.
