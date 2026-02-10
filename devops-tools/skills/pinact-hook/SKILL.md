---
name: Pinact Hook
description: This skill should be used when the user asks to "pin GitHub Actions", "secure workflow actions", "set up pinact", "configure action pinning hook", or wants to prevent supply chain attacks in GitHub Actions by pinning uses directives to commit SHAs.
version: 0.1.0
---

# Pinact Hook

Configure a Claude Code `PostToolUse` hook that automatically pins GitHub Actions `uses:` directives to full commit SHAs using [pinact](https://github.com/suzuki-shunsuke/pinact).

## When to Use

Activate this skill when the user:

- Asks to pin GitHub Actions to commit SHAs
- Wants to secure GitHub Actions workflows against supply chain attacks
- Asks to set up pinact as a Claude Code hook
- Wants to ensure workflow files use immutable action references
- Asks about GitHub Actions security best practices related to pinning

## Why Pin Actions

GitHub Actions `uses:` directives reference actions by git ref. Tags are mutable: they can be reassigned or deleted. If a compromised repository pushes malicious code to an existing tag, any workflow using that tag will execute the malicious code.

Pinning to a full commit SHA makes the reference immutable:

**Mutable (risky):**

```yaml
uses: actions/checkout@v4
```

**Pinned (secure):**

```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

## Prerequisites

Install pinact before configuring the hook:

```bash
go install github.com/suzuki-shunsuke/pinact/cmd/pinact@latest
```

Or via Homebrew:

```bash
brew install suzuki-shunsuke/pinact/pinact
```

## Hook Configuration

Add the following to `.claude/settings.json` (project-level) or `~/.claude/settings.json` (user-level):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/pinact_actions.py"
          }
        ]
      }
    ]
  }
}
```

## Hook Script

Create the hook script at `~/.claude/hooks/pinact_actions.py`:

```python
#!/usr/bin/env python3
"""PostToolUse hook: run pinact on GitHub Actions workflow files."""

import json
import os
import subprocess
import sys


def main():
    tool_input = json.loads(os.environ.get("CLAUDE_TOOL_INPUT", "{}"))
    file_path = tool_input.get("file_path", "")

    if not file_path:
        return

    if "/.github/workflows/" not in file_path and "/.github/actions/" not in file_path:
        return

    if not file_path.endswith((".yml", ".yaml")):
        return

    result = subprocess.run(
        ["pinact", "run", "-u", file_path],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0 and result.stderr:
        print(json.dumps({
            "result": "Pin updated",
            "description": f"pinact pinned actions in {os.path.basename(file_path)}",
        }))
    elif result.returncode != 0:
        print(json.dumps({
            "result": "Pin failed",
            "description": result.stderr.strip(),
        }), file=sys.stderr)


if __name__ == "__main__":
    main()
```

Make it executable:

```bash
chmod +x ~/.claude/hooks/pinact_actions.py
```

## How It Works

1. Claude writes or edits a file using the `Write` or `Edit` tool
2. The `PostToolUse` hook checks if the file is a GitHub Actions workflow (`.github/workflows/*.yml` or `.github/actions/*.yml`)
3. If it matches, the hook runs `pinact run -u` on the file
4. pinact resolves mutable tags to full commit SHAs and adds version comments
5. The hook reports back to Claude what was pinned

## Output Behavior

**When setting up the hook:** Write the configuration and script files directly. Explain what the hook does and how it triggers.

**When asked about pinning:** Explain the supply chain risk and recommend the hook approach.

## Limitations

- Requires pinact installed locally
- Makes GitHub API calls to resolve SHAs (may require `GITHUB_TOKEN` for rate limits)
- Adds 1-2 seconds latency to workflow file writes
- Skips non-semantic version refs like `@main` or `@master`

## Additional Resources

For detailed examples and patterns:

- **`references/patterns.md`** - Workflow examples and common pinning scenarios
