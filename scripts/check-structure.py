#!/usr/bin/env python3
"""Check that every plugin, skill, and hook is listed where it belongs.

scripts/sync-manifests.py refreshes the fields of entries that already
exist. This script finds what is missing from a list:

  - a plugin directory under plugins/ with no entry in
    .claude-plugin/marketplace.json
  - a marketplace plugin with no section in the top-level README.md
  - a skill absent from its plugin README or from the top-level catalog
  - a hook script absent from its plugin README
  - a marketplace category that is not one of the four
  - a SKILL.md outside plugins/<plugin>/skills/<name>/, where no plugin
    loads it

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
PLUGINS = ROOT / "plugins"
README = ROOT / "README.md"
CATEGORIES = ("writing", "dev", "ai", "other")
# Local copies of a vendored skill, kept for the agent tools that read them
# from these paths. `.vale.ini` turns its styles off for the same two.
LOCAL_SKILL_ROOTS = (".claude/skills", ".agents/skills")


def plugin_dirs():
    """Directories under plugins/ that carry a plugin manifest."""
    if not PLUGINS.is_dir():
        return []
    return [
        path
        for path in sorted(PLUGINS.iterdir())
        if path.is_dir() and (path / ".claude-plugin" / "plugin.json").is_file()
    ]


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


def misplaced_skills():
    """SKILL.md files that sit where no plugin loads them.

    A plugin loads `<plugin>/skills/<name>/SKILL.md` and nothing else, so
    a skill written one directory off is invisible to every other check
    here: it is absent from no list, because no list knows it exists.
    """
    loadable = {
        plugin_dir / "skills" / skill / "SKILL.md"
        for plugin_dir in plugin_dirs()
        for skill in skill_names(plugin_dir)
    }
    local = tuple(ROOT / root for root in LOCAL_SKILL_ROOTS)
    found = []
    for path in sorted(ROOT.rglob("SKILL.md")):
        if ".git" in path.parts or path in loadable:
            continue
        if any(path.is_relative_to(root) for root in local):
            continue
        found.append(
            f"{path.relative_to(ROOT)}: no plugin loads a skill from here - "
            f"move it to plugins/<plugin>/skills/<name>/SKILL.md"
        )
    return found


def main():
    problems = misplaced_skills()

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
                f"directory plugins/{name}/ - add one with source "
                f"./plugins/{name}"
            )
            continue

        category = entry.get("category")
        if category not in CATEGORIES:
            problems.append(
                f".claude-plugin/marketplace.json: plugin {entry['name']!r} "
                f"has category {category!r} - use one of "
                f"{', '.join(CATEGORIES)}"
            )

        readme = plugin_dir / "README.md"
        if not readme.is_file():
            problems.append(
                f"plugins/{name}/README.md: missing - add a README for the plugin"
            )
            continue
        text = readme.read_text()

        if f"](./plugins/{name}/README.md)" not in catalog:
            problems.append(
                f"README.md: no catalog section for plugin {entry['name']!r} - "
                f"add one linking to ./plugins/{name}/README.md"
            )

        for skill in skill_names(plugin_dir):
            if f"](./skills/{skill}/SKILL.md)" not in text:
                problems.append(
                    f"plugins/{name}/README.md: skill {skill} is not listed - "
                    f"add a link to ./skills/{skill}/SKILL.md"
                )
            if f"](./plugins/{name}/skills/{skill}/SKILL.md)" not in catalog:
                problems.append(
                    f"README.md: skill {name}/{skill} is not in the catalog - "
                    f"add a link to ./plugins/{name}/skills/{skill}/SKILL.md"
                )

        for hook in hook_files(plugin_dir):
            if f"hooks/{hook}" not in text:
                problems.append(
                    f"plugins/{name}/README.md: hook {hook} is not listed - "
                    f"add an entry naming hooks/{hook}"
                )

    if problems:
        sys.exit("\n".join(problems))


if __name__ == "__main__":
    main()
