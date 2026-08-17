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

1. Run `<skill-dir>/scripts/pr.sh prepare`, where `<skill-dir>` is this
   skill's base directory. It pushes the branch if the remote lacks its
   commits and prints the template to fill.
2. Fill every template section from the whole session, not the diff alone: the
   original request, the decisions made and their tradeoffs, and what was
   tested and how. Follow the writing instructions in the template's comments,
   and leave the comments in place - the submit step removes them.
3. Write the filled template to a file and run:

   ```bash
   <skill-dir>/scripts/pr.sh submit "<title>" <body-file>
   ```

The submit command strips the comments and adds the `SKILL_CREATE_PR=1` marker
that tells the guard hook this PR came through the skill; a bare
`gh pr create` is blocked.
