# Launch a side task

Your prompt names the brief file, repo, branch, base and caller pane. Create a Herdr worktree for the branch and
start an agent in it with the brief. You cannot ask the user anything: when a step needs a decision, stop and
report the question.

## 1. Create the worktree

`herdr worktree create` refuses to start from a linked worktree (`linked_worktree_source`), so start it from the
repo's main checkout. That works even when the repo has no open Herdr workspace:

```sh
git -C <repo> fetch origin main
src=$(herdr worktree list --cwd <repo> | jq -r '.result.source.source_checkout_path')
herdr worktree create --cwd "$src" --branch <branch> --base <base> --no-focus
```

Read the new pane from `.result.root_pane.pane_id` and the workspace from `.result.workspace.workspace_id`. If the
command asks for `--trust-repository`, stop and report that. The user decides.

## 2. Start the agent and send the brief

Start an agent of the caller's kind, named after the branch (`[a-z][a-z0-9_-]{0,31}`):

```sh
kind=$(herdr pane get <caller-pane> | jq -r '.result.pane.agent')
herdr agent start <name> --kind "$kind" --pane <root-pane-id>
herdr agent prompt <name> "$(cat <brief>)"
herdr agent wait <name> --until working --until blocked --timeout 60000
```

If `agent start` returns `agent_not_ready` or the wait ends `blocked`, read the pane with
`herdr agent read <name> --source recent-unwrapped --lines 80` and report what it asks.

## 3. Report

Done when the new agent is `working`. Reply with the branch, worktree path, workspace ID and agent name, or with the
question that stopped you.
