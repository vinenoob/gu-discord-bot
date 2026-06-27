# Deployment

How this bot runs on the Raspberry Pi and auto-deploys on every push to `master`.

## How it works

```
push to master ──> GitHub ──> (self-hosted runner on the Pi) ──> deploy.yml:
                                                                   git pull
                                                                   pip install (if deps changed)
                                                                   systemctl restart gu-bot
```

The Pi runs a **GitHub Actions self-hosted runner** that holds an *outbound*
connection to GitHub — so there's no port forwarding or inbound access. When you
push to `master`, GitHub sends the job down that connection, and
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) updates the live
clone and restarts the service. Updates land within seconds.

The bot itself runs as a **systemd service** (`gu-bot`) that starts on boot and
restarts on failure.

## Scripts

| Script | Run as | Purpose |
|---|---|---|
| [`dev-setup.sh`](dev-setup.sh) | normal user | System + Python deps and the virtualenv. All a dev machine needs. |
| [`install-service.sh`](install-service.sh) | `sudo` | systemd unit + sudoers restart rule; enables & starts the service. Pi only. |

## Local development

```bash
git clone https://github.com/vinenoob/gu-discord-bot.git
cd gu-discord-bot
./dev-setup.sh
echo 'YOUR_DISCORD_BOT_TOKEN' > key.txt    # or: export key=YOUR_TOKEN
./.venv/bin/python main.py
```

## First-time Pi setup

```bash
# 1. Clone and set up the environment + token
git clone https://github.com/vinenoob/gu-discord-bot.git
cd gu-discord-bot
./dev-setup.sh
echo 'YOUR_DISCORD_BOT_TOKEN' > key.txt

# 2. Run it as a service (starts on boot)
sudo ./install-service.sh

# 3. Register the GitHub Actions runner (enables auto-deploy)
#    Get the URL + token from:
#    repo > Settings > Actions > Runners > New self-hosted runner > Linux
mkdir ~/actions-runner && cd ~/actions-runner
curl -o runner.tar.gz -L <URL_FROM_PAGE>
tar xzf runner.tar.gz
./config.sh --url https://github.com/vinenoob/gu-discord-bot --token <TOKEN_FROM_PAGE>
sudo ./svc.sh install pi      # run the runner as the 'pi' user
sudo ./svc.sh start
```

> If you cloned the bot somewhere other than `/home/pi/gu-discord-bot`, update
> `BOT_DIR` at the top of [`deploy.yml`](.github/workflows/deploy.yml).

After this, every push to `master` auto-deploys. Watch it in the repo's
**Actions** tab.

## Required GitHub settings

Because the repo is public and the runner executes on your home network, lock
these down (**Settings → Actions → General**):

- **Fork pull request workflows from outside collaborators** → *Require approval
  for all outside collaborators*
- **Workflow permissions** → *Read repository contents* (read-only token)

And generally: keep **Collaborators** to just you, and enable **2FA**. The
deploy workflow only triggers `on: push` to `master` and never checks out PR
code, so fork PRs can't run anything on the Pi.

## Common commands

```bash
systemctl status gu-bot              # is it running?
journalctl -u gu-bot -f              # live bot logs
sudo systemctl restart gu-bot        # manual restart
journalctl -u actions.runner.* -f    # runner / deploy logs on the Pi
```

## Troubleshooting

- **Bot won't start** — check `journalctl -u gu-bot -e`. Most often a missing
  `key.txt` or a dependency that didn't install.
- **Push didn't deploy** — confirm the runner is online under *Settings →
  Actions → Runners*, and check the run in the **Actions** tab.
- **`sudo systemctl restart` fails in the deploy** — the sudoers rule in
  `/etc/sudoers.d/gu-bot` is missing; re-run `sudo ./install-service.sh`.
- **`bad interpreter: ^M`** — a script got Windows line endings. The
  [`.gitattributes`](.gitattributes) rule prevents this; re-clone if you hit it.
