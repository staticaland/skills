# GitHub Dependabot cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

A bot cooldown delays the **pull request**, not resolution - anything that
resolves outside the bot still needs a native gate. For ecosystems with no
native support, this is the only gate available, so pair it with exact-version
locking.

Dependabot exempts security updates from cooldowns, so CVE fix PRs still arrive
immediately.

Since **July 2026** a three-day cooldown applies to version updates with no
configuration at all. Customize in `dependabot.yml`:

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
