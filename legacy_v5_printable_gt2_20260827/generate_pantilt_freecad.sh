#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -x ./squashfs-root/usr/bin/freecadcmd ]]; then
  /home/user/Applications/FreeCAD-1.1.3.AppImage --appimage-extract
fi

output="$(printf 'exec(open("build_pantilt_freecad.py").read())\n' | ./squashfs-root/usr/bin/freecadcmd -c 2>&1)"
printf '%s\n' "$output"

if grep -q 'Traceback (most recent call last)' <<<"$output"; then
  exit 1
fi

grep -q 'VALIDATION_PASSED True' <<<"$output"
