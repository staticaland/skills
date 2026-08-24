# Renovate cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

A bot cooldown delays the **pull request**, not resolution - anything that
resolves outside the bot still needs a native gate. For ecosystems with no
native support, this is the only gate available, so pair it with exact-version
locking.

Renovate exempts security updates from cooldowns, so CVE fix PRs still arrive
immediately.

`minimumReleaseAge` (formerly `stabilityDays`) has been supported for years, and
Renovate 42 made a 3-day minimum the `npm` default through the
`config:best-practices` preset. In `renovate.json`:

```json
{
  "packageRules": [
    {
      "matchUpdateTypes": ["major", "minor", "patch"],
      "minimumReleaseAge": "3 days"
    }
  ]
}
```
