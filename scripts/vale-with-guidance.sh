#!/bin/sh

# Wraps vale for the prek hooks: when vale fails, frame the report with a
# pointer to .vale/README.md so fixes start from editorial judgment rather
# than the exit code.

set -u

output=$(vale "$@" 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
  cat <<'EOF'
Vale flagged problems below. Alerts are advice from a style guide, not
orders. Read .vale/README.md before editing, then give each alert a verdict:
rewrite the sentence or suppress with an inline comment. A change that
silences an alert while weakening the prose is a regression.

EOF
  printf '%s\n' "$output"
fi

exit "$status"
