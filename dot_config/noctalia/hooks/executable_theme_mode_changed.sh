#!/usr/bin/env bash
set -euo pipefail

wallpaper_cache="$HOME/.cache/noctalia/wallpaper_path"

[[ -f "$wallpaper_cache" ]] || exit 0

wallpaper=$(<"$wallpaper_cache")

[[ -f "$wallpaper" ]] || exit 0

matugen image "$wallpaper" \
  --mode "$NOCTALIA_THEME_MODE" \
  --source-color-index 0 \
  --type scheme-fruit-salad
