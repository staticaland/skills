#!/bin/sh

set -eu

if [ "$#" -ne 1 ]; then
  echo "usage: $0 COMMIT_EDITMSG" >&2
  exit 2
fi

repo_root=$(git rev-parse --show-toplevel)
message_dir=$(mktemp -d "$repo_root/vale-commit-message.XXXXXX")
message_copy="$message_dir/COMMIT_EDITMSG"
trap 'rm -f "$message_copy"; rmdir "$message_dir"' EXIT HUP INT TERM

cp "$1" "$message_copy"
vale "$message_copy"
