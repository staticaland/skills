# Renovate automerge

Read the current option semantics from the
[automerge concept page](https://docs.renovatebot.com/key-concepts/automerge/)
and the [configuration options](https://docs.renovatebot.com/configuration-options/)
when a detail below disagrees with what the validator says.

## The rules

One `packageRules` entry per ecosystem the step 3 table automerges, matched on
its manager, and no rule that spans every manager. `automerge` defaults to
`false`, so an ecosystem with no rule is held without writing one. Add to the
canonical config, in its existing syntax, beside any rules the
`renovate-setup` skill wrote:

```json5
{
  packageRules: [
    {
      description: "GitHub Actions: pinned to SHAs and exercised by the checks",
      matchManagers: ["github-actions"],
      matchUpdateTypes: ["minor", "patch", "pin", "digest", "pinDigest"],
      automerge: true,
    },
    {
      description: "npm development dependencies at 1.0 or above",
      matchManagers: ["npm"],
      matchDepTypes: ["devDependencies"],
      matchUpdateTypes: ["minor", "patch"],
      matchCurrentVersion: "!/^0/",
      automerge: true,
    },
    {
      description: "Container digests behind an unchanged tag",
      matchManagers: ["dockerfile", "docker-compose"],
      matchUpdateTypes: ["digest", "pinDigest"],
      automerge: true,
    },
    {
      description: "A person merges these whatever the manager says",
      matchPackageNames: ["<database driver>", "<framework>"],
      automerge: false,
    },
  ],
  lockFileMaintenance: {
    enabled: true,
    automerge: true,
  },
}
```

Manager names come from Renovate's
[manager index](https://docs.renovatebot.com/modules/manager/). `matchDatasources`
scopes a rule the same way when one manager serves more than one registry.
`matchCurrentVersion: "!/^0/"` keeps every `0.x` package on the manual side,
because a minor of a pre-1.0 package can break anything. Rules apply in order
and later rules win, so the hold list goes after the automerge rules. `major` is
absent from every `matchUpdateTypes` on purpose. The presets `:automergeMinor`,
`:automergePatch`, and `:automergeDigest` exist, but they apply to every
manager at once, which is the switch this skill avoids.

## How Renovate merges

Renovate refuses to automerge a branch with no checks at all. `ignoreTests: true`
lifts that refusal, and belongs nowhere near a project that automerges.

`automergeType: "branch"` skips the PR and pushes to the base branch once the
branch's checks pass, raising a PR only on failure. It only works where the
base branch allows Renovate to push directly, and the check workflow must run
on `renovate/**` branches, not on `pull_request`. Prefer the default `pr` type:
the PR is the audit trail.

`automergeStrategy` picks the merge method and must be one the repository
allows. Leave it on `auto` unless the repository allows exactly one method
that differs from Renovate's choice.

## Reviews

A required review blocks automerge. On GitHub, either the administrator adds
the Renovate app to **Allow specified actors to bypass required pull requests**,
or installs the `renovate-approve` helper app. Name the one that fits and
stop.

## Validate

```bash
npx --yes --package renovate -- renovate-config-validator --strict
```

Then open any existing Renovate PR after the config merges. The PR body includes
an `Automerge:` line: `Enabled` on a PR the rule matches, `Disabled by config`
on one it holds. Renovate rewrites open PR bodies on its next run, so this is
the proof that the rule matches what the policy says, before any merge
happens.
