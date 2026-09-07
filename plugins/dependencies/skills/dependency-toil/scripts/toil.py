#!/usr/bin/env python3
"""Deterministic halves of the dependency-toil skill.

Usage:
  toil.py measure [--author <login>]... [--org <org>]
    Prints one row per open update PR - age in days, the Dependabot
    ecosystem read off the branch name, check states, mergeable and review
    state, and a provisional cause read off those states - then the cause
    counts, the merged median and p90 time-to-merge, the authors behind the
    update PRs, the update bots the repository has config for, and the
    merge settings the repository API returns to a reader with push access.

    An update PR is one with any of: a renovate/ or dependabot/ branch, a
    dependencies, renovate, or dependabot label, or an update-shaped title
    (chore(deps), Update, Bump, Pin, Lock file maintenance, digest). No
    login is assumed, and a bot author alone is not a signal, because
    release and assistant bots open PRs too; those logins are listed at
    the end so --author can add one the signals miss. --org ranks that
    owner's repositories by the open PRs of the bot authors found and of
    every --author login.

  toil.py verify <pr-number>
    Prints the PR's auto-merge request, check states, merge time and
    actor, the `Automerge:` line Renovate writes into the body, and the
    workflow runs on the merge commit.

Provisional causes:
  toil             checks green, mergeable, no review outstanding
  draft            the bot opened it as a draft
  conflicting      the base moved and the branch has not been rebased
  red-check        a check failed, errored, timed out, or was cancelled
  pending-check    a check has not reported
  no-checks        nothing ran on the branch at all
  review-required  branch protection wants an approval
  changes-requested a reviewer asked for changes

Needs `gh` authenticated for the repository in the working directory.
Exits 2 when `gh` fails, 1 when nothing could be measured.
"""

import argparse
import json
import math
import re
import statistics
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime

GREEN = {"SUCCESS", "NEUTRAL", "SKIPPED"}
RED = {
    "FAILURE",
    "ERROR",
    "TIMED_OUT",
    "CANCELLED",
    "ACTION_REQUIRED",
    "STARTUP_FAILURE",
}

BOT_CONFIGS = {
    "renovate": [
        "renovate.json",
        "renovate.json5",
        ".renovaterc",
        ".renovaterc.json",
        ".renovaterc.json5",
        ".github/renovate.json",
        ".github/renovate.json5",
    ],
    "dependabot": [".github/dependabot.yml", ".github/dependabot.yaml"],
}


def gh(*args: str):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        sys.exit(2)
    return json.loads(result.stdout) if result.stdout.strip() else None


def parse_time(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def check_states(rollup: list[dict] | None) -> list[str]:
    states = set()
    for check in rollup or []:
        states.add(
            check.get("conclusion")
            or check.get("state")
            or check.get("status")
            or "PENDING"
        )
    return sorted(states)


def cause(pr: dict) -> str:
    states = set(check_states(pr["statusCheckRollup"]))
    if pr["isDraft"]:
        return "draft"
    if pr["mergeable"] == "CONFLICTING":
        return "conflicting"
    if not states:
        return "no-checks"
    if states & RED:
        return "red-check"
    if states - GREEN:
        return "pending-check"
    if pr["reviewDecision"] == "REVIEW_REQUIRED":
        return "review-required"
    if pr["reviewDecision"] == "CHANGES_REQUESTED":
        return "changes-requested"
    return "toil"


BRANCH_PREFIXES = ("renovate/", "dependabot/")
TITLE_PATTERN = re.compile(
    r"^(chore|fix|build|ci)\(deps(-dev)?\)|^(Update|Pin|Bump|Upgrade) |Lock file maintenance|digest to [0-9a-f]{7}",
    re.IGNORECASE,
)
PR_FIELDS = "number,title,createdAt,mergedAt,isDraft,reviewDecision,mergeable,statusCheckRollup,headRefName,author,labels"


LABELS = {"dependencies", "renovate", "dependabot"}


def is_update_pr(pr: dict, extra_authors: set[str]) -> bool:
    """Any one signal marks an update PR: a bot branch prefix, an update label, an update-shaped title, a named author."""
    return (
        pr["author"].get("login") in extra_authors
        or pr["headRefName"].startswith(BRANCH_PREFIXES)
        or any(label["name"].lower() in LABELS for label in pr["labels"])
        or bool(TITLE_PATTERN.search(pr["title"]))
    )


def update_prs(
    state: str, limit: int, extra_authors: set[str]
) -> tuple[list[dict], Counter]:
    """Return the update PRs and, for the note at the end, bot authors whose PRs matched no signal."""
    prs = gh("pr", "list", "--state", state, "--limit", str(limit), "--json", PR_FIELDS)
    matched = [pr for pr in prs if is_update_pr(pr, extra_authors)]
    unmatched_bots = Counter(
        pr["author"]["login"]
        for pr in prs
        if pr["author"].get("is_bot") and pr not in matched
    )
    return matched, unmatched_bots


def ecosystem(branch: str) -> str:
    """Dependabot encodes the ecosystem in the branch: dependabot/<ecosystem>/<dir>/<dep>-<version>."""
    parts = branch.split("/")
    return parts[1] if parts[0] == "dependabot" and len(parts) > 2 else "-"


def open_rows(prs: list[dict]) -> list[tuple]:
    now = datetime.now(UTC)
    return [
        (
            (now - parse_time(pr["createdAt"])).total_seconds() / 86400,
            pr["number"],
            pr["author"]["login"],
            ecosystem(pr["headRefName"]),
            ",".join(check_states(pr["statusCheckRollup"])) or "-",
            pr["mergeable"],
            pr["reviewDecision"] or "-",
            cause(pr),
            pr["title"],
        )
        for pr in prs
    ]


def merged_ages(prs: list[dict]) -> list[float]:
    return [
        (parse_time(pr["mergedAt"]) - parse_time(pr["createdAt"])).total_seconds()
        / 86400
        for pr in prs
    ]


def tracked_bots() -> list[str]:
    top = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    files = set(
        subprocess.run(
            ["git", "-C", top, "ls-files"], check=True, capture_output=True, text=True
        ).stdout.split()
    )
    return [bot for bot, paths in BOT_CONFIGS.items() if files & set(paths)]


def measure(args: argparse.Namespace) -> None:
    extra = set(args.author or [])
    open_prs, open_bots = update_prs("open", 500, extra)
    merged_prs, merged_bots = update_prs("merged", 300, extra)
    if not open_prs and not merged_prs:
        sys.exit(
            "No update PR found: no renovate/ or dependabot/ branch, update label, or update-shaped title. Pass --author <login>."
        )

    rows = open_rows(open_prs)
    print("days\tnumber\tauthor\tecosystem\tchecks\tmergeable\treview\tcause\ttitle")
    for row in sorted(rows, reverse=True):
        print(f"{row[0]:.0f}\t" + "\t".join(str(field) for field in row[1:]))
    print()
    print(
        "open:",
        len(rows),
        json.dumps(dict(Counter(row[7] for row in rows).most_common())),
    )

    ages = sorted(merged_ages(merged_prs))
    if ages:
        median = statistics.median(ages)
        p90 = ages[math.ceil(0.9 * len(ages)) - 1]
        print(
            f"merged: {len(ages)} of the last 300 merged PRs  median_days: {median:.1f}  p90_days: {p90:.1f}"
        )
    else:
        print("merged: 0")

    authors = Counter(pr["author"]["login"] for pr in open_prs + merged_prs)
    print(
        "update authors:",
        ", ".join(f"{login} ({n})" for login, n in authors.most_common()),
    )
    other_bots = open_bots + merged_bots
    if other_bots:
        print(
            "other bot authors, not counted:",
            ", ".join(f"{login} ({n})" for login, n in other_bots.most_common()),
        )
    print("bot config:", ", ".join(tracked_bots()) or "none tracked")

    repo = gh("api", "repos/{owner}/{repo}")
    methods = [
        name
        for name, key in (
            ("squash", "allow_squash_merge"),
            ("merge", "allow_merge_commit"),
            ("rebase", "allow_rebase_merge"),
        )
        if repo.get(key)
    ]
    auto = repo.get("allow_auto_merge")
    print(
        "auto-merge allowed:",
        "unreadable without push access" if auto is None else ("yes" if auto else "NO"),
    )
    print("merge methods allowed:", ", ".join(methods) or "unreadable")
    print(
        "delete branch on merge:", "yes" if repo.get("delete_branch_on_merge") else "no"
    )

    if args.org:
        counts: Counter = Counter()
        for login in sorted(
            {login for login in authors if login.startswith("app/")} | extra
        ):
            hits = gh(
                "search",
                "prs",
                "--author",
                login,
                "--state",
                "open",
                "--owner",
                args.org,
                "--limit",
                "1000",
                "--json",
                "repository",
            )
            counts.update(hit["repository"]["nameWithOwner"] for hit in hits)
        print()
        print("repository\topen")
        for repo_name, count in counts.most_common():
            print(f"{repo_name}\t{count}")


def verify(args: argparse.Namespace) -> None:
    pr = gh(
        "pr", "view", str(args.number), "--json",
        "title,body,autoMergeRequest,statusCheckRollup,mergedAt,mergedBy,mergeCommit",
    )  # fmt: skip
    print("title:", pr["title"])
    print("auto-merge request:", json.dumps(pr["autoMergeRequest"]))
    print("checks:", ",".join(check_states(pr["statusCheckRollup"])) or "-")
    for line in pr["body"].splitlines():
        if "Automerge" in line and ":" in line:
            print("renovate body:", line.strip())
    merged_by = (pr["mergedBy"] or {}).get("login")
    print(
        "merged:",
        pr["mergedAt"] or "not merged",
        f"by {merged_by}" if merged_by else "",
    )
    if pr["mergeCommit"]:
        runs = gh(
            "run",
            "list",
            "--commit",
            pr["mergeCommit"]["oid"],
            "--json",
            "name,event,status,conclusion",
        )
        print("runs on merge commit:")
        for run in runs:
            print(
                f"  {run['name']}\t{run['event']}\t{run['conclusion'] or run['status']}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)

    m = commands.add_parser(
        "measure", help="age every open bot PR and read the merge settings"
    )
    m.add_argument(
        "--author",
        action="append",
        help="bot login as gh spells it, e.g. app/renovate; repeatable",
    )
    m.add_argument("--org", help="also rank this owner's repositories by open bot PRs")
    m.set_defaults(run=measure)

    v = commands.add_parser("verify", help="show the automerge evidence on one PR")
    v.add_argument("number", type=int)
    v.set_defaults(run=verify)

    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
