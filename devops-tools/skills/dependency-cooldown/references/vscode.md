# VS Code extension cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

`extensions.autoUpdateDelay` since **1.125** (1.123 shipped a fixed two-hour delay; 1.125 made it configurable). The value is hours, defaulting to `2`. In `settings.json`:

```json
"extensions.autoUpdateDelay": 72
```

Two limits: it applies only when extension auto-update is enabled, and it gates **updates to installed extensions only, not first installs**. A broader `minimumReleaseAge` request ([vscode#316867](https://github.com/microsoft/vscode/issues/316867)) was closed without shipping that part. Until it does, review changelogs before installing a brand-new extension and pin extension versions where possible.
