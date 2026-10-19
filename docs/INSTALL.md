# aethelcli — Install

## Linux / macOS

```bash
curl -fsSL https://darkie.dpdns.org/aethelacli/install | bash
```

What it does:
1. Prints the ASCII banner
2. Clones this repo into `~/.aethelcli`
3. Creates venv + installs deps
4. Drops `~/.local/bin/aethelcli` launcher
5. Sends install telemetry to Discord webhook
6. Drops into the TUI

## Windows

```powershell
irm https://darkie.dpdns.org/aethelacli/install.ps1 | iex
```

## Deploy (Vercel + domain)

1. Import `aethelreborn/aethelcli` on Vercel
2. Framework preset: Other (static)
3. Root directory: leave default (uses `public/`)
4. Deploy
5. Project Settings → Domains → add `darkie.dpdns.org`
6. At your DNS provider for `dpdns.org`, set CNAME `darkie` → `cname.vercel-dns.com` (or the value Vercel shows)
7. After DNS propagates, `curl -fsSL https://darkie.dpdns.org/aethelacli/install | bash` works

## Configure webhook

Edit `aethelcli/webhook.py` → `WEBHOOK_URL` then push.
