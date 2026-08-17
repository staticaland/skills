#!/usr/bin/env bash
# Deterministic halves of the create-pr skill.
#
# Usage:
#   pr.sh prepare
#     Pushes the branch if the remote lacks its commits, then prints the
#     template to fill: the repo's .github/PULL_REQUEST_TEMPLATE.md if it
#     exists, otherwise this skill's references/pr-template.md. Comments
#     stay in - they carry the writing instructions.
#
#   pr.sh submit <title> <body-file>
#     Strips HTML comments from <body-file>, then creates the PR with the
#     SKILL_CREATE_PR=1 marker the guard hook requires.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

prepare() {
  if ! git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1 \
    || [[ -n "$(git log '@{u}..HEAD' --oneline)" ]]; then
    git push -u origin HEAD
  fi

  local template="$SKILL_DIR/references/pr-template.md"
  local repo_root
  repo_root="$(git rev-parse --show-toplevel)"
  if [[ -f "$repo_root/.github/PULL_REQUEST_TEMPLATE.md" ]]; then
    template="$repo_root/.github/PULL_REQUEST_TEMPLATE.md"
  fi

  echo "TEMPLATE: $template"
  cat "$template"
}

submit() {
  local title="${1:?Usage: pr.sh submit <title> <body-file>}"
  local body_file="${2:?Usage: pr.sh submit <title> <body-file>}"
  if [[ ! -f "$body_file" ]]; then
    echo "Error: no such file: $body_file" >&2
    exit 1
  fi

  local stripped
  stripped="$(mktemp)"
  perl -0pe 's/<!--.*?-->\n?//gs' "$body_file" >"$stripped"

  SKILL_CREATE_PR=1 gh pr create --title "$title" --body-file "$stripped"
}

case "${1:-}" in
  prepare) prepare ;;
  submit)
    shift
    submit "$@"
    ;;
  *)
    echo "Usage: pr.sh {prepare | submit <title> <body-file>}" >&2
    exit 1
    ;;
esac
