#!/bin/bash
# Install the skills into a coding agent's skills directory.
#   ./install.sh user      → ~/.agents/skills      (every project on this machine)
#   ./install.sh local     → ./.agents/skills      (this repo only)
#   ./install.sh <dir>     → any other skills directory your agent reads
#                            (e.g. ~/.gemini/skills, ~/.gemini/config/skills)
# Or set SKILLS_DIR=<dir> and run with no argument.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
case "${1:-${SKILLS_DIR:-user}}" in
  user)  dest="$HOME/.agents/skills" ;;
  local) dest="$PWD/.agents/skills" ;;
  -h|--help) echo "usage: $0 [user|local|<dir>]"; exit 0 ;;
  *) dest="$1" ;;
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
echo "Start a new agent session (or reload its skills) so the skills are picked up."
