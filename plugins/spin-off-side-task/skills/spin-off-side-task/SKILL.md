---
name: spin-off-side-task
description: Hand a side task found in the current thread to a new agent in its own Herdr worktree, with a brief that gives it the thread's context. Use when the user asks to spin off or hand off a fix, or to make a separate PR for something this thread found, while this session keeps its own task.
---

# Spin off a side task

A **side task** is work this thread found but does not own: a slow CI job spotted while reviewing a PR, a bug next
to the one being fixed. It gets its own branch, worktree and agent, so this session's branch and focus stay
untouched. The new agent starts with nothing but the brief and the repo, so the brief is the whole hand-off.

Run every command from this session's pane. Check `test "${HERDR_ENV:-}" = 1` first; if it fails, tell the user
this session is not inside Herdr and stop.

## 1. Write the brief

Write it to a temporary file. The new agent must be able to act on it without asking what it means:

- **Task**: what to change and what the result should be, in one or two sentences.
- **Evidence**: what this thread found, copied in full: log lines, numbers, file paths, PR and issue numbers,
  commands that reproduce it. Mark guesses as guesses and say what would confirm them.
- **Decisions**: every choice the user already made in the thread, and options they turned down with the reason,
  so the new agent does not reopen them.
- **Scope**: where the side task ends, and which parts stay with this session.
- **Finish**: what the user asked for. Default to "commit locally with small atomic conventional commits; do not
  push or open a pull request". Allow a push or PR only when the user asked for one, as in "make a new PR".
- **Source**: a pointer back to this thread, so the new agent can read more when the brief leaves a question open:

  ```text
  This side task comes from Herdr pane <HERDR_PANE_ID>. Read it for more context with:

      herdr pane read '<HERDR_PANE_ID>' --lines 400 --source recent-unwrapped
  ```

Done when a reader with only the brief and the repo could start the work.

## 2. Create the worktree

Pick a short kebab-case branch name for the side task. Base it on `origin/main` after `git fetch origin main`. Base
it on `HEAD` only when the side task needs commits that exist only on this branch, and say so in the brief.

`herdr worktree create` refuses to start from a linked worktree (`linked_worktree_source`), so start it from the
repo's parent workspace:

```sh
src=$(herdr worktree list --cwd "$PWD" | jq -r '.result.source.source_workspace_id')
herdr worktree create --workspace "$src" --branch <branch> --base origin/main --no-focus
```

Read the new pane from `.result.root_pane.pane_id` and the workspace from `.result.workspace.workspace_id`. If the
command asks for `--trust-repository`, ask the user. Add it only when they say so.

## 3. Start the agent and send the brief

Start an agent of this session's kind, named after the branch (`[a-z][a-z0-9_-]{0,31}`):

```sh
kind=$(herdr pane get "$HERDR_PANE_ID" | jq -r '.result.pane.agent')
herdr agent start <name> --kind "$kind" --pane <root-pane-id>
herdr agent prompt <name> "$(cat <brief-file>)"
herdr agent wait <name> --until working --until blocked --timeout 60000
```

If `agent start` returns `agent_not_ready` or the wait ends `blocked`, read the pane with
`herdr agent read <name> --source recent-unwrapped --lines 80` and show the user what it asks; leave the answer to
them.

Done when the new agent is `working`.

## 4. Report and return

Tell the user the branch, workspace ID and agent name in one or two lines, then go back to this session's own
task. The side task belongs to the new agent now, so leave its files and branch alone.
