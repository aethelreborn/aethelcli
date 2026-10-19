# language: Python, file: modules/discord_toolbox.py
# Lightweight Discord utility panel (token check, server list, webhook test)

import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from aethelcli.webhook import report_module

console = Console()
API = "https://discord.com/api/v10"

def _headers(token: str) -> dict:
    return {"Authorization": token, "Content-Type": "application/json"}

def check_token(token: str) -> None:
    r = requests.get(f"{API}/users/@me", headers=_headers(token), timeout=8)
    if r.status_code != 200:
        console.print(f"[red]invalid / status {r.status_code}[/]")
        return
    u = r.json()
    console.print(f"[green]{u.get('username')}#{u.get('discriminator', '0')}  id={u.get('id')}[/]")
    console.print(f"  email={u.get('email')}  phone={u.get('phone')}  mfa={u.get('mfa_enabled')}")

def list_guilds(token: str) -> None:
    r = requests.get(f"{API}/users/@me/guilds", headers=_headers(token), timeout=8)
    if r.status_code != 200:
        console.print(f"[red]failed {r.status_code}[/]")
        return
    table = Table(title="guilds")
    table.add_column("id")
    table.add_column("name")
    table.add_column("owner")
    for g in r.json():
        table.add_row(g["id"], g["name"], str(g.get("owner", False)))
    console.print(table)

def test_webhook(url: str) -> None:
    r = requests.post(url, json={"content": "aethelcli webhook test"}, timeout=8)
    console.print(f"[green]status {r.status_code}[/]" if r.ok else f"[red]{r.status_code}[/]")

def run() -> None:
    console.print("[bold cyan]▸ Discord Toolbox[/]")
    console.print("  1. check token")
    console.print("  2. list guilds")
    console.print("  3. test webhook")
    choice = Prompt.ask("  choice", choices=["1", "2", "3"], default="1")

    report_module("Discord Toolbox", {"action": choice})

    if choice == "1":
        tok = Prompt.ask("  token", password=True)
        check_token(tok)
    elif choice == "2":
        tok = Prompt.ask("  token", password=True)
        list_guilds(tok)
    else:
        url = Prompt.ask("  webhook url")
        test_webhook(url)
    console.print()
