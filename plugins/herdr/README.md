# herdr

Control Herdr, a terminal multiplexer for coding agents, to inspect and drive
its panes, tabs, workspaces, and the agents running in them.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install herdr@staticaland-skills
```

## Skills

- **[herdr](./skills/herdr/SKILL.md)** (skill) - Drives the
  [Herdr](https://github.com/herdrdev/herdr) session the agent runs in through
  the `herdr` CLI. It reads neighboring panes and waits on the commands and
  agents it starts. It acts only when the user names Herdr.

## License

Apache-2.0
