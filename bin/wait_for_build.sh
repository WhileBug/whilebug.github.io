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
  # Only a build that started after the touch counts: a regeneration whose
  # changed-file list has _pages/about.md on a line of its own (verbose logs also
  # print "Reading: _pages/about.md" in every build), or a full build after a
  # _config.yml restart. A build already running at touch time may miss edits.
  if awk '/\|[[:space:]]+_pages\/about\.md[[:space:]]*$|Generating\.\.\./ { started = 1 } started && /done in/ { found = 1 } END { exit !found }' <<<"$logs"; then
    echo "build finished"
    exit 0
  fi
  sleep 2
done
echo "timed out waiting for the build"
exit 1
