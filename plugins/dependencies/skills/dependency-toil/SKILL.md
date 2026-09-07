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
it, see the checks are green, click merge. Repeated for every patch bump it
costs an hour a week and buys nothing, so the PRs accumulate. A backlog of
stale updates is worse than either merging or ignoring them: the fix a project
needs is buried under forty it does not, and every day open is a day the
lockfile drifts further from what the manifest says.

**Automerge** removes the click, and only the click. The check suite keeps its
vote. An update merges because a required check passed, and a person is
involved only when it fails, or when the change is one the policy holds back
for a human: a major, a pre-1.0 package, a dependency of the deploy itself.

The bots differ in where the policy is defined. Renovate keeps it in its own
config. Dependabot has no automerge setting, so a GitHub Actions workflow
enables GitHub's auto-merge on each PR the bot opens.

**Repository settings are the user's.** Automerge depends on settings that only
an administrator changes: auto-merge allowed, branch protection, required
checks. Read them where a read-only command exists, state what must hold, and
hand the list over. Leave every setting as it is, through the API and the web
UI alike: the user changes them.

## Procedure

### 1. Measure the toil

Find the bot's login first. The hosted Renovate app is `app/renovate`, a
self-hosted runner is whatever account it runs as, and Dependabot is always
`app/dependabot`:

```bash
gh pr list --state all --limit 100 --json author --jq '[.[].author.login] | unique'
```

Then age every open bot PR, with the state that explains why it is still open:

```bash
gh pr list --state open --author app/renovate --limit 200 \
  --json number,title,url,createdAt,isDraft,reviewDecision,mergeable,statusCheckRollup \
  --jq '.[] | [((now - (.createdAt | fromdateiso8601)) / 86400 | floor), .number, .reviewDecision, .mergeable, ([.statusCheckRollup[]? | .conclusion // .state] | unique | join(",")), .title] | @tsv' \
  | sort -rn
```

Add the merged history, because time-to-merge is the toil in one number:

```bash
gh pr list --state merged --author app/renovate --limit 100 --json createdAt,mergedAt \
  --jq '[.[] | ((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 86400] | sort | {merged: length, median_days: .[length / 2 | floor], p90_days: .[length * 0.9 | floor]}'
```

For a whole organization, `gh search prs --author app/dependabot --state open --owner <org> --json repository,number,createdAt,url` ranks the repositories by
backlog.

Done when every open bot PR has a row with its age in days, check state, review
state, and conflict state, and the merged median and p90 are recorded as the
baseline the fix has to beat.

### 2. Sort each stale PR by cause

Automerge cures one cause. Read the rows and give each PR one of these:

| Row looks like                                   | Cause                                              | Fix                                                                                            |
| ------------------------------------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| checks `SUCCESS`, no review, `MERGEABLE`         | **toil**: waiting for a click                      | automerge, steps 3 to 5                                                                        |
| checks `FAILURE`                                 | the update breaks the build, or the check is flaky | fix or close the PR; automerge would leave it open anyway                                      |
| checks empty or `PENDING` for days               | no workflow runs on the bot's branches             | add the branch pattern or event to the workflow; a PR with no check can never automerge safely |
| `CONFLICTING`                                    | the base moved and the bot has not rebased         | Renovate: `rebaseWhen`; Dependabot: `@dependabot rebase`, or let it rebase on its next run     |
| `reviewDecision` `REVIEW_REQUIRED`               | branch protection wants an approval no one gives   | step 5: the approval workflow, or a bypass for the bot                                         |
| a burst of PRs of one kind on the same day       | limits or grouping missing, not a merge problem    | group them (`groupName`, Dependabot `groups`) so one PR carries the batch                      |
| Renovate PR held behind the Dependency Dashboard | `dependencyDashboardApproval` gates it             | keep the gate if the project chose it; automerge is for the updates outside it                 |

The first cause is where automerge pays. Fixing a red check or a missing
workflow comes first, because automerge on a PR that never turns green is a
no-op.

Done when every PR from step 1 has a cause and the toil rows are counted
separately.

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

Automerge and the cooldown from the `dependency-cooldown` skill compose. A
release ages for the minimum release age first, and only then does the bot open
the PR that automerges, so a compromised version still gets its window to be
caught. Keep both.

Done when the policy names the update types and dependencies on each side, and
the user has agreed to the split.

### 4. Configure the bot

Read the file for the bot the repository runs:

- Renovate: [`references/renovate.md`](references/renovate.md). `automerge` in
  `packageRules`, and the PR body's `Automerge:` line as the proof.
- Dependabot: [`references/dependabot.md`](references/dependabot.md). A
  workflow on `pull_request` that runs `gh pr merge --auto` after
  `dependabot/fetch-metadata` classifies the update.

A repository running both bots gets both, and the same policy in each.

Done when the config or workflow expresses exactly the step 3 policy and
validates, and the merge method it uses is one the repository allows.

### 5. List the settings for the user

Read what a read-only command shows:

```bash
gh repo view --json autoMergeAllowed,squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge
```

Then give the user this list, marked with what the read showed and what the
user still confirms in the repository settings. Each line names the setting
and what breaks without it:

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
Dependabot's **Check for updates** or Renovate's dashboard checkbox. Observe:

```bash
gh pr view <number> --json autoMergeRequest,statusCheckRollup,mergedAt,mergedBy
```

Renovate's PR body says `Automerge: Enabled`. A Dependabot PR shows a non-null
`autoMergeRequest` after the workflow runs. Then confirm the PR merged after
its checks passed and that a PR outside the class, such as a major, stayed
open. After the first merge, check the default branch's push workflows
ran on the merge commit, so a release pipeline downstream still sees the
change.

Done when one PR inside the policy has merged by itself with green checks, one
outside it has waited, and the step 1 measurement is scheduled to be re-run
after a month so the median moves from days to hours on the record.

Report the baseline from step 1, the cause count from step 2, the policy, the
files changed, the settings list with its confirmed and to-do items, and the PR
that proved the loop.
