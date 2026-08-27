# toolchain

Pin a project's tools to a mise toolchain, and run Git hooks with prek.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install toolchain@staticaland-skills
```

## Skills

- **[mise-setup](./skills/mise-setup/SKILL.md)** (skill) - Inventories
  the tools a project already uses across CI, containers, task runners, and
  per-language version files, then pins each one to a
  [mise](https://mise.jdx.dev/) backend and version in a committed `mise.toml`
  with a lockfile.
- **[prek](./skills/prek/SKILL.md)** (skill) - Sets up and runs Git hooks
  with [prek](https://prek.j178.dev/), the Rust drop-in alternative to
  pre-commit: workspace mode, built-in hooks, and shared toolchains.

## License

MIT
