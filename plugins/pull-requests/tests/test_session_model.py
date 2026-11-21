"""Tests for hooks/session_model.py."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
HOOK = HOOKS / "session_model.py"

sys.path.insert(0, str(HOOKS))

from session_model import display_name, lookup, record  # noqa: E402


class DisplayName(unittest.TestCase):
    def test_names_claude_models(self):
        cases = {
            "claude-opus-5-5": "Opus 5.5",
            "claude-opus-5": "Opus 5",
            "claude-fable-5-2": "Fable 5.2",
            "claude-sonnet-4-5-20250929": "Sonnet 4.5",
            "claude-opus-4-20250514": "Opus 4",
            "claude-3-5-sonnet-20241022": "Sonnet 3.5",
            "claude-3-opus-20240229": "Opus 3",
            "claude-opus-5-5[1m]": "Opus 5.5",
            "us.anthropic.claude-opus-5-5-v1:0": "Opus 5.5",
            "claude-sonnet-5@20260101": "Sonnet 5",
        }
        for model, name in cases.items():
            with self.subTest(model=model):
                self.assertEqual(display_name(model), name)

    def test_keeps_other_ids_and_names(self):
        for model in ("gpt-5.2-codex", "Opus 5.5", "my-gateway/custom"):
            with self.subTest(model=model):
                self.assertEqual(display_name(model), model)

    def test_rejects_values_that_are_not_a_model_name(self):
        for model in (None, "", "  ", 5, "<b>x</b>", "a\nb", "**x**", "x" * 61):
            with self.subTest(model=model):
                self.assertIsNone(display_name(model))


class Record(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name) / "state"

    def test_looks_up_what_was_recorded(self):
        record("abc-123", "claude-opus-5-5", self.dir)
        self.assertEqual(lookup("abc-123", self.dir), "claude-opus-5-5")

    def test_last_record_wins(self):
        record("abc-123", "claude-opus-5-5", self.dir)
        record("abc-123", "claude-sonnet-5", self.dir)
        self.assertEqual(lookup("abc-123", self.dir), "claude-sonnet-5")

    def test_unknown_session_has_no_model(self):
        self.assertIsNone(lookup("abc-123", self.dir))
        self.assertIsNone(lookup(None, self.dir))

    def test_ignores_a_session_id_that_is_a_path(self):
        record("../escape", "claude-opus-5-5", self.dir)
        self.assertFalse((self.dir.parent / "escape").exists())
        self.assertIsNone(lookup("../escape", self.dir))

    def test_ignores_a_missing_model(self):
        record("abc-123", None, self.dir)
        self.assertIsNone(lookup("abc-123", self.dir))

    def test_removes_old_records(self):
        record("old", "claude-opus-5", self.dir)
        os.utime(self.dir / "old", (0, 0))
        record("new", "claude-opus-5-5", self.dir)
        self.assertIsNone(lookup("old", self.dir))
        self.assertEqual(lookup("new", self.dir), "claude-opus-5-5")


class Hook(unittest.TestCase):
    """The hook as Claude Code runs it, with HOME pointed at a scratch dir."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name)
        self.dir = self.home / ".cache" / "pull-requests-plugin" / "session-model"

    def run_hook(self, stdin):
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=stdin,
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": str(self.home), "USERPROFILE": str(self.home)},
        )

    def test_session_start_records_model(self):
        payload = {
            "session_id": "abc123",
            "hook_event_name": "SessionStart",
            "source": "startup",
            "model": "claude-opus-5",
        }
        result = self.run_hook(json.dumps(payload))
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        self.assertEqual(lookup("abc123", self.dir), "claude-opus-5")

    def test_post_model_switch_records_to_model(self):
        record("abc123", "claude-sonnet-5", self.dir)
        payload = {
            "session_id": "abc123",
            "hook_event_name": "PostModelSwitch",
            "from_model": "claude-sonnet-5",
            "to_model": "claude-opus-5",
        }
        self.run_hook(json.dumps(payload))
        self.assertEqual(lookup("abc123", self.dir), "claude-opus-5")

    def test_session_start_without_model_keeps_quiet(self):
        payload = {"session_id": "abc123", "hook_event_name": "SessionStart"}
        result = self.run_hook(json.dumps(payload))
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        self.assertIsNone(lookup("abc123", self.dir))

    def test_bad_input_does_not_fail(self):
        result = self.run_hook("not json")
        self.assertEqual((result.returncode, result.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
