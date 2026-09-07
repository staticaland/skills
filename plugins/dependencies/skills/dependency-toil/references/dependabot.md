# Dependabot automerge

`dependabot.yml` has no automerge option. The policy is a GitHub Actions
workflow that runs on each Dependabot PR, classifies the update with
`dependabot/fetch-metadata`, and arms GitHub's auto-merge with
`gh pr merge --auto`. GitHub's own guide is
[Automating Dependabot with GitHub Actions](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/automate-dependabot-with-actions);
read the action's README for the current list of outputs.

## The workflow

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
      - name: Enable auto-merge
        if: >-
          contains(fromJSON('["version-update:semver-minor", "version-update:semver-patch"]'), steps.metadata.outputs.update-type)
          && !startsWith(steps.metadata.outputs.previous-version, '0.')
          && !contains(steps.metadata.outputs.dependency-names, '<deploy tool>')
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Fill in the three placeholders:

- `<owner>/<repo>` stops the workflow running in forks.
- `<sha>` pins the action, as the `renovate-setup` skill pins every action:
  `gh api repos/dependabot/fetch-metadata/commits/v2 --jq .sha`. Keep the
  version comment so the bot can update the pin.
- `<deploy tool>` is the hold list from the policy. `dependency-names` is a
  comma-separated string, so `contains` also matches part of a longer name, and
  for a grouped PR it names every dependency in the group.

Use a merge method the repository allows: `--squash`, `--merge`, or
`--rebase`.

`update-type` is one of `version-update:semver-major`,
`version-update:semver-minor`, and `version-update:semver-patch`. A grouped PR
reports the highest level in the group, so one major in a group holds the
whole group. `dependency-type` distinguishes `direct:production`,
`direct:development`, and `indirect` when the policy automerges development
dependencies more freely.

## Token and event

A workflow that a Dependabot PR triggers runs with a read-only `GITHUB_TOKEN`
until the `permissions` block raises it, and it sees Dependabot secrets, not
Actions secrets. The block above grants exactly what `gh pr merge --auto`
needs. Keep the event on `pull_request`: `pull_request_target` runs with the
base branch's permissions on code from the PR, and this workflow checks nothing
out, so it gains nothing from the wider token.

`gh pr merge --auto` arms auto-merge and exits. The merge happens when the
required checks pass, which depends on **Allow auto-merge** on the repository
and on branch protection or a rule set that requires at least one status
check. Both are the user's settings. With no required check GitHub reports the
PR as already clean and refuses to arm it, and the step fails with that
message.

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

The approval counts only when the administrator has enabled **Allow GitHub
Actions to create and approve pull requests** under the repository's Actions
settings, and a CODEOWNERS requirement is never met by a bot. State both and
leave the change to the user.

## Validate

Push the workflow, then open the next Dependabot PR:

```bash
gh pr view <number> --json autoMergeRequest --jq .autoMergeRequest
gh run list --workflow 'Automerge Dependabot updates' --limit 5
```

A PR inside the policy shows an `autoMergeRequest` with the merge method and
the workflow's actor. A major shows `null` and a skipped merge step in the run
log. Comment `@dependabot recreate` on an open PR to have the bot open it fresh
and trigger the workflow without waiting for the schedule.
