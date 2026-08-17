---
name: create-pr
description: >
  Create a GitHub pull request. Use when the user asks to open, create, or
  submit a PR, when work is ready for review, or whenever gh pr create would
  otherwise be run.
---

# create-pr

Open a PR whose description lets a reviewer judge the change without having
been in the session.

## Steps

1. Push the branch if the remote lacks its commits: `git push -u origin HEAD`.
2. Pick the template: the repo's `.github/PULL_REQUEST_TEMPLATE.md` if it
   exists, otherwise `references/pr-template.md` in this skill.
3. Fill every template section from the whole session, not the diff alone: the
   original request, the decisions made and their tradeoffs, and what was
   tested and how. Follow any writing instructions in the template's comments,
   then drop the comments from the body.
4. Write the body to a file and create the PR with the marker:

   ```bash
   SKILL_CREATE_PR=1 gh pr create --title "<title>" --body-file <file>
   ```

The `SKILL_CREATE_PR=1` marker tells the guard hook this description came
through the skill; a bare `gh pr create` is blocked.
