# pull-requests

Open a GitHub pull request from the repository's own template, manage stacked
branches and pull requests with gh-stack, and attach images and videos to
issues and pull requests.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install pull-requests@staticaland-skills
```

## Skills

- **[create-pr](./skills/create-pr/SKILL.md)** (skill) - Opens a GitHub
  pull request with `gh`, filling the skill's PR template.
- **[gh-attach](./skills/gh-attach/SKILL.md)** (skill) - Uploads an image
  or video to a GitHub issue, pull request, or comment with the `gh --attach`
  flag, and controls where it renders in the body.
- **[gh-stack](./skills/gh-stack/SKILL.md)** (skill) - Manages stacked
  branches and pull requests with the
  [gh-stack](https://github.com/github/gh-stack) GitHub CLI extension: create,
  view, push, submit, sync, rebase, merge, and check out a stack.

## Hooks

- **pr-create guard** (`hooks/pr_create_guard.py`) - Blocks a direct
  `gh pr create` and tells Claude to invoke the create-pr skill
  instead. Other `git` and `gh` commands are untouched.
- **AI-assistance notice** (`hooks/ai_assisted_notice.py`) - Requires the
  body of a `gh pr create`, `gh pr edit`, `gh issue create`, or
  `gh issue edit` to end with the line
  `**<sub>AI assisted 🤖</sub>**`. The line may name the model, as in
  `**<sub>AI assisted 🤖 · Opus 5.5</sub>**`. Denies the call and quotes the
  line until the body has it. The create-pr skill adds it for you, with the
  model name when it is known.
- **session model** (`hooks/session_model.py`) - Records the model a
  Claude Code session runs on, from `SessionStart` and `PostModelSwitch` hook
  input. The create-pr skill reads the record to name the model in the notice.

## License

MIT
