#!/bin/sh
# SessionStart hook. Gives a Claude Code cloud session the toolchain this
# repository validates with.
#
# `mise` is absent from the cloud image, and every check runs through
# `mise exec -- prek`, so a session without this script starts with no way to
# validate its own work and spends its first minutes building one.
#
# The script does nothing outside a cloud session, where the contributor's own
# mise is already in place. It always exits 0: a session that starts without a
# toolchain is worth more than a session that fails to start.
#
# https://code.claude.com/docs/en/cloud-environments

set -u

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

# renovate: datasource=github-releases depName=jdx/mise
MISE_VERSION="v2026.8.10"
MISE_PATH=/usr/local/bin/mise

repo="${CLAUDE_PROJECT_DIR:-$(dirname "$(dirname "$0")")}"

installed=""
if [ -x "$MISE_PATH" ]; then
  installed="v$("$MISE_PATH" --version 2>/dev/null | head -1 | cut -d' ' -f1)"
fi

# The hook runs on every start and every resume, and reaching the installer
# costs ten seconds even when it decides to skip the download. Compare the
# version here instead, and leave the network alone on a resumed session.
#
# /usr/local/bin is on the default PATH of the cloud image, so mise lands where
# every later shell finds it without a profile edit.
if [ "$installed" != "$MISE_VERSION" ]; then
  if ! curl -fsSL https://mise.run |
    MISE_VERSION="$MISE_VERSION" \
      MISE_INSTALL_PATH="$MISE_PATH" \
      MISE_QUIET=1 sh >/dev/null 2>&1; then
    echo "session-setup: mise did not install. Install it by hand with:"
    echo "  curl -fsSL https://mise.run | sh"
    exit 0
  fi
fi

"$MISE_PATH" trust "$repo/mise.toml" >/dev/null 2>&1
if ! "$MISE_PATH" -C "$repo" install --locked >/dev/null 2>&1; then
  echo "session-setup: mise is installed, and the locked tools are not."
  echo "Retry with: mise install --locked"
  exit 0
fi

echo "Toolchain ready. Validate with: mise exec -- prek run --all-files"

# zizmor audits action references against the GitHub API. Where the sandbox
# proxy answers 401, the hook fails on files the session never touched, and the
# exit code of a whole prek run stops carrying a signal. Measure that rather
# than assume it, so the note appears only where it is true.
if ! "$MISE_PATH" -C "$repo" exec -- zizmor --no-progress \
  "$repo/.github/workflows/prek.yml" >/dev/null 2>&1; then
  echo "zizmor cannot reach the GitHub API here, so its hook fails on every run."
  echo "For a run whose exit code reflects your own change:"
  echo "  ZIZMOR_OFFLINE=true mise exec -- prek run --all-files"
  echo "That keeps the offline audits. CI runs the online ones on the pull request."
fi

exit 0
