#!/usr/bin/env python3
"""PostToolUse hook: run pinact on GitHub Actions workflow files."""

import json
import os
import subprocess
import sys


def main():
    hook_input = json.loads(sys.stdin.read())
    tool_input = hook_input.get("tool_input", {})
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
