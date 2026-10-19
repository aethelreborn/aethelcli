# language: Python, file: gui.py
# customtkinter GUI shell for aethelcli

import threading
from typing import Callable

import customtkinter as ctk

from aethelcli.webhook import report_module
from aethelcli.modules import MODULES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class AethelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("aethelcli")
        self.geometry("720x520")
        self.minsize(640, 420)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkLabel(
            self,
            text="aethelcli",
            font=ctk.CTkFont(family="Consolas", size=28, weight="bold"),
        )
        header.grid(row=0, column=0, pady=(18, 6), sticky="n")

        sub = ctk.CTkLabel(self, text="module launcher · darkie.dpdns.org", text_color="gray")
        sub.grid(row=0, column=0, pady=(50, 0), sticky="n")

        frame = ctk.CTkScrollableFrame(self, label_text="Modules")
        frame.grid(row=1, column=0, padx=20, pady=12, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        for i, (key, name, runner) in enumerate(MODULES):
            btn = ctk.CTkButton(
                frame,
                text=f"{key}.  {name}",
                height=42,
                anchor="w",
                command=lambda r=runner, n=name: self._run_module(r, n),
            )
            btn.grid(row=i, column=0, padx=8, pady=6, sticky="ew")

        footer = ctk.CTkLabel(self, text="TUI: aethelcli   |   GUI: aethelcli --gui", text_color="gray60")
        footer.grid(row=2, column=0, pady=(0, 12))

        self.log = ctk.CTkTextbox(self, height=110, font=ctk.CTkFont(family="Consolas", size=12))
        self.log.grid(row=3, column=0, padx=20, pady=(0, 16), sticky="ew")
        self.log.insert("end", "[*] ready\n")
        self.log.configure(state="disabled")

    def _log(self, msg: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _run_module(self, runner: Callable, name: str) -> None:
        report_module(name, {"ui": "gui"})
        self._log(f"[+] launching {name} (check terminal for interactive prompts)")
        def target():
            try:
                runner()
                self.after(0, lambda: self._log(f"[+] {name} finished"))
            except Exception as e:
                self.after(0, lambda: self._log(f"[!] {name}: {e}"))
        threading.Thread(target=target, daemon=True).start()

def launch_gui() -> None:
    app = AethelApp()
    app.mainloop()
