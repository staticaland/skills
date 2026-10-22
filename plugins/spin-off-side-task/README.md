# spin-off-side-task

Hand a side task found in an agent's thread to a new agent in its own Herdr
worktree, with a brief that gives it the thread's context.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install spin-off-side-task@staticaland-skills
```

## Skills

- **[spin-off-side-task](./skills/spin-off-side-task/SKILL.md)** (skill) -
  Writes a brief with the task, evidence, decisions, and scope from the current
  thread, creates a Herdr worktree for it, and starts a new agent of the same
  kind there with the brief. Requires [Herdr](https://herdr.dev/) and `jq`.

## License

MIT
