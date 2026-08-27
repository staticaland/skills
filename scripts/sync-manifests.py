#!/usr/bin/env python3
"""Sync the derived manifest fields from each plugin's plugin.json.

A plugin's .claude-plugin/plugin.json is the source of truth for its
version and description. This script copies those fields into the files
that repeat them:

  - the plugin's entry in .claude-plugin/marketplace.json
  - the plugin's .codex-plugin/plugin.json, when that directory exists
  - the plugin's root plugin.json, the Agent Plugins manifest
    (https://agent-plugins.org/), which is the source manifest plus the
    required $schema field

marketplace.json stays the curated list of published plugins: the script
never adds or removes entries, it only refreshes version and description.
The per-plugin derived files cover every plugin under plugins/, including
drafts that marketplace.json omits on purpose.

Usage:
  sync-manifests.py          Rewrite the derived files in place.
  sync-manifests.py --check  Exit 1 when a derived file is stale.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
AGENT_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def dumps(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def sync_plugin_files(plugin_dir, stale, check):
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text())

    codex_path = plugin_dir / ".codex-plugin" / "plugin.json"
    if codex_path.parent.is_dir():
        want = manifest_path.read_text()
        if not codex_path.is_file() or codex_path.read_text() != want:
            stale.append(codex_path)
            if not check:
                codex_path.write_text(want)

    agent_plugin_path = plugin_dir / "plugin.json"
    want = dumps({"$schema": AGENT_PLUGIN_SCHEMA, **manifest})
    if not agent_plugin_path.is_file() or agent_plugin_path.read_text() != want:
        stale.append(agent_plugin_path)
        if not check:
            agent_plugin_path.write_text(want)


def main():
    check = "--check" in sys.argv[1:]
    stale = []

    for plugin_dir in sorted((ROOT / "plugins").iterdir()):
        if (plugin_dir / ".claude-plugin" / "plugin.json").is_file():
            sync_plugin_files(plugin_dir, stale, check)

    marketplace = json.loads(MARKETPLACE.read_text())
    for entry in marketplace["plugins"]:
        plugin_dir = ROOT / entry["source"]
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not manifest_path.is_file():
            sys.exit(
                f"Error: marketplace entry {entry['name']!r} has no "
                f"{manifest_path.relative_to(ROOT)}"
            )
        manifest = json.loads(manifest_path.read_text())
        if manifest["name"] != entry["name"]:
            sys.exit(
                f"Error: marketplace entry {entry['name']!r} points at "
                f"{manifest_path.relative_to(ROOT)}, which names itself "
                f"{manifest['name']!r}"
            )
        entry["version"] = manifest["version"]
        entry["description"] = manifest["description"]

    want = dumps(marketplace)
    if MARKETPLACE.read_text() != want:
        stale.append(MARKETPLACE)
        if not check:
            MARKETPLACE.write_text(want)

    if stale:
        names = ", ".join(str(path.relative_to(ROOT)) for path in stale)
        if check:
            sys.exit(
                f"Stale derived manifests: {names} - run scripts/sync-manifests.py"
            )
        print(f"Updated: {names}")


if __name__ == "__main__":
    main()
