"""Tests for `pr.py submit`, run with a stand-in `gh` that saves the body."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
PR = PLUGIN / "skills" / "create-pr" / "scripts" / "pr.py"
NOTICE = "**<sub>AI assisted 🤖</sub>**"

sys.path.insert(0, str(PLUGIN / "hooks"))

from session_model import record  # noqa: E402


class Submit(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name)
        self.state = self.home / ".cache" / "pull-requests-plugin" / "session-model"
        self.sent = self.home / "sent.md"
        bin_dir = self.home / "bin"
        bin_dir.mkdir()
        gh = bin_dir / "gh"
        gh.write_text(f'#!/bin/sh\ncat > "{self.sent}"\n')
        gh.chmod(0o755)
        self.path = f"{bin_dir}{os.pathsep}{os.environ['PATH']}"
        self.body = self.home / "body.md"
        self.body.write_text("<!-- hint -->\nText\n")

    def submit(self, *options, session=None):
        env = {
            **os.environ,
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "PATH": self.path,
        }
        env.pop("CLAUDE_CODE_SESSION_ID", None)
        if session:
            env["CLAUDE_CODE_SESSION_ID"] = session
        subprocess.run(
            [sys.executable, str(PR), "submit", *options, "title", str(self.body)],
            check=True,
            env=env,
        )
        return self.sent.read_text()

    def named(self, model):
        return "Text\n\n" + NOTICE.replace("</sub>", f" · {model}</sub>") + "\n"

    def test_names_no_model_when_none_is_known(self):
        self.assertEqual(self.submit(), f"Text\n\n{NOTICE}\n")

    def test_names_the_recorded_model(self):
        record("abc123", "claude-opus-5-5", self.state)
        self.assertEqual(self.submit(session="abc123"), self.named("Opus 5.5"))

    def test_names_the_stated_model_without_a_record(self):
        sent = self.submit("--model", "claude-sonnet-5", session="abc123")
        self.assertEqual(sent, self.named("Sonnet 5"))

    def test_accepts_model_with_an_equals_sign(self):
        self.assertEqual(
            self.submit("--model=gpt-5.2-codex"), self.named("gpt-5.2-codex")
        )

    def test_recorded_model_wins_over_the_stated_one(self):
        record("abc123", "claude-opus-5-5", self.state)
        sent = self.submit("--model", "claude-sonnet-5", session="abc123")
        self.assertEqual(sent, self.named("Opus 5.5"))

    def test_drops_a_stated_model_that_holds_markup(self):
        sent = self.submit("--model", "</sub>**\n# Injected")
        self.assertEqual(sent, f"Text\n\n{NOTICE}\n")


if __name__ == "__main__":
    unittest.main()
