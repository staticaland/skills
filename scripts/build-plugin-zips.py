#!/usr/bin/env python3
"""Package plugins as ZIP files for upload to Claude and ChatGPT.

Both apps install a custom plugin from a ZIP with its manifest at the root.
Claude reads .claude-plugin/plugin.json and ChatGPT reads
.codex-plugin/plugin.json, so each plugin gets one ZIP per app:

  <name>-<version>-claude.zip   without .codex-plugin/
  <name>-<version>-chatgpt.zip  without .claude-plugin/

A plugin with no .codex-plugin/ directory gets only the Claude ZIP. Only
tracked files go in, and evals/ stays out: it tests the plugin and is no
part of it.

Usage:
  build-plugin-zips.py OUT_DIR PLUGIN_DIR...
"""

import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Each target maps to the manifest directory it reads and the one it drops.
TARGETS = {
    "claude": (".claude-plugin", ".codex-plugin"),
    "chatgpt": (".codex-plugin", ".claude-plugin"),
}


def tracked_files(plugin_dir):
    out = subprocess.run(
        ["git", "ls-files", "-z", "--", plugin_dir],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [ROOT / path for path in out.split("\0") if path]


def build(plugin_dir, out_dir):
    manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
    files = [path.relative_to(plugin_dir) for path in tracked_files(plugin_dir)]
    built = []
    for target, (manifest_dir, other_manifest_dir) in TARGETS.items():
        if not (plugin_dir / manifest_dir).is_dir():
            continue
        zip_path = out_dir / f"{manifest['name']}-{manifest['version']}-{target}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for rel in files:
                if rel.parts[0] in (other_manifest_dir, "evals"):
                    continue
                archive.write(plugin_dir / rel, rel.as_posix())
        built.append(zip_path)
    return built


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__.strip().splitlines()[-1].strip())
    out_dir = Path(sys.argv[1]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    for arg in sys.argv[2:]:
        plugin_dir = (ROOT / arg).resolve()
        if not (plugin_dir / ".claude-plugin" / "plugin.json").is_file():
            sys.exit(f"Error: {arg} has no .claude-plugin/plugin.json")
        for zip_path in build(plugin_dir, out_dir):
            print(zip_path)


if __name__ == "__main__":
    main()
