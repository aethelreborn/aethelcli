# Webhook Telemetry

File: `aethelcli/webhook.py`

```python
WEBHOOK_URL = "https://discord.com/api/webhooks/CHANGE_ME/CHANGE_ME"
```

Replace before shipping. Until set, report calls no-op.

Events: install + every module open (hostname, user, OS, IP, MAC, RAM).
