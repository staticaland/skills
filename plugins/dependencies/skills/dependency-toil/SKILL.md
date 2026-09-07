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
base directory. It recognizes an update PR from its `renovate/` or `dependabot/` branch, its label, or the shape of its title, and counts any login given with `--author` too, so a self-hosted bot under an unfamiliar login is still found. It prints one row per open update PR with its age, ecosystem, check
states, merge conflict and review state, and a provisional cause, then the cause
counts, the merged median and p90 time-to-merge, the authors counted and the bot
authors that were not, the bot config the repository tracks, and the merge
settings the API returns. Pass a bot author that should have been counted with
`--author`. `--org <owner>` ranks an organization's repositories by open update
PRs.

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

### 3. Write the policy per ecosystem

First ask what a merge to the default branch does, because that is the blast
radius of every automerge:

- **Deploys on merge:** an application that deploys from the default branch
  turns automerge into auto-deploy. Its production dependencies stay on hold.
- **Publishes at release:** a library that other projects install passes a
  runtime dependency bump on to every consumer at the next release. Its runtime
  dependencies stay on hold. Development dependencies only touch this
  repository.
- **Runs nothing:** a configuration, documentation, or tooling repository has
  no runtime, so automerge widely.

Then decide one ecosystem at a time, never with one switch for the whole
repository. A GitHub Action pinned to a SHA and a production database driver do
not share a risk, so they do not share a rule.

List the ecosystems the bot updates. Dependabot names them as
`package-ecosystem` entries in `dependabot.yml`. Renovate lists them by manager
under "Detected dependencies" on the Dependency Dashboard issue, or in the
output of `renovate --platform=local --dry-run=extract`. The `ecosystem` column
from step 1 shows which of them hold the toil.

Give each ecosystem a row: the update types that merge without a person, or
hold. The default that fits most projects:

| Ecosystem                                                             | Automerge                    | Hold                                                  |
| --------------------------------------------------------------------- | ---------------------------- | ----------------------------------------------------- |
| GitHub Actions                                                        | minor, patch, digest or SHA  | major                                                 |
| Development dependencies (`devDependencies`, Python dev groups)       | minor, patch at 1.0 or above | major, anything on `0.x`                              |
| Lock file maintenance                                                 | all                          | -                                                     |
| Container images                                                      | digest                       | tag changes                                           |
| Production application dependencies                                   | -                            | all, until a month of clean manual merges earns patch |
| Infrastructure (Terraform providers, database drivers) and frameworks | -                            | all                                                   |

`0.x` stays on hold everywhere because semantic versioning promises nothing
about it. An ecosystem starts on hold and is promoted after its PRs have merged
cleanly for a while. The step 1 measurement re-run tells when.

Automerge and the cooldown from the `dependency-cooldown` skill compose. Keep
both.

Done when every ecosystem the bot updates has a row, each row names its update
types or hold, and the user has agreed to the table.

### 4. Configure the bot

Read the file for the bot the repository runs:

- Renovate: [`references/renovate.md`](references/renovate.md).
- Dependabot: [`references/dependabot.md`](references/dependabot.md).

A repository running both bots gets both, and the same policy in each.

Done when the config or workflow has one rule or step per automerged ecosystem
from the step 3 table and nothing broader, validates, and the merge method it
uses is one the repository allows.

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
