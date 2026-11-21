"""Tests for hooks/ai_assisted_notice.py, run as the PreToolUse hook runs it."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
HOOK = HOOKS / "ai_assisted_notice.py"
NOTICE = "**<sub>AI assisted 🤖</sub>**"
NAMED = "**<sub>AI assisted 🤖 · Opus 5.5</sub>**"

sys.path.insert(0, str(HOOKS))

from ai_assisted_notice import wrap  # noqa: E402


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

    def test_allows_notice_that_names_a_model(self):
        command = f"gh pr create --title t --body 'Text\n\n{NAMED}'"
        self.assertIsNone(self.run_hook(command))

    def test_allows_notice_that_names_a_raw_model_id(self):
        named = NOTICE.replace("</sub>", " · gpt-5.2-codex</sub>")
        command = f"gh pr edit 1 --body 'Text\n\n{named}'"
        self.assertIsNone(self.run_hook(command))

    def test_denies_notice_that_is_not_last(self):
        command = f"gh pr create --title t --body '{NAMED}\n\nText'"
        self.assertIn("needs the AI-assistance notice", self.run_hook(command))

    def test_denies_altered_notice(self):
        altered = NOTICE.replace("</sub>", " by Opus</sub>")
        command = f"gh pr create --title t --body 'Text\n\n{altered}'"
        self.assertIn("needs the AI-assistance notice", self.run_hook(command))

    def test_denies_body_without_notice(self):
        reason = self.run_hook("gh issue create --title t --body 'Text'")
        self.assertIn("needs the AI-assistance notice", reason)

    def test_ignores_other_commands(self):
        self.assertIsNone(self.run_hook("gh pr view 1"))


class BodyFile(HookTest):
    def test_allows_file_ending_with_notice(self):
        self.write("body.md", f"Text\n\n{NOTICE}\n")
        self.assertIsNone(self.run_hook("gh issue create -t t --body-file body.md"))

    def test_allows_file_ending_with_notice_that_names_a_model(self):
        self.write("body.md", f"Text\n\n{NAMED}\n")
        self.assertIsNone(self.run_hook("gh pr edit 1 --body-file body.md"))

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


class UnreadableBodyFile(HookTest):
    def test_denies_missing_file_without_asking_for_the_notice(self):
        reason = self.run_hook("gh issue create -t t --body-file missing.md")
        self.assertIn("missing.md does not exist or cannot be read", reason)
        self.assertIn("nothing in it ran", reason)
        self.assertIn("separate step", reason)
        self.assertNotIn(NOTICE, reason)
        self.assertNotIn("Add this line", reason)

    def test_denies_file_another_step_writes(self):
        command = "printf 'Text' > body.md && gh pr create -t t -F body.md"
        reason = self.run_hook(command)
        self.assertIn("does not exist or cannot be read", reason)

    def test_denies_directory(self):
        (self.cwd / "dir").mkdir()
        reason = self.run_hook("gh issue edit 1 --body-file dir")
        self.assertIn("does not exist or cannot be read", reason)


class HeredocWritesBodyFile(HookTest):
    def test_judges_heredoc_redirected_before_the_tag(self):
        command = (
            f"cat > \"$BODY_DIR/body.md\" <<'EOF'\nText\n\n{NOTICE}\nEOF\n"
            'gh issue create -t t --body-file "$BODY_DIR/body.md"'
        )
        self.assertIsNone(self.run_hook(command, env={"BODY_DIR": str(self.cwd)}))

    def test_judges_heredoc_redirected_after_the_tag(self):
        command = (
            f"cat <<'EOF' > body.md\nText\n\n{NOTICE}\nEOF\n"
            "gh pr create -t t -F body.md"
        )
        self.assertIsNone(self.run_hook(command))

    def test_reads_flags_past_an_apostrophe_in_the_heredoc(self):
        command = (
            f"cat > \"$BODY_DIR/body.md\" <<'EOF'\nIt doesn't work.\n\n{NOTICE}\nEOF\n"
            'gh issue create --title "x" --body-file "$BODY_DIR/body.md" -l bug'
        )
        self.assertIsNone(self.run_hook(command, env={"BODY_DIR": str(self.cwd)}))

    def test_denies_heredoc_without_notice(self):
        command = "cat > body.md <<EOF\nText\nEOF\ngh pr create -t t -F body.md"
        reason = self.run_hook(command)
        self.assertIn("in the heredoc that writes body.md", reason)
        self.assertIn(NOTICE, reason)

    def test_heredoc_wins_over_stale_file(self):
        self.write("body.md", f"Old\n\n{NOTICE}\n")
        command = (
            "mkdir -p x && cat > ./body.md <<'EOF'\nNew\nEOF\n"
            "gh issue edit 1 -F body.md"
        )
        self.assertIn("needs the AI-assistance notice", self.run_hook(command))

    def test_ignores_heredoc_written_elsewhere(self):
        command = (
            f"cat > other.md <<'EOF'\nText\n\n{NOTICE}\nEOF\n"
            "gh issue create -t t -F body.md"
        )
        self.assertIn("does not exist or cannot be read", self.run_hook(command))


class StdinBody(HookTest):
    def test_judges_heredoc_on_stdin(self):
        command = f"gh pr edit 1 --body-file - <<'EOF'\nText\n\n{NOTICE}\nEOF"
        self.assertIsNone(self.run_hook(command))

    def test_judges_heredoc_on_stdin_that_names_a_model(self):
        command = f"gh pr edit 1 --body-file - <<'EOF'\nText\n\n{NAMED}\nEOF"
        self.assertIsNone(self.run_hook(command))

    def test_denies_heredoc_on_stdin_without_notice(self):
        command = "gh pr edit 1 --body-file - <<'EOF'\nText\nEOF"
        self.assertIn("needs the AI-assistance notice", self.run_hook(command))


class Wrap(unittest.TestCase):
    def test_adds_plain_notice_without_a_model(self):
        self.assertEqual(wrap("Text\n"), f"Text\n\n{NOTICE}\n")

    def test_names_the_model(self):
        self.assertEqual(wrap("Text\n", "Opus 5.5"), f"Text\n\n{NAMED}\n")

    def test_adds_the_model_to_a_plain_notice(self):
        self.assertEqual(wrap(f"Text\n\n{NOTICE}\n", "Opus 5.5"), f"Text\n\n{NAMED}\n")

    def test_keeps_a_named_notice_without_a_model(self):
        self.assertEqual(wrap(f"Text\n\n{NAMED}\n"), f"Text\n\n{NAMED}\n")


if __name__ == "__main__":
    unittest.main()
