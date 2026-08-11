# `uv` cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

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

`exclude-newer-package` has no CLI flag or environment variable - config file only.

## Single-file scripts

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

Create the lockfile with `uv lock --script s.py`, which writes `s.py.lock` beside the script - commit it. Re-run the same command to refresh it after editing the dependencies or the cooldown.

The duration does not fight `--locked`. The lockfile records the window itself as `exclude-newer-span = "P3D"`, not the timestamp it resolved to, so it keeps verifying as the window slides forward.

Scripts carry no `pyproject.toml`, so the repo-wide inventory misses them - grep for `/// script` to find them.
