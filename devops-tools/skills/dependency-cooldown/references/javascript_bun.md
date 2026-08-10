# Bun cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

`minimumReleaseAge` since **1.3**, in **seconds**. In `bunfig.toml`:

```toml
[install]
minimumReleaseAge = 259200 # 3 days
minimumReleaseAgeExcludes = ["@types/node", "typescript"]  # bypass
```
