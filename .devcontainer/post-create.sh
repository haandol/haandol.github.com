#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

bundler_version="$(awk '/^BUNDLED WITH$/ { getline; print $1; exit }' Gemfile.lock)"
if [[ -z "$bundler_version" ]]; then
  echo "Gemfile.lock must specify a Bundler version under BUNDLED WITH." >&2
  exit 1
fi

if ! gem list --installed bundler --version "$bundler_version" >/dev/null; then
  gem install bundler --version "$bundler_version" --no-document
fi

BUNDLE_FROZEN=true bundle "_${bundler_version}_" install
