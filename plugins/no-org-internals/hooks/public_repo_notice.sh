#!/usr/bin/env bash
# SessionStart hook. Tells the agent when the repository it works in is
# public, so nothing internal to the owning organization ends up in code,
# comments, commit messages, pull request descriptions, or issues.
#
# Reads the hook input on stdin and asks `gh` for the visibility of the
# repository at `cwd`. A PRIVATE or INTERNAL answer ends the hook silently.
# Any other answer emits the notice: PUBLIC, or no answer at all because `gh`
# is missing, logged out, or the remote is not on GitHub. Unknown counts as
# public, since a needless notice costs less than a leak.
#
# Runs under Claude Code and Codex. Both send `cwd` on stdin, both export
# CLAUDE_PLUGIN_ROOT for the command in hooks.json, and both add
# `hookSpecificOutput.additionalContext` to the model's context. Always exits
# 0: a hook must never keep a session from starting.

cd "$(jq -r .cwd)" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

case "$(gh repo view --json visibility -q .visibility 2>/dev/null)" in
  PRIVATE | INTERNAL) ;;
  *)
    jq -n '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:"This repository is PUBLIC. Anything you write here — code, comments, commit messages, PR descriptions, issues — is world-readable. Do not reference repositories, systems, hostnames, ticket IDs, people, or data internal to the organization owning this repo. If a change is motivated by something internal, describe the motivation in general terms without naming the source. If a task cannot be done without such a reference, say so instead of writing it."}}'
    ;;
esac
