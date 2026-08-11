# `pipenv` cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

`cool-down-period` since **2026.6.2**, in the `[pipenv]` section of the project `Pipfile`, as `<N>d`:

```toml
[pipenv]
cool-down-period = "3d"
```

Passes the value to `pip`'s `--uploaded-prior-to` during resolution, so it only filters against indexes that expose upload times. No environment variable, no per-package bypass - remove the setting or install through `pip` directly.
