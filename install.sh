#!/bin/bash
# Install the skills for Claude Code.
#   ./install.sh user    → ~/.claude/skills   (every project on this machine)
#   ./install.sh local   → ./.claude/skills   (this repo only)
set -e
here="$(cd "$(dirname "$0")" && pwd)"
case "${1:-user}" in
  user)  dest="$HOME/.claude/skills" ;;
  local) dest="$PWD/.claude/skills" ;;
  *) echo "usage: $0 [user|local]"; exit 1 ;;
esac
mkdir -p "$dest"
for s in "$here"/skills/*/; do
  name="$(basename "$s")"
  rm -rf "$dest/$name"
  cp -R "$s" "$dest/$name"
  echo "  · $name → $dest/$name"
done
if [ -f "$dest/mma-animation/scripts/package.json" ] && command -v npm >/dev/null; then
  (cd "$dest/mma-animation/scripts" && npm install --silent) && echo "  · mma-animation: npm install done"
fi
echo "Start a new Claude Code session so the skills are picked up."
