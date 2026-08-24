# pull-requests

Open a GitHub pull request from the repository's own template, and manage
stacked branches and pull requests with gh-stack.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install pull-requests@staticaland-skills
```

## Skills

- **[create-pr](./skills/create-pr/SKILL.md)** (skill) - Opens a GitHub
  pull request with `gh`, filling the repo's PR template or the skill's bundled
  one.
- **[gh-stack](./skills/gh-stack/SKILL.md)** (skill) - Manages stacked
  branches and pull requests with the
  [gh-stack](https://github.com/github/gh-stack) GitHub CLI extension: create,
  view, push, submit, sync, rebase, merge, and check out a stack.

## Hooks

- **pr-create guard** (`hooks/pr_create_guard.py`) - Blocks a direct
  `gh pr create` and tells Claude to invoke the create-pr skill
  instead. Other `git` and `gh` commands are untouched.

## License

MIT
