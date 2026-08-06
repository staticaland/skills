# JavaScript cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

Every JavaScript package manager picked a different unit. Convert the chosen duration per tool: **`npm` days**, **`pnpm` minutes**, **Bun seconds**, **Yarn and Deno duration strings**.

## `npm`

`min-release-age` since **11.10.0**, in days.

```bash
npm config set min-release-age=3
```

Project `.npmrc`:

```ini
min-release-age = 3 # days
min-release-age-exclude[] = @myorg/*      # bypass, npm 11.19.0+ / 12; minimatch globs
min-release-age-exclude[] = my-internal-pkg
```

An exemption covers only the named package — its transitive dependencies still obey the gate unless they match a pattern too. `--min-release-age=0` disables the gate for one command.

## `pnpm`

`minimumReleaseAge` since **10.16.0**, in minutes.

**v11+** ships a 1440-minute (one day) default, and all non-authentication settings belong in `pnpm-workspace.yaml` (`.npmrc` is for authentication only):

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

## Yarn

`npmMinimalAgeGate` since **4.10.0**; a `1d` gate applies by default since **4.15.0**. In `.yarnrc.yml`:

```yaml
npmMinimalAgeGate: "3d"
npmPreapprovedPackages:  # bypass; globs supported
  - typescript
  - eslint
```

## Bun

`minimumReleaseAge` since **1.3**, in seconds. In `bunfig.toml`:

```toml
[install]
minimumReleaseAge = 259200 # 3 days
minimumReleaseAgeExcludes = ["@types/node", "typescript"]  # bypass
```

## Deno

`minimumDependencyAge` since **2.6**; a 24-hour gate applies by default since **2.9** and any explicit setting overrides it. Takes minutes, an ISO 8601 duration, or an RFC 3339 timestamp. In `deno.json`:

```json
{
  "minimumDependencyAge": "P3D"
}
```

Bypass with the object form:

```json
{
  "minimumDependencyAge": {
    "age": "P3D",
    "exclude": ["npm:@mycompany/cli", "jsr:@mycompany/lib"]
  }
}
```

CLI: `deno install|update|outdated --minimum-dependency-age=P3D`.
