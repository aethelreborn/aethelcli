# language: Python, file: webhook.py
# Discord webhook telemetry — install + module events

import platform
import socket
import uuid
import getpass
import json
import time
from datetime import datetime, timezone
from typing import Any

import requests
import psutil

# ── replace with your webhook URL ──────────────────────────────────────────
WEBHOOK_URL = "https://discord.com/api/webhooks/CHANGE_ME/CHANGE_ME"
# ───────────────────────────────────────────────────────────────────────────

def _base_info() -> dict[str, Any]:
    try:
        ip = requests.get("https://api.ipify.org", timeout=4).text
    except Exception:
        ip = "unknown"
    return {
        "hostname": socket.gethostname(),
        "user": getpass.getuser(),
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "python": platform.python_version(),
        "ip": ip,
        "mac": ":".join(["{:02x}".format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)][::-1]),
        "cpu": platform.processor() or "n/a",
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 1),
        "ts": datetime.now(timezone.utc).isoformat(),
    }

def _post(payload: dict) -> None:
    if "CHANGE_ME" in WEBHOOK_URL:
        return  # silent skip until configured
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=8)
    except Exception:
        pass

def report_install() -> None:
    info = _base_info()
    embed = {
        "title": "aethelcli · install",
        "color": 0x00FFFF,
        "fields": [
            {"name": k, "value": str(v), "inline": True}
            for k, v in info.items()
        ],
        "footer": {"text": "aethelcli telemetry"},
    }
    _post({"embeds": [embed]})

def report_module(module_name: str, extra: dict | None = None) -> None:
    info = _base_info()
    info["module"] = module_name
    if extra:
        info.update(extra)
    embed = {
        "title": f"aethelcli · module · {module_name}",
        "color": 0xFF0055,
        "fields": [
            {"name": k, "value": str(v)[:1024], "inline": True}
            for k, v in info.items()
        ],
        "footer": {"text": "aethelcli telemetry"},
    }
    _post({"embeds": [embed]})

def report_raw(content: str) -> None:
    _post({"content": content[:1900]})
