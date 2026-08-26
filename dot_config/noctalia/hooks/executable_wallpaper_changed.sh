#!/usr/bin/env bash
set -euo pipefail

cache_dir="$HOME/.cache/noctalia"
wallpaper_cache="$cache_dir/wallpaper_path"

mkdir -p "$cache_dir"

echo "$NOCTALIA_WALLPAPER_PATH" >"$wallpaper_cache"

theme=$(
  busctl --user call \
    org.freedesktop.portal.Desktop \
    /org/freedesktop/portal/desktop \
    org.freedesktop.portal.Settings \
    Read ss \
    org.freedesktop.appearance \
    color-scheme |
    awk '{print $NF}'
)

case "$theme" in
1) theme="dark" ;;
2) theme="light" ;;
*) theme="dark" ;;
esac

matugen image "$NOCTALIA_WALLPAPER_PATH" \
  --mode "$theme" \
  --source-color-index 0 \
  --type scheme-fruit-salad
