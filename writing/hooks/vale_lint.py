#!/usr/bin/env python3
"""PostToolUse hook: run Vale on edited or written Markdown files."""

import json
import subprocess
import sys


def main():
    hook_input = json.loads(sys.stdin.read())
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        return

    if not file_path.endswith(".md"):
        return

    result = subprocess.run(
        ["vale", file_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 and result.stdout:
        print(json.dumps({
            "result": "Vale found issues",
            "description": result.stdout.strip(),
        }), file=sys.stderr)
    elif result.returncode == 0:
        print(json.dumps({
            "result": "Vale passed",
            "description": f"No issues found in {file_path}",
        }))


if __name__ == "__main__":
    main()
