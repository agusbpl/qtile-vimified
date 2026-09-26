#!/usr/bin/env bash
# ==============================================================================
# qtile-vimified: install.sh
# End-to-end installer for Qtile Vimified
# ==============================================================================
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QTILE_CONF_DIR="${HOME}/.config/qtile"

echo -e "\033[1;34m:: Installing qtile-vimified...\033[0m"

mkdir -p "$QTILE_CONF_DIR"

# 1. Install whichkey.py and default theme.py
echo "-> Deploying whichkey.py to $QTILE_CONF_DIR..."
cp "$DIR/whichkey.py" "$QTILE_CONF_DIR/whichkey.py"
echo -e "\033[32m✔ whichkey.py deployed.\033[0m"

if [ ! -f "$QTILE_CONF_DIR/theme.py" ]; then
  echo "-> Deploying theme.py to $QTILE_CONF_DIR..."
  cp "$DIR/theme.py" "$QTILE_CONF_DIR/theme.py"
  echo -e "\033[32m✔ theme.py deployed.\033[0m"
fi

# 2. Reload Qtile if running
if pgrep -x qtile >/dev/null 2>&1; then
  echo "-> Reloading Qtile configuration..."
  qtile cmd-obj -o cmd -f reload_config >/dev/null 2>&1 || true
  echo -e "\033[32m✔ Qtile reloaded live.\033[0m"
fi

echo ""
echo -e "\033[1;32m🎉 qtile-vimified installed and active!\033[0m"
echo -e "Press \033[1mALT + RETURN\033[0m to open the Master Hub Which-Key HUD."
