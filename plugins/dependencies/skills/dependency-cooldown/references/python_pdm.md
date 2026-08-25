# PDM cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

`exclude-newer` since **2.26.9**, accepting a relative duration (`7d`, `12h`,
`3w`) or an absolute UTC date.

```toml
[tool.pdm.resolution]
exclude-newer = "3d"
```

Global (PDM 2.27.0+): `pdm config strategy.exclude-newer 3d`, with `--local` to
scope it to `.pdm.toml`. Per command: `pdm lock --exclude-newer 3d`. No
environment variable.
