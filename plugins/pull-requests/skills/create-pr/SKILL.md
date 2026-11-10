---
name: create-pr
description: >
  Create a GitHub pull request. Use when the user asks to open, create, or
  submit a PR, when work is ready for review, or whenever `gh pr create`
  would otherwise be run.
---

# create-pr

Open a PR whose description lets a reviewer judge the change without having
been in the session.

## Steps

1. Run `<skill-dir>/scripts/pr.py prepare`, where `<skill-dir>` is this
   skill's base directory. It pushes the branch, prints the template to fill,
   and prints the `BODY FILE:` path it created for this run.
2. Fill every template section from the whole session, not the diff alone.
   Cover the original request and the decisions made with their tradeoffs, and
   say what was tested and how. Follow the writing instructions in the template's comments,
   and leave the comments in place - the submit step removes them.
3. Read the `BODY FILE:` path `prepare` printed with the Read tool - the file
   is an empty placeholder, and the Write tool refuses a file it has not read.
   Then write the filled template to that exact path - never a path of your
   own choosing, which risks reusing a stale body from an earlier session.
   Then run:

   ```bash
   <skill-dir>/scripts/pr.py submit --model "<model-id>" "<title>" <body-file>
   ```

   `<model-id>` is your exact model ID as your system prompt states it,
   such as `claude-opus-5-5`. Leave `--model` out when you do not know it
   for certain.

The submit command strips the comments, adds the AI-assistance notice below
the body, and creates the PR through `gh`; the guard hook blocks a
bare `gh pr create`. The notice names the model, as in
`AI assisted 🤖 · Opus 5.5`. The script prefers the model the harness
reported for the session and falls back to `--model`.

For any other PR or issue body, such as `gh issue create` or `gh pr edit`,
write the body file with the Write tool first, then run `gh` as a separate
command.
