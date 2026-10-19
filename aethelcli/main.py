# language: Python, file: main.py
# aethelcli entry — TUI menu + optional GUI flag

import argparse
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from aethelcli.banner import show_banner
from aethelcli.webhook import report_module
from aethelcli.modules import MODULES

console = Console()

def tui() -> None:
    show_banner()

    table = Table(show_header=True, header_style="bold magenta", box=None, padding=(0, 2))
    table.add_column("#", style="cyan", width=4)
    table.add_column("Module", style="white")
    for key, name, _ in MODULES:
        table.add_row(key, name)
    table.add_row("0", "Exit")
    table.add_row("g", "Launch GUI")

    console.print(Panel(table, title="[bold]module list[/]", border_style="cyan"))
    console.print()

    while True:
        choice = Prompt.ask("[bold cyan]select[/]", default="0").strip().lower()
        if choice in ("0", "q", "exit"):
            console.print("[dim]bye[/]")
            break
        if choice == "g":
            from aethelcli.gui import launch_gui
            launch_gui()
            continue

        matched = next((m for m in MODULES if m[0] == choice), None)
        if not matched:
            console.print("[red]invalid[/]")
            continue

        key, name, runner = matched
        report_module(name, {"ui": "tui"})
        try:
            runner()
        except KeyboardInterrupt:
            console.print("\n[yellow]aborted[/]")
        except Exception as e:
            console.print(f"[red]error: {e}[/]")

def main() -> None:
    parser = argparse.ArgumentParser(prog="aethelcli")
    parser.add_argument("--gui", action="store_true", help="launch GUI directly")
    args = parser.parse_args()

    if args.gui:
        from aethelcli.gui import launch_gui
        launch_gui()
    else:
        tui()

if __name__ == "__main__":
    main()
