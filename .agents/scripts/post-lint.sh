#!/usr/bin/env bash
# Deterministic checks for Haandol blog posts — no judgment required.
# Usage:
#   .agents/scripts/post-lint.sh                    # all posts and drafts
#   .agents/scripts/post-lint.sh _posts/2026-07-25-foo.md ...
#
# Exits 1 if any check fails. Rules come from AGENTS.md; keep both in sync.

set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  files=(_posts/*.md)
  [ -d _drafts ] && for d in _drafts/*.md; do [ -e "$d" ] && files+=("$d"); done
fi

fail=0
report() { echo "$1: $2"; fail=1; }

for f in "${files[@]}"; do
  [ -e "$f" ] || continue
  case "$f" in *.md) ;; *) continue ;; esac

  # TL;DR: at most 3 bullets
  n=$(awk '/^## TL;DR/{f=1;next} /^## /{f=0} f&&/^- /{c++} END{print c+0}' "$f")
  [ "$n" -gt 3 ] && report "$f" "TL;DR has $n bullets (max 3)"

  # Mermaid blocks must be wrapped in {% raw %} / {% endraw %}
  raw=$(grep -c '^{% raw %}$' "$f")
  endraw=$(grep -c '^{% endraw %}$' "$f")
  mermaid=$(grep -c '^```mermaid$' "$f")
  [ "$raw" != "$endraw" ] && report "$f" "raw/endraw mismatch (raw=$raw endraw=$endraw)"
  [ "$mermaid" -gt "$raw" ] && report "$f" "$mermaid mermaid block(s) but only $raw raw wrapper(s)"

  # Code fences must be balanced
  fences=$(grep -c '^```' "$f")
  [ $((fences % 2)) -ne 0 ] && report "$f" "odd number of code fences ($fences)"

  # Internal post links must end in .html — the slash form 404s
  slash=$(grep -oE '\]\(/20[0-9]{2}/[0-9]{2}/[0-9]{2}/[a-z0-9-]+/\)' "$f" | wc -l | tr -d ' ')
  [ "$slash" -gt 0 ] && report "$f" "$slash internal link(s) use the 404-ing slash form"

  # Footnote refs and definitions must correspond
  refs=$(grep -oE '\[\^[0-9]+\]' "$f" | grep -v ':' | sort -u)
  defs=$(grep -oE '^\[\^[0-9]+\]:' "$f" | sed 's/:$//' | sort -u)
  for r in $refs; do
    echo "$defs" | grep -qxF "$r" || report "$f" "footnote $r referenced but not defined"
  done
  for d in $defs; do
    echo "$refs" | grep -qxF "$d" || report "$f" "footnote $d defined but never referenced"
  done

  # Required front matter
  for key in layout title excerpt author tags; do
    grep -qE "^$key:" "$f" || report "$f" "front matter missing '$key'"
  done

  # Referenced local images must exist
  while IFS= read -r img; do
    [ -n "$img" ] && [ ! -e ".$img" ] && report "$f" "missing image $img"
  done < <(grep -oE '\]\(/assets/[^)]+\)' "$f" | sed 's/^](//; s/)$//')
done

if [ "$fail" -eq 0 ]; then
  echo "post-lint: ${#files[@]} file(s) checked, all clean"
fi
exit "$fail"
