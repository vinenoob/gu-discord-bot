#!/usr/bin/env bash
#
# install-service.sh — run the bot as a systemd service that starts on boot and
# that deploys (the GitHub Actions runner) can restart without a password.
#
# Run with sudo, AFTER dev-setup.sh has created the virtualenv:
#
#     sudo ./install-service.sh
#
# Safe to re-run (idempotent). It writes the systemd unit + a narrow sudoers
# rule, then enables and starts the service.
#
set -euo pipefail

SERVICE_NAME="gu-bot"

# --- Resolve the human user (not root) --------------------------------------
RUN_USER="${SUDO_USER:-$(id -un)}"
if [ "$RUN_USER" = "root" ]; then
  echo "ERROR: run via sudo as your normal user (e.g. 'sudo ./install-service.sh')," >&2
  echo "       not as root directly — the bot should not run as root." >&2
  exit 1
fi
if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: please run with sudo:  sudo ./install-service.sh" >&2
  exit 1
fi

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
SYSTEMCTL="$(command -v systemctl)"

# --- Require the virtualenv from dev-setup ----------------------------------
if [ ! -x "$PYTHON_BIN" ]; then
  echo "ERROR: no virtualenv found at $VENV_DIR." >&2
  echo "       Run dev setup first, as your normal user:  ./dev-setup.sh" >&2
  exit 1
fi

echo ">> Repo directory : $REPO_DIR"
echo ">> Service user   : $RUN_USER"

# --- Warn if the token is missing (service would crash-loop without it) -----
if [ ! -f "$REPO_DIR/key.txt" ] && [ -z "${key:-}" ]; then
  echo
  echo "!! WARNING: no key.txt found. The service will restart-loop until you add it:"
  echo "     echo 'YOUR_DISCORD_BOT_TOKEN' > $REPO_DIR/key.txt"
  echo
fi

# --- systemd service --------------------------------------------------------
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

# --- sudoers rule: let deploys restart the bot without a password -----------
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

# --- Enable + start ---------------------------------------------------------
echo ">> Reloading systemd and starting the service..."
"$SYSTEMCTL" daemon-reload
"$SYSTEMCTL" enable --now "${SERVICE_NAME}.service"

echo
echo ">> Service installed and running. Useful commands:"
echo "     systemctl status ${SERVICE_NAME}"
echo "     journalctl -u ${SERVICE_NAME} -f      # live logs"
echo "     sudo systemctl restart ${SERVICE_NAME}"
