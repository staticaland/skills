---
name: dependency-toil
description:
  Find dependency-update pull requests that sit open for days, and cut the toil
  by having Renovate or Dependabot automerge the updates that a green check
  already vouches for. Use when the user mentions a pile of bot PRs, stale
  Renovate or Dependabot PRs, automerge, auto-merge, or wants dependency updates
  to land without a person clicking merge.
version: 0.1.0
---

# Dependency Toil

**Toil** is the manual work a bot's pull request still asks of a person: open
it, see the checks are green, click merge.

**Automerge** removes the click, and only the click.

**Repository settings are the user's.** Leave every setting as it is, through
the API and the web UI alike: the user changes them.

## Procedure

### 1. Measure the toil

Run `<skill-dir>/scripts/toil.py measure`, where `<skill-dir>` is this skill's
base directory. It prints one row per open bot PR with its age, check states,
merge conflict and review state, and a provisional cause, then the cause counts, the
merged median and p90 time-to-merge, the bot config the repository tracks, and
the merge settings the API returns. Add `--author app/<bot>` for a self-hosted
bot under another login, and `--org <owner>` to rank an organization's
repositories by open bot PRs.

Done when the output is saved as the baseline the fix has to beat.

### 2. Confirm each cause

The script's cause is a lookup on states. Correct it where reading is needed:

- `red-check`: open the failing run. A flaky check is fixed in the check; a real
  break is fixed or closed in the PR.
- `no-checks` or `pending-check`: no workflow runs on the bot's branches. Add
  the branch pattern or event first; a PR with no check can never automerge
  safely.
- `conflicting`: `rebaseWhen` controls when Renovate rebases. Dependabot
  rebases on `@dependabot rebase` or on its next run.
- `review-required`: step 5, the approval workflow or a bypass for the bot.
- A burst of `toil` rows of one kind opened the same day: grouping is missing
  (`groupName`, Dependabot `groups`), not a merge step.
- Updates held on Renovate's Dependency Dashboard are not PRs. Keep the gate if
  the project chose it.

Fixing a red check or a missing workflow comes first, because automerge on a PR that never turns green is a no-op.

Done when every row's cause is confirmed and the `toil` rows are counted.

### 3. Write the policy

Decide which updates merge without a person, and write the decision down before
touching config so the config has something to match. The default that fits
most projects:

- **Automerge**: patch and minor of packages at 1.0 or above, digest and pin
  updates, lockfile maintenance.
- **Hold for a person**: major updates, anything on a `0.x` version because
  semantic versioning promises nothing about it, and a list of dependencies the
  project cannot afford to have move silently: the deploy tooling, the
  database driver, the framework.

Automerge and the cooldown from the `dependency-cooldown` skill compose. Keep
both.

Done when the policy names the update types and dependencies on each side, and
the user has agreed to the split.

### 4. Configure the bot

Read the file for the bot the repository runs:

- Renovate: [`references/renovate.md`](references/renovate.md).
- Dependabot: [`references/dependabot.md`](references/dependabot.md).

A repository running both bots gets both, and the same policy in each.

Done when the config or workflow expresses exactly the step 3 policy and
validates, and the merge method it uses is one the repository allows.

### 5. List the settings for the user

The `measure` output ends with the settings the API returns: auto-merge
allowed, the merge methods allowed, and delete-branch-on-merge. Give the user
this list, marked with what that read showed and what the user still confirms
in the repository settings:

- **Allow auto-merge** under general settings. Without it, `gh pr merge --auto`
  fails, and Renovate's `platformAutomerge` falls back to merging on its own
  schedule.
- **Branch protection or a rule set on the default branch that requires status
  checks, with at least one check selected.** Auto-merge waits for the required
  checks and nothing else. With no required check the PR is "clean" the moment
  it opens, GitHub refuses to arm auto-merge on it, and Renovate would merge
  without any test having run.
- **The required check is one the bot's PRs trigger.** A check named in
  protection that never reports leaves auto-merge armed forever.
- **Required reviews.** If the branch requires an approval, either the bot is
  on the bypass list for pull requests, or an approval workflow supplies the
  review. For Dependabot the approval step in the reference needs **Allow
  GitHub Actions to create and approve pull requests** under Actions settings.
  A CODEOWNERS review cannot be satisfied by a bot.
- **Merge queue.** If the default branch uses one, the workflow's
  `GITHUB_TOKEN` cannot add a PR to the queue; the user supplies a fine-grained
  PAT or GitHub App token as a Dependabot secret.
- **Merge method.** The `--merge`, `--squash`, or `--rebase` flag in the
  workflow, and Renovate's `automergeStrategy`, must be a method the repository
  allows.

Done when the user has the list, each item reads as confirmed or to-do, and
nothing in the repository's settings was changed by this session.

### 6. Prove it on the next PR

Wait for the next bot PR in the automerge class, or trigger one with
Dependabot's **Check for updates** or Renovate's dashboard checkbox. Then run
`<skill-dir>/scripts/toil.py verify <number>`.

Renovate's PR body line reads `Automerge: Enabled`. A Dependabot PR shows a
non-null auto-merge request after the workflow runs. Then confirm the PR merged
after its checks passed and that a PR outside the class, such as a major,
stayed open. The runs listed on the merge commit show whether the default
branch's push workflows ran, so a release pipeline downstream still sees the
change.

Done when one PR inside the policy has merged by itself with green checks, one
outside it has waited, and the step 1 measurement is scheduled to be re-run
after a month so the median moves from days to hours on the record.

Report the baseline from step 1, the cause count from step 2, the policy, the
files changed, the settings list with its confirmed and to-do items, and the PR
that proved the loop.
