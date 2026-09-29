#!/usr/bin/env bash
# Trigger a rebuild of the running jekyll container and wait until it finishes.
# Exits 1 (and prints the log lines) if Jekyll reports a Liquid/Sass error.
set -euo pipefail

since=$(date -u +%Y-%m-%dT%H:%M:%SZ)
touch _pages/about.md
for _ in $(seq 1 150); do
  logs=$(docker compose logs --no-color --since "$since" jekyll 2>&1 || true)
  if grep -qE "Liquid (Exception|Warning)|Conversion error|[^_]Error:" <<<"$logs"; then
    echo "BUILD ERROR:"
    grep -E "Liquid (Exception|Warning)|Conversion error|[^_]Error:" <<<"$logs" | head -20
    exit 1
  fi
  if grep -q "done in" <<<"$logs"; then
    echo "build finished"
    exit 0
  fi
  sleep 2
done
echo "timed out waiting for the build"
exit 1
