# Dependabot automerge

`dependabot.yml` has no automerge option. GitHub's own guide is
[Automating Dependabot with GitHub Actions](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/automate-dependabot-with-actions);
read the action's README for the current list of outputs.

## The workflow

One merge step per ecosystem the step 3 table automerges, each gated on
`package-ecosystem`, and no step without that gate. An ecosystem with no step
is held.

```yaml
name: Automerge Dependabot updates
on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  automerge:
    name: Enable auto-merge when the policy allows
    runs-on: ubuntu-latest
    if: github.event.pull_request.user.login == 'dependabot[bot]' && github.repository == '<owner>/<repo>'
    steps:
      - name: Read the update metadata
        id: metadata
        uses: dependabot/fetch-metadata@<sha> # v2
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
      - name: Enable auto-merge for GitHub Actions
        if: >-
          steps.metadata.outputs.package-ecosystem == 'github_actions'
          && steps.metadata.outputs.update-type != 'version-update:semver-major'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Enable auto-merge for npm development dependencies
        if: >-
          steps.metadata.outputs.package-ecosystem == 'npm_and_yarn'
          && steps.metadata.outputs.dependency-type == 'direct:development'
          && steps.metadata.outputs.update-type != 'version-update:semver-major'
          && !startsWith(steps.metadata.outputs.previous-version, '0.')
          && !contains(steps.metadata.outputs.dependency-names, '<held package>')
          && !contains(steps.metadata.outputs.dependency-names, '<another held package>')
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Fill in the placeholders:

- `<owner>/<repo>` stops the workflow running in forks.
- `<sha>` pins the action, as the `renovate-setup` skill pins every action:
  `gh api repos/dependabot/fetch-metadata/commits/v2 --jq .sha`. Keep the
  version comment so the bot can update the pin.
- `<held package>` is one entry of the hold list from the policy, and every
  held package gets its own `!contains` predicate: `contains` tests for one
  piece of text, so one predicate with a comma-separated list matches only that
  exact list. `dependency-names` is itself a comma-separated string, so
  `contains` also matches part of a longer name, and for a grouped PR it names
  every dependency in the group.

`package-ecosystem` uses Dependabot's internal names, which differ from the
keys in `dependabot.yml`: `github_actions`, `npm_and_yarn`, `pip`, `docker`,
`gomod`, `bundler`, `cargo`, `terraform`. The same string is the second segment
of every Dependabot branch name, `dependabot/<ecosystem>/...`, so read it off an
existing PR.

`update-type` is one of `version-update:semver-major`,
`version-update:semver-minor`, and `version-update:semver-patch`. A grouped PR
reports the highest level in the group, so one major in a group holds the
whole group. `dependency-type` distinguishes `direct:production`,
`direct:development`, and `indirect`.

## Token and event

A workflow that a Dependabot PR triggers runs with a read-only `GITHUB_TOKEN`
until the `permissions` block raises it, and it sees Dependabot secrets, not
Actions secrets. Keep the event on `pull_request`: `pull_request_target` runs with the
base branch's permissions on code from the PR, and this workflow checks nothing
out, so it gains nothing from the wider token. A merge step that fails with a
403 has lost that write access, to a missing `permissions` block or to an
organization policy that pins the token to read. The fallback is a fine-grained
PAT stored as a Dependabot secret and passed as `GH_TOKEN`.

`gh pr merge --auto` arms auto-merge and exits. With no required check GitHub
reports the PR as already clean and refuses to arm it, and the step fails with
that message.

## Reviews

If the branch requires an approval, add a step before the merge step with the
same `if` condition:

```yaml
- name: Approve
  run: gh pr review --approve "$PR_URL"
  env:
    PR_URL: ${{ github.event.pull_request.html_url }}
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Validate

Push the workflow, then open the next Dependabot PR:

```bash
gh run list --workflow 'Automerge Dependabot updates' --limit 5
```

A PR inside the policy shows an `autoMergeRequest` with the merge method and
the workflow's actor. A major shows `null` and a skipped merge step in the run
log. Comment `@dependabot recreate` on an open PR to have the bot open it fresh
and trigger the workflow without waiting for the schedule.
