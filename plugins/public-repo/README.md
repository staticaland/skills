# public-repo

Tell the agent at session start when the repository is public, so nothing
internal to its owner leaks into code, commits, or pull requests.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install public-repo@staticaland-skills
```

A `.codex-plugin/plugin.json` manifest sits next to the Claude Code one, and
Codex reads the same `hooks/hooks.json`, so the hook runs under both agents.

## Hooks

- **public repository notice** (`hooks/public_repo_notice.sh`) - Asks `gh`
  for the visibility of the repository at session start. Unless the answer is
  private or internal, it tells the agent that the repository is public and
  that internal repositories, systems, hostnames, ticket IDs, people, and data
  stay out of everything it writes. An unknown visibility counts as public.
  Requires the `gh` CLI and `jq`.

## License

MIT
