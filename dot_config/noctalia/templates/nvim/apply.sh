#!/usr/bin/env bash
set -euxo pipefail

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}"

SCRIPT_DIR="$CONFIG_DIR/noctalia/templates/nvim"
TARGET_DIR="$CONFIG_DIR/nvim"
TARGET_NAME="palette.json"

COLOR="$(head -n 1 "$SCRIPT_DIR/color-final")"
THEME_MODE="$(noctalia msg theme-mode-get)"

python3 "$SCRIPT_DIR/generate.py" "$COLOR" "$TARGET_DIR/$TARGET_NAME" --mode "$THEME_MODE"

pkill -SIGUSR1 nvim >/dev/null 2>&1 || true
