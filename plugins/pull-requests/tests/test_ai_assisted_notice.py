"""Tests for hooks/ai_assisted_notice.py, run as the PreToolUse hook runs it."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "ai_assisted_notice.py"
NOTICE = "**<sub>AI assisted 🤖</sub>**"


class HookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cwd = Path(self.tmp.name)

    def run_hook(self, command, env=None):
        """The deny reason the hook prints for command, or None if it allows."""
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(
                {"tool_input": {"command": command}, "cwd": str(self.cwd)}
            ),
            capture_output=True,
            text=True,
            env={**os.environ, **(env or {})},
            check=True,
        )
        if not result.stdout.strip():
            return None
        return json.loads(result.stdout)["hookSpecificOutput"][
            "permissionDecisionReason"
        ]

    def write(self, name, text):
        path = self.cwd / name
        path.write_text(text)
        return path


class InlineBody(HookTest):
    def test_allows_body_ending_with_notice(self):
        command = f"gh pr create --title t --body 'Text\n\n{NOTICE}'"
        self.assertIsNone(self.run_hook(command))

    def test_denies_body_without_notice(self):
        reason = self.run_hook("gh issue create --title t --body 'Text'")
        self.assertIn("needs the AI-assistance notice", reason)

    def test_ignores_other_commands(self):
        self.assertIsNone(self.run_hook("gh pr view 1"))


class BodyFile(HookTest):
    def test_allows_file_ending_with_notice(self):
        self.write("body.md", f"Text\n\n{NOTICE}\n")
        self.assertIsNone(self.run_hook("gh issue create -t t --body-file body.md"))

    def test_denies_file_without_notice(self):
        self.write("body.md", "Text\n")
        reason = self.run_hook("gh issue create -t t -F body.md")
        self.assertIn("needs the AI-assistance notice", reason)

    def test_expands_variables_in_path(self):
        self.write("body.md", f"Text\n\n{NOTICE}\n")
        command = 'gh issue create -t t --body-file "$BODY_DIR/body.md"'
        self.assertIsNone(self.run_hook(command, env={"BODY_DIR": str(self.cwd)}))

    def test_expands_home_in_path(self):
        self.write("body.md", f"Text\n\n{NOTICE}\n")
        command = "gh issue create -t t --body-file ~/body.md"
        self.assertIsNone(self.run_hook(command, env={"HOME": str(self.cwd)}))


class StdinBody(HookTest):
    def test_judges_heredoc_on_stdin(self):
        command = f"gh pr edit 1 --body-file - <<'EOF'\nText\n\n{NOTICE}\nEOF"
        self.assertIsNone(self.run_hook(command))

    def test_denies_heredoc_on_stdin_without_notice(self):
        command = "gh pr edit 1 --body-file - <<'EOF'\nText\nEOF"
        self.assertIn("needs the AI-assistance notice", self.run_hook(command))


if __name__ == "__main__":
    unittest.main()
