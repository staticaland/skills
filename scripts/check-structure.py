#!/usr/bin/env python3
"""Check that every plugin, skill, and hook is listed where it belongs.

scripts/sync-manifests.py refreshes the fields of entries that already
exist. This script finds what is missing from a list:

  - a plugin directory with no entry in .claude-plugin/marketplace.json
  - a marketplace plugin with no section in the top-level README.md
  - a skill absent from its plugin README or from the top-level catalog
  - a hook script absent from its plugin README
  - a marketplace category that is not one of the four, or that does not
    match the directory the plugin lives in

Every violation is reported, then the script exits 1. A clean repo
prints nothing and exits 0.

Usage:
  check-structure.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
README = ROOT / "README.md"
CATEGORIES = ("writing", "dev", "ai", "other")


def plugin_dirs():
    """Top-level directories that carry a plugin manifest."""
    found = []
    for path in sorted(ROOT.iterdir()):
        if path.name.startswith(".") or not path.is_dir():
            continue
        if (path / ".claude-plugin" / "plugin.json").is_file():
            found.append(path)
    return found


def skill_names(plugin_dir):
    skills = plugin_dir / "skills"
    if not skills.is_dir():
        return []
    return sorted(
        path.name for path in skills.iterdir() if (path / "SKILL.md").is_file()
    )


def hook_files(plugin_dir):
    hooks = plugin_dir / "hooks"
    if not hooks.is_dir():
        return []
    return sorted(
        path.name
        for path in hooks.iterdir()
        if path.is_file()
        and path.name != "hooks.json"
        and not path.name.startswith(".")
    )


def main():
    problems = []

    marketplace = json.loads(MARKETPLACE.read_text())
    catalog = README.read_text()

    listed = {}
    for entry in marketplace["plugins"]:
        listed[(ROOT / entry["source"]).resolve()] = entry

    for plugin_dir in plugin_dirs():
        name = plugin_dir.name
        entry = listed.get(plugin_dir)
        if entry is None:
            problems.append(
                f".claude-plugin/marketplace.json: no entry for plugin "
                f"directory {name}/ - add one with source ./{name}"
            )
            continue

        category = entry.get("category")
        if category not in CATEGORIES:
            problems.append(
                f".claude-plugin/marketplace.json: plugin {entry['name']!r} "
                f"has category {category!r} - use one of "
                f"{', '.join(CATEGORIES)}"
            )
        elif category != name:
            problems.append(
                f".claude-plugin/marketplace.json: plugin {entry['name']!r} "
                f"has category {category!r} but lives in {name}/ - set the "
                f"category to {name!r}"
            )

        readme = plugin_dir / "README.md"
        if not readme.is_file():
            problems.append(f"{name}/README.md: missing - add a README for the plugin")
            continue
        text = readme.read_text()

        if f"](./{name}/README.md)" not in catalog:
            problems.append(
                f"README.md: no catalog section for plugin {entry['name']!r} - "
                f"add one linking to ./{name}/README.md"
            )

        for skill in skill_names(plugin_dir):
            if f"](./skills/{skill}/SKILL.md)" not in text:
                problems.append(
                    f"{name}/README.md: skill {skill} is not listed - add a "
                    f"link to ./skills/{skill}/SKILL.md"
                )
            if f"](./{name}/skills/{skill}/SKILL.md)" not in catalog:
                problems.append(
                    f"README.md: skill {name}/{skill} is not in the catalog - "
                    f"add a link to ./{name}/skills/{skill}/SKILL.md"
                )

        for hook in hook_files(plugin_dir):
            if f"hooks/{hook}" not in text:
                problems.append(
                    f"{name}/README.md: hook {hook} is not listed - add an "
                    f"entry naming hooks/{hook}"
                )

    if problems:
        sys.exit("\n".join(problems))


if __name__ == "__main__":
    main()
