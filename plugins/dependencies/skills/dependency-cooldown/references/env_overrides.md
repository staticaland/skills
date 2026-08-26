# Environment variables that outrank project config

Several managers rank an environment variable above the project file. On a
machine that exports the variable - the user-wide
[`cooldowns.sh`](cooldowns_sh.md) helper does exactly that - the tool obeys the
variable and the committed setting does nothing, with no error. CI without the variable obeys
the file, so the same command resolves differently on the two machines, and a
verification run on the wrong machine passes for the wrong reason.

| Variable                        | Tool                     | Against the committed setting                                          |
| ------------------------------- | ------------------------ | ---------------------------------------------------------------------- |
| `UV_EXCLUDE_NEWER`              | `uv`                     | Wins over `exclude-newer` in `pyproject.toml` and `uv.toml`            |
| `PIP_UPLOADED_PRIOR_TO`         | `pip`, pip-tools, `pipenv` | Wins over `uploaded-prior-to` at every `pip.conf` level              |
| `POETRY_SOLVER_MIN_RELEASE_AGE` | Poetry                   | Wins over `solver.min-release-age` in config files                     |
| `npm_config_min_release_age`    | `npm`                    | Wins over `min-release-age` in the project `.npmrc`                    |
| `YARN_NPM_MINIMAL_AGE_GATE`     | Yarn                     | Wins over `npmMinimalAgeGate` in `.yarnrc.yml`                         |
| `BUNDLE_COOLDOWN`               | Bundler                  | **Loses** to a committed `.bundle/config`; wins over the global config |
| `COOLDOWN_MINUTES`              | cargo-cooldown           | No conflict - the variable is the only place the duration lives        |

Shell wrappers shadow the same way: `cooldowns.sh` installs a `pip` function
and `deno` aliases that inject a CLI flag, and a flag outranks even the
variables. `type pip deno` exposes them.

## What to do on a difference

Leave the user's environment alone - it is their machine-wide gate and may be
deliberate. Warn instead: show the variable's value next to the committed one
and say which of the two this machine obeys. CI has no such variable and reads
only the committed file. A difference in either direction misleads - a longer
window in the environment adds friction the repo never asked for, a shorter one
weakens the gate the repo promises.
