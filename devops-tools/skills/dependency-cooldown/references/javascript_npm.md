# `npm` cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

`min-release-age` since **11.10.0**, in **days**.

```bash
npm config set min-release-age=3
```

Project `.npmrc`:

```ini
min-release-age = 3 # days
min-release-age-exclude[] = @myorg/*      # bypass, npm 11.19.0+ / 12; minimatch globs
min-release-age-exclude[] = my-internal-pkg
```

An exemption covers only the package - its transitive dependencies still obey the gate unless they match a pattern too. `--min-release-age=0` disables the gate for one command.
