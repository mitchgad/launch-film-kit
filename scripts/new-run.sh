#!/usr/bin/env bash
# Make a run folder for a new film: $RUNS/<name>-NN (default ~/runs) with brand/ set up from the template, and
# optionally sfx/ copied from a sound library folder.
#
#   scripts/new-run.sh acme                    -> ~/runs/acme-01
#   scripts/new-run.sh acme ~/Sounds/favs      -> ~/runs/acme-02, with ~/Sounds/favs copied in as sfx/
set -euo pipefail

name=${1:?usage: new-run.sh <name> [sound-library-folder]}
library=${2:-}
root=${RUNS:-$HOME/runs}
kit=$(cd "$(dirname "$0")/.." && pwd)

n=1
while [ -e "$root/$name-$(printf %02d "$n")" ]; do n=$((n + 1)); done
dir="$root/$name-$(printf %02d "$n")"

mkdir -p "$dir/brand/site" "$dir/brand/assets" "$dir/brand/logo" "$dir/brand/fonts"
sed "s/^# BRAND:/# $name:/" "$kit/templates/brand-kit.md" > "$dir/brand/README.md"
if [ -n "$library" ]; then
  cp -R "$library" "$dir/sfx"
fi

echo "$dir"
echo
echo "Next:"
echo "  1. Fill in $dir/brand (see its README.md)."
echo "  2. Start the build session:  cd $dir && claude --safe-mode --effort max --permission-mode auto"
echo "  3. Paste the prompt from $kit/prompts/launch-film.md"
