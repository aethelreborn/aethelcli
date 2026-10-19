# Architecture

```
aethelcli/
├── install/          # source copies of install scripts
├── public/           # Vercel static root
│   └── aethelacli/   # /aethelacli/install endpoint
├── aethelcli/        # Python package
│   ├── main.py       # TUI
│   ├── gui.py        # CustomTkinter
│   ├── webhook.py
│   └── modules/
├── vercel.json
└── requirements.txt
```

Install flow: curl endpoint → bash → git clone this repo → venv → launcher → TUI.
