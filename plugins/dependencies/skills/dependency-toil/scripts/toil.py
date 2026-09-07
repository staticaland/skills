#!/usr/bin/env python3
"""Deterministic halves of the dependency-toil skill.

Usage:
  toil.py measure [--author app/<bot>]... [--org <org>]
    Prints one row per open bot PR - age in days, check states, mergeable
    and review state, and a provisional cause read off those states - then
    the cause counts, the merged median and p90 time-to-merge, the update
    bots the repository has config for, and the merge settings the
    repository API returns to a reader with push access. Without --author, app/renovate and app/dependabot are
    measured when either authored one of the last 100 PRs; a self-hosted
    bot under another login needs --author. --org ranks that owner's
    repositories by open bot PRs.

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


UPDATE_BOTS = {"app/renovate", "app/dependabot"}


def bot_authors() -> list[str]:
    prs = gh("pr", "list", "--state", "all", "--limit", "100", "--json", "author")
    bots = {pr["author"]["login"] for pr in prs if pr["author"].get("is_bot")}
    known = sorted(bots & UPDATE_BOTS)
    if not known and bots:
        sys.exit(
            f"No Renovate or Dependabot PR among the last 100. Bots seen: {', '.join(sorted(bots))}. Pass --author."
        )
    return known


def open_rows(author: str) -> list[tuple]:
    prs = gh(
        "pr", "list", "--state", "open", "--author", author, "--limit", "200",
        "--json", "number,title,createdAt,isDraft,reviewDecision,mergeable,statusCheckRollup",
    )  # fmt: skip
    now = datetime.now(UTC)
    return [
        (
            (now - parse_time(pr["createdAt"])).total_seconds() / 86400,
            pr["number"],
            author,
            ",".join(check_states(pr["statusCheckRollup"])) or "-",
            pr["mergeable"],
            pr["reviewDecision"] or "-",
            cause(pr),
            pr["title"],
        )
        for pr in prs
    ]


def merged_ages(author: str) -> list[float]:
    prs = gh(
        "pr",
        "list",
        "--state",
        "merged",
        "--author",
        author,
        "--limit",
        "100",
        "--json",
        "createdAt,mergedAt",
    )
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
    authors = args.author or bot_authors()
    if not authors:
        sys.exit("No bot among the last 100 PRs. Pass --author app/<bot>.")

    rows = [row for author in authors for row in open_rows(author)]
    print("days\tnumber\tauthor\tchecks\tmergeable\treview\tcause\ttitle")
    for row in sorted(rows, reverse=True):
        print(f"{row[0]:.0f}\t" + "\t".join(str(field) for field in row[1:]))
    print()
    print(
        "open:",
        len(rows),
        json.dumps(dict(Counter(row[6] for row in rows).most_common())),
    )

    ages = sorted(age for author in authors for age in merged_ages(author))
    if ages:
        median = ages[len(ages) // 2]
        p90 = ages[min(int(len(ages) * 0.9), len(ages) - 1)]
        print(f"merged: {len(ages)}  median_days: {median:.1f}  p90_days: {p90:.1f}")
    else:
        print("merged: 0")

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
        hits = gh(
            "search", "prs", "--author", authors[0], "--state", "open", "--owner", args.org,
            "--limit", "1000", "--json", "repository",
        )  # fmt: skip
        counts = Counter(hit["repository"]["nameWithOwner"] for hit in hits)
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
