#!/usr/bin/env bash
#
# install.sh — set up the GU Discord Bot as a systemd service on Linux (Raspberry Pi).
#
# Run from the repo root, as your normal user, with sudo:
#
#     sudo ./install.sh
#
# It is safe to re-run (idempotent). It will:
#   1. install system packages the bot needs (python venv, ffmpeg)
#   2. create a Python virtualenv and install requirements.txt
#   3. write a systemd service that runs the bot and restarts it on failure
#   4. add a narrow sudoers rule so deploys can restart the bot without a password
#   5. enable + start the service
#
set -euo pipefail

SERVICE_NAME="gu-bot"

# --- Resolve the human user (not root) and the repo directory ---------------
RUN_USER="${SUDO_USER:-$(id -un)}"
if [ "$RUN_USER" = "root" ]; then
  echo "ERROR: run this as your normal user via sudo (e.g. 'sudo ./install.sh')," >&2
  echo "       not as root directly — the bot should not run as root." >&2
  exit 1
fi

# This script lives in the repo root; resolve that path absolutely.
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"
SYSTEMCTL="$(command -v systemctl)"

# --- Must be root to write the service + sudoers files ----------------------
if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: please run with sudo:  sudo ./install.sh" >&2
  exit 1
fi

echo ">> Repo directory : $REPO_DIR"
echo ">> Service user   : $RUN_USER"
echo

# --- 1. System packages -----------------------------------------------------
if command -v apt-get >/dev/null 2>&1; then
  echo ">> Ensuring system packages (python3-venv, ffmpeg)..."
  apt-get update -qq
  apt-get install -y python3-venv ffmpeg
else
  echo ">> Skipping apt (not Debian/Raspberry Pi OS). Make sure python3-venv and"
  echo "   ffmpeg are installed for voice features to work."
fi

# --- 2. Virtualenv + dependencies (as the run user, so files aren't root) ---
# Recreate the venv if it's missing or not a valid Linux venv (e.g. a venv
# copied over from Windows has Scripts/python.exe instead of bin/python).
if [ ! -x "$PYTHON_BIN" ]; then
  echo ">> Creating fresh virtualenv at $VENV_DIR ..."
  rm -rf "$VENV_DIR"
  sudo -u "$RUN_USER" python3 -m venv "$VENV_DIR"
fi
echo ">> Installing requirements..."
sudo -u "$RUN_USER" "$PIP_BIN" install --upgrade pip
sudo -u "$RUN_USER" "$PIP_BIN" install -r "$REPO_DIR/requirements.txt"

# --- Warn if the bot token is missing ---------------------------------------
if [ ! -f "$REPO_DIR/key.txt" ] && [ -z "${key:-}" ]; then
  echo
  echo "!! WARNING: no key.txt found and \$key is not set."
  echo "   The bot will fail to log in. Create the token file with:"
  echo "       echo 'YOUR_DISCORD_BOT_TOKEN' > $REPO_DIR/key.txt"
  echo
fi

# --- 3. systemd service -----------------------------------------------------
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
echo ">> Writing $SERVICE_FILE"
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=GU Discord Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$RUN_USER
WorkingDirectory=$REPO_DIR
ExecStart=$PYTHON_BIN main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# --- 4. sudoers rule: let deploys restart the bot without a password --------
SUDOERS_FILE="/etc/sudoers.d/${SERVICE_NAME}"
echo ">> Writing $SUDOERS_FILE"
cat > "$SUDOERS_FILE" <<EOF
$RUN_USER ALL=(root) NOPASSWD: $SYSTEMCTL restart ${SERVICE_NAME}.service
EOF
chmod 0440 "$SUDOERS_FILE"
# Validate syntax before trusting it; remove it if invalid so sudo isn't broken.
if ! visudo -cf "$SUDOERS_FILE" >/dev/null; then
  echo "ERROR: generated sudoers file is invalid, removing it." >&2
  rm -f "$SUDOERS_FILE"
  exit 1
fi

# --- 5. Enable + start ------------------------------------------------------
echo ">> Reloading systemd and starting the service..."
"$SYSTEMCTL" daemon-reload
"$SYSTEMCTL" enable --now "${SERVICE_NAME}.service"

echo
echo ">> Done! The bot is now running and will start on boot."
echo "   Useful commands:"
echo "     systemctl status ${SERVICE_NAME}"
echo "     journalctl -u ${SERVICE_NAME} -f      # live logs"
echo "     sudo systemctl restart ${SERVICE_NAME}"
