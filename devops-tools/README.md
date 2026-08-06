# devops-tools

Pin GitHub Actions to commit SHAs on workflow edits, parallelize workflow steps, set up dependency cooldowns, and analyze skills to split scriptable work from judgment work.

## Skills

- **[dependency-cooldown](./skills/dependency-cooldown/SKILL.md)** — Sets up a minimum release age across a project's package managers and update bots, so a compromised release is caught before it resolves; per-ecosystem references from [cooldowns.dev](https://cooldowns.dev/).
- **[parallel-steps](./skills/parallel-steps/SKILL.md)** — Makes GitHub Actions workflow steps run in parallel with the `background`, `wait`, `cancel`, and `parallel` keywords; written in ASD-STE100 Simplified Technical English.
- **[skill-analyzer](./skills/skill-analyzer/SKILL.md)** — Splits a skill into scriptable and judgment work: classifies each step as deterministic or LLM, proposes a script interface and a simplified SKILL.md.

## Hooks

- **pinact** (`hooks/pinact_actions.py`, PostToolUse on Write|Edit) — Runs [pinact](https://github.com/suzuki-shunsuke/pinact) on GitHub Actions workflow files (`.github/workflows/`, `.github/actions/`) after Claude writes or edits them, pinning action references to full commit SHAs. Requires the `pinact` CLI on your PATH.
