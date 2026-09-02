# The `cooldowns.sh` helper

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

[`cooldowns.sh`](https://github.com/mprpic/cooldowns/blob/main/cooldowns.sh)
configures cooldowns across `pip`, `uv`, `poetry`, `pdm`, `npm`, `pnpm`, Yarn,
Bun, Deno, Cargo, and Bundler in one command, and verifies them.

```bash
cooldowns.sh set pip 3d
cooldowns.sh set uv "3 days"
cooldowns.sh set npm 7d
```

Each `set` writes **user-wide** configuration. It edits no project file, but an
exported variable can still outrank a committed project config - which side
wins differs per tool, and [env_overrides.md](env_overrides.md) maps it:

| Tool      | Method                                                        | Location                                       |
| --------- | ------------------------------------------------------------- | ---------------------------------------------- |
| `pip`     | Environment variable export (26.1+) or shell wrapper (older)  | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `uv`      | Environment variable export                                   | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `poetry`  | `poetry config` setting                                       | `~/.config/pypoetry/config.toml`               |
| `pdm`     | `pdm config` setting (requires PDM >= 2.27.0)                 | `~/.config/pdm/config.toml`                    |
| `npm`     | `.npmrc` key                                                  | `~/.npmrc`                                     |
| `pnpm`    | `.npmrc` key                                                  | `~/.npmrc`                                     |
| `yarn`    | Environment variable export                                   | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `bun`     | `bunfig.toml` key                                             | `~/.bunfig.toml`                               |
| `deno`    | Shell aliases                                                 | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `cargo`   | Environment variable export (requires `cargo-cooldown` crate) | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |
| `bundler` | Environment variable export (requires Bundler >= 4.0.13)      | `/etc/profile.d/cooldowns.sh` (or `~/.bashrc`) |

Profile-script tools write to `/etc/profile.d/cooldowns.sh` when that directory
exists and is writable, otherwise `~/.bashrc`.

Project-only tools are **not covered**: `pipenv`, `pixi`, mise, and Scala
Steward. (`pipenv` does inherit `PIP_UPLOADED_PRIOR_TO` from
`cooldowns.sh set pip`, since it runs on `pip`.)
pinact is not covered either, but carries its own user-wide file - the global
config in [github-actions.md](github-actions.md).

`cooldowns.sh check` scans installed managers and exits non-zero on any missing
or stale cooldown, which makes it usable as a CI gate:

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
