# pinact

Pin every GitHub Actions reference to a commit SHA with pinact after the agent
writes or edits a workflow file.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install pinact@staticaland-skills
```

## Hooks

- **pinact** (`hooks/pinact_actions.py`) - Runs
  [pinact](https://github.com/suzuki-shunsuke/pinact) on a workflow or action
  file under `.github/workflows/` or `.github/actions/` after Claude writes or
  edits it. Requires the `pinact` CLI.

The hook runs `pinact run -u`, so it also updates every action in the file to
its latest release, major versions included. If another tool such as Renovate
or Dependabot updates your pins, leave this plugin turned off.

## License

MIT
