#!/usr/bin/env bash
# Screenshot the main pages in light and dark mode, at desktop (1400px) and phone (390px) width.
# Usage: bin/shoot_pages.sh <out-dir> [base-url]   (default base-url: http://localhost:8080)
set -euo pipefail

mkdir -p "${1:?usage: bin/shoot_pages.sh <out-dir> [base-url]}"
out="$(cd "$1" && pwd)"
base="${2:-http://localhost:8080}"
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
pages="home:/ publications:/publications/ research:/research/ news:/news/ blog:/blog/ cv:/cv/ 404:/404.html"

# shoot <color-scheme> <window-width> <png> <url>
# A pending network request can freeze Chrome's virtual clock, so each shot is killed after 60s.
shoot() {
  perl -e 'alarm shift; exec @ARGV' 60 "$chrome" --headless=new --disable-gpu --hide-scrollbars \
    --blink-settings=preferredColorScheme="$1" --timeout=20000 --virtual-time-budget=8000 \
    --window-size="$2",2400 --screenshot="$3" "$4" 2>/dev/null || echo "warning: no screenshot for $4 ($3)"
}

for entry in $pages; do
  name="${entry%%:*}"
  path="${entry#*:}"
  # Headless Chrome cannot render narrower than 500px, so phones use a 390px iframe.
  printf '<!doctype html><body style="margin:0"><iframe src="%s%s" width="390" height="2400" style="border:0"></iframe>' \
    "$base" "$path" >"$out/$name-phone.html"
  for mode in light dark; do
    scheme=1
    [ "$mode" = dark ] && scheme=0
    shoot "$scheme" 1400 "$out/$name-desktop-$mode.png" "$base$path"
    shoot "$scheme" 500 "$out/$name-phone-$mode.png" "file://$out/$name-phone.html"
  done
done
echo "screenshots in $out"
