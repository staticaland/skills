#!/bin/sh

# Wraps vale for the prek hooks: whenever vale reports alerts, frame the
# report with a pointer to .vale/README.md so fixes start from editorial
# judgment rather than the exit code. Vale exits non-zero only for
# error-level alerts, so the hook in prek.toml sets `verbose = true` to
# surface warnings and suggestions even when the hook passes.

set -u

output=$(vale "$@" 2>&1)
status=$?

# A clean run still prints a "✔ 0 errors" summary; only frame and show the
# report when vale failed or its summary marks alerts with "✖".
if [ "$status" -ne 0 ] || printf '%s' "$output" | grep -q '✖'; then
  cat <<'EOF'
Vale flagged the alerts below. Alerts are advice from a style guide, not
orders. Read .vale/README.md before editing, then give each alert a verdict:
rewrite the sentence or suppress with an inline comment. A change that
silences an alert while weakening the prose is a regression.

EOF
  printf '%s\n' "$output"
fi

exit "$status"
