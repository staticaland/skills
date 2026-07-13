# devops-tools

Pin GitHub Actions to commit SHAs automatically on workflow edits, and analyze skills to split scriptable work from judgment work.

## Skills

- **[skill-analyzer](./skills/skill-analyzer/SKILL.md)** — Splits a skill into scriptable and judgment work: classifies each step as deterministic or LLM, proposes a script interface and a simplified SKILL.md.

## Hooks

- **pinact** (`hooks/pinact_actions.py`, PostToolUse on Write|Edit) — Runs [pinact](https://github.com/suzuki-shunsuke/pinact) on GitHub Actions workflow files (`.github/workflows/`, `.github/actions/`) after Claude writes or edits them, pinning action references to full commit SHAs. Requires the `pinact` CLI on your PATH.
