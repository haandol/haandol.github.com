#!/usr/bin/env bash
# PostToolUse hook: lint a blog post right after it is edited.
# Reads the hook JSON payload on stdin and lints only _posts/_drafts markdown.
# Exit 2 tells Claude Code the edit has a problem worth fixing.

set -uo pipefail
cd "$(dirname "$0")/../.." || exit 0

payload=$(cat)
path=$(printf '%s' "$payload" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

[ -n "$path" ] || exit 0
case "$path" in
  *_posts/*.md|*_drafts/*.md) ;;
  *) exit 0 ;;
esac

# Normalize to a repo-relative path so post-lint.sh resolves image paths correctly.
rel=${path#"$PWD"/}

out=$(./.agents/scripts/post-lint.sh "$rel" 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
  printf 'post-lint found issues in %s:\n%s\n' "$rel" "$out" >&2
  exit 2
fi
exit 0
