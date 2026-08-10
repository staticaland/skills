# Cooldowns in containers, proxies, and the `cooldowns.sh` helper

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

## Container images

Developer-machine config does not carry into an image. Where a team maintains shared base images, bake the cooldown in so nobody has to remember it.

### Relative durations

`uv`, `pip` (26.1+), `npm`, `pnpm`, Bun, Deno, and Yarn all accept relative durations, which never go stale — set environment variables or copy config files in at build time:

```dockerfile
FROM quay.io/fedora/fedora

# pip cooldown (26.1+)
ENV PIP_UPLOADED_PRIOR_TO="P3D"

# uv cooldown
ENV UV_EXCLUDE_NEWER="3 days"

# npm cooldown (if you also use Node)
COPY .npmrc /path/to/your/app/dir
```

### Absolute timestamps

For `pip` < 26.1, compute the cutoff in the same `RUN` step that installs, so it is evaluated at build time:

```dockerfile
FROM quay.io/fedora/fedora

COPY requirements.txt .
RUN PIP_UPLOADED_PRIOR_TO=$(date -u -d '3 days ago' '+%Y-%m-%dT%H:%M:%SZ') \
    pip install -r requirements.txt
```

In a development container where developers also run `pip install` interactively, drop the wrapper function from [python_pip.md](python_pip.md) into `/etc/profile.d/` so it is sourced for interactive shells:

```dockerfile
COPY pip-cooldown.sh /etc/profile.d/pip-cooldown.sh
```

## Registry-level proxies

A caching proxy in front of public registries enforces cooldowns for every tool behind it, **overriding any project or CI config** and covering tools with no native support. JFrog Artifactory and Sonatype Nexus quarantine newly published versions for a configurable period, across every ecosystem they proxy, including `npm`, PyPI, and Maven.

For self-hosted `npm`, [Verdaccio](https://verdaccio.org/) does the same through its bundled `@verdaccio/package-filter` plugin: set `minAgeDays` to hide versions published less than N days ago. The plugin is disabled by default.

## `cooldowns.sh`

[`cooldowns.sh`](https://github.com/mprpic/cooldowns/blob/main/cooldowns.sh) configures cooldowns across `pip`, `uv`, `poetry`, `pdm`, `npm`, `pnpm`, Yarn, Bun, Deno, Cargo, and Bundler in one command, and verifies them.

```bash
cooldowns.sh set pip 3d
cooldowns.sh set uv "3 days"
cooldowns.sh set npm 7d
```

Each `set` writes **user-wide** configuration and leaves project configs untouched:

| Tool    | Method                                           | Location                                       |
|---------|--------------------------------------------------|------------------------------------------------|
| `pip`     | Environment variable export (26.1+) or shell wrapper (older)  | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `uv`      | Environment variable export                                   | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `poetry` | `poetry config` setting                          | `~/.config/pypoetry/config.toml`               |
| `pdm`     | `pdm config` setting (requires PDM >= 2.27.0)    | `~/.config/pdm/config.toml`                    |
| `npm`     | `.npmrc` key                                     | `~/.npmrc`                                     |
| `pnpm`    | `.npmrc` key                                     | `~/.npmrc`                                     |
| `yarn`  | Environment variable export                                   | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `bun`   | `bunfig.toml` key                                | `~/.bunfig.toml`                               |
| `deno`    | Shell aliases                                    | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `cargo` | Environment variable export (requires `cargo-cooldown` crate) | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `bundler` | Environment variable export (requires Bundler >= 4.0.13)      | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |

Profile-script tools write to `/etc/profile.d/cooldowns.sh` when that directory exists and is writable, otherwise `~/.bashrc`.

Project-only tools are **not covered**: `pipenv`, `pixi`, mise, and Scala Steward. (`pipenv` does inherit `PIP_UPLOADED_PRIOR_TO` from `cooldowns.sh set pip`, since it runs on `pip`.)

`cooldowns.sh check` scans installed managers and exits non-zero on any missing or stale cooldown, which makes it usable as a CI gate:

```text
Checking dependency cooldown configurations...

  ok      pip      PIP_UPLOADED_PRIOR_TO='P3D' (3-day cooldown) in /etc/profile.d/cooldowns.sh
  ok      uv       UV_EXCLUDE_NEWER="3 days" in /etc/profile.d/cooldowns.sh
  ok      npm      min-release-age=3d in /home/user/.npmrc
  MISS    cargo    no cooldown configured

3 configured, 0 warnings, 1 not configured
```

Both commands work in an image build:

```dockerfile
FROM quay.io/fedora/fedora

COPY cooldowns.sh /usr/local/bin/
RUN cooldowns.sh set pip 3d && cooldowns.sh set uv 3d && cooldowns.sh set npm 3d
RUN cooldowns.sh check
```
