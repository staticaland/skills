# Poetry cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

`solver.min-release-age` since **2.4.0**, in whole days.

```bash
poetry config solver.min-release-age 3
export POETRY_SOLVER_MIN_RELEASE_AGE=3
```

`pyproject.toml` or `~/.config/pypoetry/config.toml`:

```toml
[solver]
min-release-age = 3
```

Bypass per package or per source:

```bash
poetry config solver.min-release-age-exclude "setuptools,requests"
poetry config solver.min-release-age-exclude-source "private-repo"
```

Poetry **fails open**: a release with no upload time is installable.
