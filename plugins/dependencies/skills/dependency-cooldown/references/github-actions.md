# GitHub Actions cooldowns

Adapted from [mprpic/cooldowns](https://github.com/mprpic/cooldowns) (MIT) /
[cooldowns.dev](https://cooldowns.dev/), the source of truth. All examples use a
three-day cooldown.

GitHub Actions has no native cooldown, but the actions a workflow references are
dependencies like any other.

**Pin actions to full commit SHAs** so a moved tag cannot change what the
workflow runs. Apply a cooldown when updating those pins.

## pinact

[pinact](https://github.com/suzuki-shunsuke/pinact) pins actions to full commit
SHAs, and `pinact run -update` moves the pins to the newest release. `-min-age`
since **v3.5.0**; `min_age` in the config file, per-action `rules`, and the
global config file since **v4.0.0**. The value is whole days, and nothing is
held back by default:

```yaml
# .pinact.yaml or .github/pinact.yaml
version: 3

min_age:
  value: 3
  # Also check the pins already in the workflows on every run; a pin
  # younger than the window exits 2. Without it, min_age only filters
  # the versions -update proposes.
  always: true
```

`-update` always filters new versions through `min_age`, by the release
publish date or the date of the commit a tag points at. When no release is old
enough, pinact exits with an error and leaves the pin as it is. Pins already in
the files are checked only under `always: true` or `-verify-min-age`.

### Per-action rules

`rules` override `min_age` for the actions an
[`expr`](https://expr-lang.org/docs/language-definition) condition matches.
Rules run in declaration order, and a later match overrides an earlier one
field by field. `min_age: 0` disables the cooldown for the matched action, and
that rule is the **bypass** for an urgent fix - add it, run
`pinact run -update`, remove it. `-min-age 0` on the command line means unset,
so it bypasses nothing.

```yaml
rules:
  # Bypass: take actions/checkout immediately. Remove after the update.
  - min_age: 0
    conditions:
      - expr: ActionRepoFullName == "actions/checkout"
  # Hold one publisher longer than the default
  - min_age: 14
    conditions:
      - expr: ActionRepoOwner == "some-org"
```

Conditions see `ActionName`, `ActionRepoOwner`, `ActionRepoName`,
`ActionRepoFullName`, `ActionVersion`, and `VersionComment`.

### Global config

pinact layers a user-wide file under the project file, read from the first of:

```text
$PINACT_GLOBAL_CONFIG
$XDG_CONFIG_HOME/pinact/pinact.yaml
~/.config/pinact/pinact.yaml
```

`pinact init -g` creates it. Merging is per field. The project's
`min_age.value` and `min_age.always` win when set. `rules` concatenate, global
first and project last, so a project rule overrides a global rule for the same
action. Set a personal baseline in the global file, and let each repo tighten or
loosen it:

```yaml
# ~/.config/pinact/pinact.yaml - personal baseline
version: 3
min_age:
  value: 3
```

```yaml
# repo .pinact.yaml - team policy, wins over the baseline
version: 3
min_age:
  value: 7
rules:
  - min_age: 0
    conditions:
      - expr: ActionRepoOwner == "my-org"
```

Precedence from highest: the `-min-age` flag, `PINACT_MIN_AGE`, the project
file, the global file. `PINACT_MIN_AGE` is one number for every action: it
outranks `min_age` in both files, outranks every `rules[].min_age`, and
switches on `-verify-min-age`. pinact's release notes recommend the global file
over the variable for a personal default. Reserve the variable for CI, where a
floor no repo can lower is the point. On a machine that exports it, the
committed file does nothing - see [env_overrides.md](env_overrides.md).

Dependabot and Renovate also update GitHub Actions and carry their own cooldown
settings - see [bot_github.md](bot_github.md) and
[bot_renovate.md](bot_renovate.md).
