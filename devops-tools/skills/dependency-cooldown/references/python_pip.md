# `pip` cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

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

## `pip` < 26.1

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
