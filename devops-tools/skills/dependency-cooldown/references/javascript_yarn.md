# Yarn cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

`npmMinimalAgeGate` since **4.10.0**, as a **duration string**; a `1d` gate applies by default since **4.15.0**. In `.yarnrc.yml`:

```yaml
npmMinimalAgeGate: "3d"
npmPreapprovedPackages:  # bypass; globs supported
  - typescript
  - eslint
```
