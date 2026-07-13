# devops-tools

Tools for securing and automating CI/CD workflows.

## Hooks

- **pinact** (`hooks/pinact_actions.py`, PostToolUse on Write|Edit) — Runs [pinact](https://github.com/suzuki-shunsuke/pinact) on GitHub Actions workflow files (`.github/workflows/`, `.github/actions/`) after Claude writes or edits them, pinning action references to full commit SHAs. Requires the `pinact` CLI on your PATH.
