# Renovate automerge

Renovate keeps the automerge policy in its own config, so the whole fix is a
`packageRules` entry. Read the current option semantics from the
[automerge concept page](https://docs.renovatebot.com/key-concepts/automerge/)
and the [configuration options](https://docs.renovatebot.com/configuration-options/)
when a detail below disagrees with what the validator says.

## The rule

Add to the canonical config, in its existing syntax, beside any rules the
`renovate-setup` skill wrote:

```json5
{
  packageRules: [
    {
      description: "Automerge non-major updates of stable packages",
      matchUpdateTypes: ["minor", "patch", "pin", "digest", "pinDigest"],
      matchCurrentVersion: "!/^0/",
      automerge: true,
    },
    {
      description: "A person merges these",
      matchPackageNames: ["<deploy tool>", "<framework>"],
      automerge: false,
    },
  ],
  lockFileMaintenance: {
    enabled: true,
    automerge: true,
  },
}
```

`matchCurrentVersion: "!/^0/"` keeps every `0.x` package on the manual side,
because a minor of a pre-1.0 package can break anything. Rules apply in order
and later rules win, so the hold list goes after the automerge rule. `major` is
absent from `matchUpdateTypes` on purpose. The presets `:automergeMinor`,
`:automergePatch`, and `:automergeDigest` exist, but a written rule shows the
policy in one place instead of behind a preset name.

`automerge` is `false` by default, and a `minimumReleaseAge` already in the
config still applies. Renovate opens the PR when the release has aged, and
automerges it when the checks pass.

## How Renovate merges

`platformAutomerge` defaults to `true`, so Renovate arms GitHub's own auto-merge
on the PR, and GitHub merges the moment the required checks pass. This needs the
repository's **Allow auto-merge** setting, and branch protection that requires
at least one status check, otherwise GitHub can merge a PR whose tests failed.
Without platform automerge Renovate merges the PR itself on a later run, once
it sees passing checks, so a merge can take a couple of hours.

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
or installs the `renovate-approve` helper app. Both are the user's settings
change. Name the one that fits and stop.

## Validate

```bash
npx --yes --package renovate -- renovate-config-validator --strict
```

Then open any existing Renovate PR after the config merges. The PR body includes
an `Automerge:` line: `Enabled` on a PR the rule matches, `Disabled by config`
on one it holds. Renovate rewrites open PR bodies on its next run, so this is
the proof that the rule matches what the policy says, before any merge
happens.
