#!/usr/bin/env bash
#
# dev-setup.sh — prepare a working environment to run/develop the bot.
#
# Run as your normal user (NOT root):
#
#     ./dev-setup.sh
#
# Installs system + Python dependencies and creates the virtualenv so you can
# run the bot directly with:  ./.venv/bin/python main.py
#
# This is all you need on a dev machine. To run the bot as a background service
# that starts on boot (e.g. on the Raspberry Pi), run ./install-service.sh after.
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"

if [ "$(id -u)" -eq 0 ]; then
  echo "ERROR: run dev-setup.sh as your normal user, not root (the venv should be" >&2
  echo "       owned by you). It uses sudo only for installing system packages." >&2
  exit 1
fi

# --- System packages --------------------------------------------------------
# python3-venv: needed to create the virtualenv.
# ffmpeg:       needed by the voice / gTTS features at runtime.
if command -v apt-get >/dev/null 2>&1; then
  echo ">> Installing system packages (python3-venv, ffmpeg)..."
  sudo apt-get update -qq
  sudo apt-get install -y python3-venv ffmpeg
else
  echo ">> Non-Debian system: please ensure python3-venv and ffmpeg are installed."
fi

# --- Virtualenv + dependencies ---------------------------------------------
# Recreate the venv if missing or invalid (e.g. a Windows venv copied over has
# Scripts/python.exe instead of bin/python).
if [ ! -x "$PYTHON_BIN" ]; then
  echo ">> Creating virtualenv at $VENV_DIR ..."
  rm -rf "$VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi
echo ">> Installing requirements..."
"$PIP_BIN" install --upgrade pip
"$PIP_BIN" install -r "$REPO_DIR/requirements.txt"

# --- Token reminder ---------------------------------------------------------
if [ ! -f "$REPO_DIR/key.txt" ] && [ -z "${key:-}" ]; then
  echo
  echo "!! Next: add your bot token so it can log in:"
  echo "     echo 'YOUR_DISCORD_BOT_TOKEN' > $REPO_DIR/key.txt"
fi

echo
echo ">> Dev setup complete. Run the bot manually with:"
echo "     $PYTHON_BIN main.py"
echo "   Or install it as a service that starts on boot:"
echo "     sudo ./install-service.sh"
