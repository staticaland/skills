# `pnpm` cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

`minimumReleaseAge` since **10.16.0**, in **minutes**.

**v11+** defaults to 1440 minutes (one day), and all non-authentication settings belong in `pnpm-workspace.yaml` (`.npmrc` is for authentication only):

```yaml
minimumReleaseAge: 4320 # 3 days
minimumReleaseAgeExclude:
  - webpack
  - react
```

**v10** defaults to 0 (disabled) and reads `.npmrc`:

```ini
minimum-release-age=4320
```

The v10 exclude list still requires `pnpm-workspace.yaml`.
