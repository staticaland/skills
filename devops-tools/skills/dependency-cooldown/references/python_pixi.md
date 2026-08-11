# `pixi` cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

`exclude-newer` since **0.67.0**, accepting an RFC 3339 timestamp, a
`YYYY-MM-DD` date, or a relative duration (anything
[`humantime`](https://docs.rs/humantime/) parses).

```toml
[workspace]
exclude-newer = "3d"

[pypi-exclude-newer]
torch = "0d"  # bypass; use [exclude-newer] for conda packages
```

Per-channel overrides are covered in the
[`pixi` security docs](https://pixi.prefix.dev/latest/security/#2-delay-fresh-uploads-with-exclude-newer).
