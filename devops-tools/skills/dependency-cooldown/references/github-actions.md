# GitHub Actions cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) / [cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a three-day cooldown.

GitHub Actions has no native cooldown, but the actions a workflow references are dependencies like any other. In the March 2025 [tj-actions/changed-files compromise](https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised), attackers re-pointed existing version tags at a malicious commit and leaked CI secrets from more than 20,000 repositories.

Two moves, together: **pin actions to full commit SHAs** so a moved tag cannot change what the workflow runs, and apply a cooldown when updating those pins.

## actions-up

[actions-up](https://github.com/azat-io/actions-up) scans workflows and composite actions and updates the actions they reference, pinning to full commit SHAs by default. `--min-age` since **1.6.0**, and a one-day cooldown by default since **1.16.0**. The value is days:

```bash
npx actions-up --min-age 3
```

No per-action exemption. To bypass for an urgent fix, run `--min-age 0` and select only the action needed.

Dependabot and Renovate also update GitHub Actions and carry their own cooldown settings - see [bot_github.md](bot_github.md) and [bot_renovate.md](bot_renovate.md).
