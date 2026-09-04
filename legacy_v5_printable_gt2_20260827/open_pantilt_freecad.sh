#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ -x /home/user/Applications/FreeCAD-1.1.3.AppImage ]]; then
  exec /home/user/Applications/FreeCAD-1.1.3.AppImage open_pantilt_visible_freecad.py
fi

if [[ -x /home/user/Applications/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage ]]; then
  exec /home/user/Applications/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage open_pantilt_visible_freecad.py
fi

echo "FreeCAD AppImage not found in /home/user/Applications" >&2
exit 1
