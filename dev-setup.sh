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
# curl:   needed to install uv.
# ffmpeg: needed by the voice / gTTS features at runtime.
if command -v apt-get >/dev/null 2>&1; then
  echo ">> Installing system packages (curl, ffmpeg)..."
  sudo apt-get update -qq
  sudo apt-get install -y curl ffmpeg
else
  echo ">> Non-Debian system: please ensure curl and ffmpeg are installed."
fi

# --- uv (manages the Python version) ----------------------------------------
# The Python version comes from .python-version, not the OS, so the Pi runs the
# same version as dev machines. uv downloads a prebuilt Python for it.
if ! command -v uv >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/uv" ]; then
  echo ">> Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
UV_BIN="$(command -v uv || echo "$HOME/.local/bin/uv")"
PYTHON_VERSION="$(tr -d '[:space:]' < "$REPO_DIR/.python-version")"

# --- Virtualenv + dependencies ---------------------------------------------
# Recreate the venv if missing, invalid (e.g. a Windows venv copied over has
# Scripts/python.exe instead of bin/python), or on the wrong Python version.
VENV_VERSION=""
if [ -x "$PYTHON_BIN" ]; then
  VENV_VERSION="$("$PYTHON_BIN" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
fi
if [ "$VENV_VERSION" != "$PYTHON_VERSION" ]; then
  echo ">> Creating virtualenv at $VENV_DIR with Python $PYTHON_VERSION ..."
  rm -rf "$VENV_DIR"
  # --seed adds pip, which the deploy workflow uses to update requirements.
  "$UV_BIN" venv --seed --python "$PYTHON_VERSION" "$VENV_DIR"
  VENV_REBUILT=1
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

if [ -n "${VENV_REBUILT:-}" ] && systemctl list-unit-files gu-bot.service >/dev/null 2>&1; then
  echo
  echo "!! The virtualenv was rebuilt. Restart the service to use it:"
  echo "     sudo systemctl restart gu-bot"
fi

echo
echo ">> Dev setup complete. Run the bot manually with:"
echo "     $PYTHON_BIN main.py"
echo "   Or install it as a service that starts on boot:"
echo "     sudo ./install-service.sh"
