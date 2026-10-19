# language: Python, file: banner.py
# Placeholder ASCII — replace the ART block with the final design dj supplies.

from rich.console import Console
from rich.text import Text

console = Console()

ART = r"""
    ___         __  __         __     ___   ____
   /   |  ___  / /_/ /_  ___  / /    /   | /  _/
  / /| | / _ \/ __/ __ \/ _ \/ /    / /| | / /  
 / ___ |/  __/ /_/ / / /  __/ /    / ___ |_/ /   
/_/  |_|\___/\__/_/ /_/\___/_/    /_/  |_/___/   
"""

SUB = "aethelcli  ·  modules loaded  ·  darkie.dpdns.org"

def show_banner() -> None:
    console.print(Text(ART, style="bold cyan"))
    console.print(Text(SUB, style="dim"))
    console.print()
