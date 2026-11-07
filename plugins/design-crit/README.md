# design-crit

Run a design crit on a rendered UI and fix its alignment, spacing, hierarchy,
and collision defects, each named in designer terms.

## Install

```text
/plugin marketplace add staticaland/skills
/plugin install design-crit@staticaland-skills
```

## Skills

- **[design-crit](./skills/design-crit/SKILL.md)** (skill) - Renders the UI,
  names each defect with the designer's term for it - ragged edge, off-scale
  gap, competing focal points, clipping - measures it, fixes it at the
  source, and re-renders to confirm. It renders through the
  [agent-browser](../browser/skills/agent-browser/SKILL.md) skill when the
  `browser` plugin is installed, else through Playwright.

## License

MIT
