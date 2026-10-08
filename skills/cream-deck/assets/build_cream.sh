#!/bin/bash
# Render the cream (workshop-style) diagrams: inline the felt icons, then Chrome at 2×.
#   ./build_cream.sh            all c*.svg produced by make_cream.py
#   ./build_cream.sh c4 c9      some
# Run from the folder that holds make_cream.py and svgkit_cream.py. PNGs land in ../ (the deck's img/).
# ICONS: the felt icon set — defaults to this skill's assets/icons; override with ICONS=/path.
set -e
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ICONS="${ICONS:-$HOME/.claude/skills/cream-deck/assets/icons}"
python3 make_cream.py >/dev/null
for src in c*.svg; do
  name="${src%.svg}"
  if [ $# -gt 0 ]; then hit=0; for a in "$@"; do case "$name" in "$a"*) hit=1;; esac; done; [ $hit = 1 ] || continue; fi
  python3 - "$src" "$ICONS" <<'PY'
import base64, pathlib, re, sys
src, icons = sys.argv[1], pathlib.Path(sys.argv[2])
s = pathlib.Path(src).read_text()
s = re.sub(r"@@ICON:([a-z]+)@@", lambda m: "data:image/png;base64," + base64.b64encode((icons / f"icon-{m.group(1)}.png").read_bytes()).decode(), s)
pathlib.Path(".build.svg").write_text(s)
PY
  "$CHROME" --headless=new --disable-gpu --force-device-scale-factor=2 --window-size=1600,900 \
    --hide-scrollbars --screenshot="../$name.png" ".build.svg" >/dev/null 2>&1
  echo "  · $name.png"
done
rm -f .build.svg
