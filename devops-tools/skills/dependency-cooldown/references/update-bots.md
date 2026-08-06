# Update bot cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

A bot cooldown delays the **pull request**, not resolution — anything that resolves outside the bot still needs a native gate. For ecosystems with no native support, this is the only gate available, so pair it with exact-version locking.

Both bots **exempt security updates** from cooldowns, so CVE fix PRs still arrive immediately.

## Renovate

`minimumReleaseAge` (formerly `stabilityDays`) has been supported for years, and Renovate 42 made a 3-day minimum the `npm` default through the `config:best-practices` preset. In `renovate.json`:

```json
{
  "packageRules": [
    {
      "matchUpdateTypes": [
        "major",
        "minor",
        "patch"
      ],
      "minimumReleaseAge": "3 days"
    }
  ]
}
```

## Dependabot

Since **July 2026** a three-day cooldown applies to version updates with no configuration at all. Customize in `dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: pip
    directory: /
    schedule:
      interval: daily
    cooldown:
      default-days: 3
      semver-major-days: 7
      semver-minor-days: 3
      semver-patch-days: 3
```

## Ecosystems with no native cooldown

Go ([open proposal](https://github.com/golang/go/issues/76485), not accepted), [NuGet](https://github.com/NuGet/Home/issues/14657), [Composer](https://github.com/composer/composer/issues/12633), [Dart's pub](https://github.com/dart-lang/pub/issues/4791), Swift Package Manager (no request filed), Maven/Gradle, and `conda`.

For all of these: lock dependencies to exact versions, configure the bot cooldown above, and consider a [registry-level proxy](containers-and-proxies.md). Maven projects can also use [Scala Steward](jvm.md), though it is little used outside Scala and does not officially support Gradle.
