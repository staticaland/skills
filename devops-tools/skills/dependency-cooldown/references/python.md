# Python cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

## `uv`

Built in since **0.9.17**. Accepts timestamp and duration formats in multiple forms.

```bash
uv pip install --exclude-newer '3 days' foo
export UV_EXCLUDE_NEWER="3 days"
```

Project config in `pyproject.toml` (or user config in `~/.config/uv/uv.toml`, without the table header):

```toml
[tool.uv]
exclude-newer = "3 days"
exclude-newer-package = { setuptools = false }  # bypass: exempt one package, revert after
```

`exclude-newer-package` has no CLI flag or environment variable — config file only.

### Single-file scripts

A [PEP 723](https://peps.python.org/pep-0723/) script resolves its own dependencies, so it needs its own cooldown in a `[tool.uv]` table inside the inline metadata block:

```python
#!/usr/bin/env -S uv run --locked --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["click"]
#
# [tool.uv]
# exclude-newer = "3 days"
# exclude-newer-package = { click = false }  # bypass: exempt one package, revert after
# ///
```

Create the lockfile with `uv lock --script s.py`, which writes `s.py.lock` beside the script — commit it. Re-run the same command to refresh it after editing the dependencies or the cooldown.

The duration does not fight `--locked`. The lockfile records the window itself as `exclude-newer-span = "P3D"`, not the timestamp it resolved to, so it keeps verifying as the window slides forward.

Scripts carry no `pyproject.toml`, so the repo-wide inventory misses them — grep for `/// script` to find them.

## `pip`

**26.1+** accepts ISO 8601 durations for `--uploaded-prior-to`.

```bash
pip install --uploaded-prior-to P3D foo
export PIP_UPLOADED_PRIOR_TO="P3D"
```

`~/.config/pip/pip.conf`:

```ini
[install]
uploaded-prior-to = P3D
```

No per-package exemption. Bypass one install with the variable unset:

```bash
env -u PIP_UPLOADED_PRIOR_TO pip install setuptools==78.1.1
```

`pip-compile` (pip-tools) passes `--uploaded-prior-to` through and honours `PIP_UPLOADED_PRIOR_TO` (needs `pip` >= 26.0).

### `pip` < 26.1

Only absolute timestamps, which go stale. Either wrap `pip` in a shell function that computes the cutoff:

```bash
pip() {
    local pip_major
    pip_major=$(command pip --version 2>/dev/null | awk '{ split($2, a, "."); print a[1]; exit }')

    case "$1" in
        install|download|wheel)
            if [[ "${pip_major:-0}" -ge 26 ]]; then
                local cutoff
                cutoff=$(date -u -d '3 days ago' '+%Y-%m-%dT%H:%M:%SZ')
                command pip "$1" --uploaded-prior-to "$cutoff" "${@:2}"
            else
                echo "warning: pip ${pip_major:-unknown} does not support --uploaded-prior-to (need >= 26), skipping cooldown" >&2
                command pip "$@"
            fi
            ;;
        *)
            command pip "$@"
            ;;
    esac
}
```

(Call `command pip` to bypass the wrapper.) Or write an absolute date into `pip.conf` and refresh it on a `cron` job — see Seth Larson's [post](https://sethmlarson.dev/pip-relative-dependency-cooling-with-crontab).

## `pipenv`

`cool-down-period` since **2026.6.2**, in the `[pipenv]` section of the project `Pipfile`, as `<N>d`:

```toml
[pipenv]
cool-down-period = "3d"
```

Passes the value to `pip`'s `--uploaded-prior-to` during resolution, so it only filters against indexes that expose upload times. No environment variable, no per-package bypass — remove the setting or install through `pip` directly.

## `poetry`

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

## PDM

`exclude-newer` since **2.26.9**, accepting a relative duration (`7d`, `12h`, `3w`) or an absolute UTC date.

```toml
[tool.pdm.resolution]
exclude-newer = "3d"
```

Global (PDM 2.27.0+): `pdm config strategy.exclude-newer 3d`, with `--local` to scope it to `.pdm.toml`. Per command: `pdm lock --exclude-newer 3d`. No environment variable.

## `pixi`

`exclude-newer` since **0.67.0**, accepting an RFC 3339 timestamp, a `YYYY-MM-DD` date, or a relative duration (anything [`humantime`](https://docs.rs/humantime/) parses).

```toml
[workspace]
exclude-newer = "3d"

[pypi-exclude-newer]
torch = "0d"  # bypass; use [exclude-newer] for conda packages
```

Per-channel overrides are covered in the [`pixi` security docs](https://pixi.prefix.dev/latest/security/#2-delay-fresh-uploads-with-exclude-newer).

## `conda`

No native cooldown. Implementation proposed in [conda#15759](https://github.com/conda/conda/issues/15759). Fall back to an update bot or a registry proxy.

## Private PyPI registries

Upload times come only from the JSON version of the PyPI Simple API, so HTML-only indexes carry no timestamps. On missing metadata, `uv` and `pip` **fail closed** (reject the version) while `poetry` **fails open**. JFrog Artifactory needs the PyPI Simple JSON API enabled, available from 7.139.1 (SaaS, February 2026) or 7.146 (self-hosted, April 2026).
