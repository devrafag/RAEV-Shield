from __future__ import annotations

import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from .launcher import ProtectedLauncher
from .models import AppProfile
from .network import check_tor
from .storage import ProfileStore
from .tor import TorManager, candidate_tor_paths


GREEN = "#38e07b"
PANEL = "#111914"
MUTED = "#8da097"


class ShieldApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("RAEV Shield — by Rafael G.G.")
        self.geometry("1060x680")
        self.minsize(850, 580)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.tor = TorManager()
        self.launcher = ProtectedLauncher()
        self.store = ProfileStore()
        self.profiles = self.store.load()
        paths = candidate_tor_paths()
        self.tor_path: Path | None = paths[0] if paths else None
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._build()
        self._render_profiles()

    def _build(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        side = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#08100b")
        side.grid(row=0, column=0, sticky="nsew")
        side.grid_propagate(False)
        ctk.CTkLabel(side, text="⬢  RAEV SHIELD", font=("Segoe UI", 18, "bold"), text_color="white").pack(anchor="w", padx=24, pady=(28, 4))
        ctk.CTkLabel(side, text="PRIVACY GATEWAY", font=("Segoe UI", 10), text_color=MUTED).pack(anchor="w", padx=52)
        for text in ("◉  Resumen", "▦  Aplicaciones", "⌁  Circuitos", "▣  Diagnóstico", "⚙  Configuración"):
            ctk.CTkButton(side, text=text, anchor="w", height=42, fg_color="#1a2920" if "Resumen" in text else "transparent", hover_color="#1a2920").pack(fill="x", padx=14, pady=3)
        ctk.CTkLabel(side, text="RG   Rafael G.G.\n       Propietario", justify="left", text_color="#bdcbc2").pack(side="bottom", anchor="w", padx=22, pady=24)

        main = ctk.CTkFrame(self, fg_color="#0b100d", corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(3, weight=1)
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 16))
        ctk.CTkLabel(header, text="Buenos días, Rafael", font=("Segoe UI", 23, "bold")).pack(side="left")
        ctk.CTkButton(header, text="⏻  Corte de emergencia", width=170, fg_color="#321719", hover_color="#4a2023", text_color="#ffaaaa", command=self.emergency_stop).pack(side="right")

        self.hero = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=18)
        self.hero.grid(row=1, column=0, sticky="ew", padx=28)
        self.status_icon = ctk.CTkLabel(self.hero, text="◈", width=68, height=68, corner_radius=34, fg_color="#173322", text_color=GREEN, font=("Segoe UI", 31))
        self.status_icon.grid(row=0, column=0, rowspan=2, padx=22, pady=22)
        self.status_title = ctk.CTkLabel(self.hero, text="Escudo detenido", font=("Segoe UI", 19, "bold"))
        self.status_title.grid(row=0, column=1, sticky="sw")
        self.status_copy = ctk.CTkLabel(self.hero, text="Inicia Tor para proteger aplicaciones compatibles.", text_color=MUTED)
        self.status_copy.grid(row=1, column=1, sticky="nw")
        self.master = ctk.CTkSwitch(self.hero, text="", progress_color=GREEN, command=self.toggle_tor)
        self.master.grid(row=0, column=2, rowspan=2, padx=24)
        self.hero.grid_columnconfigure(1, weight=1)

        tools = ctk.CTkFrame(main, fg_color="transparent")
        tools.grid(row=2, column=0, sticky="ew", padx=28, pady=16)
        self.ip_label = ctk.CTkLabel(tools, text="IP TOR   —", text_color=MUTED)
        self.ip_label.pack(side="left")
        ctk.CTkButton(tools, text="Seleccionar tor.exe", width=145, fg_color="#1b2b21", command=self.select_tor).pack(side="right", padx=(8, 0))
        ctk.CTkButton(tools, text="+ Proteger aplicación", width=165, fg_color=GREEN, text_color="#07120a", hover_color="#65eb94", command=self.add_profile).pack(side="right")

        self.apps = ctk.CTkScrollableFrame(main, fg_color=PANEL, corner_radius=18, label_text="APLICACIONES")
        self.apps.grid(row=3, column=0, sticky="nsew", padx=28, pady=(0, 28))
        self.apps.grid_columnconfigure(1, weight=1)

    def select_tor(self) -> None:
        path = filedialog.askopenfilename(title="Selecciona tor.exe", filetypes=[("Tor", "tor.exe"), ("Ejecutables", "*.exe")])
        if path:
            self.tor_path = Path(path)
            self.status_copy.configure(text=f"Tor seleccionado: {self.tor_path}")

    def toggle_tor(self) -> None:
        if self.master.get():
            if not self.tor_path:
                self.master.deselect()
                messagebox.showinfo("Tor necesario", "Instala Tor Browser o selecciona el archivo tor.exe oficial.")
                self.select_tor()
                return
            self.status_title.configure(text="Conectando…")
            self.status_copy.configure(text="Creando un circuito Tor seguro.")
            threading.Thread(target=self._start_tor, daemon=True).start()
        else:
            self.emergency_stop()

    def _start_tor(self) -> None:
        try:
            assert self.tor_path
            self.tor.start(self.tor_path)
            if not self.tor.wait_ready():
                raise RuntimeError("Tor no respondió a tiempo")
            result = check_tor()
            if not result["is_tor"]:
                raise RuntimeError("La conexión no fue reconocida como Tor")
            self.after(0, lambda: self._connected(result["ip"]))
        except Exception as exc:
            self.tor.stop()
            self.after(0, lambda: self._failed(str(exc)))

    def _connected(self, ip: str) -> None:
        self.status_title.configure(text="Escudo activo", text_color=GREEN)
        self.status_copy.configure(text="Proxy SOCKS local activo · DNS remoto habilitado.")
        self.ip_label.configure(text=f"IP TOR   {ip}", text_color=GREEN)

    def _failed(self, reason: str) -> None:
        self.master.deselect()
        self.status_title.configure(text="No se pudo conectar", text_color="#ff8f8f")
        self.status_copy.configure(text=reason)

    def add_profile(self) -> None:
        path = filedialog.askopenfilename(title="Elige una aplicación", filetypes=[("Aplicación", "*.exe")])
        if not path:
            return
        profile = AppProfile(Path(path).stem, path, [])
        self.profiles.append(profile)
        self.store.save(self.profiles)
        self._render_profiles()

    def _render_profiles(self) -> None:
        for widget in self.apps.winfo_children():
            widget.destroy()
        if not self.profiles:
            ctk.CTkLabel(self.apps, text="Añade una aplicación compatible con proxy SOCKS para empezar.", text_color=MUTED).grid(row=0, column=0, columnspan=3, padx=20, pady=35)
            return
        for row, profile in enumerate(self.profiles):
            ctk.CTkLabel(self.apps, text="▣", width=36, height=36, fg_color="#1a261e", corner_radius=10).grid(row=row, column=0, padx=(8, 12), pady=8)
            ctk.CTkLabel(self.apps, text=f"{profile.name}\n{profile.executable}", justify="left", anchor="w").grid(row=row, column=1, sticky="ew", pady=8)
            ctk.CTkButton(self.apps, text="Abrir protegido", width=125, fg_color="#1d3927", hover_color="#285438", command=lambda p=profile: self.launch_profile(p)).grid(row=row, column=2, padx=8)

    def launch_profile(self, profile: AppProfile) -> None:
        if not self.tor.running:
            messagebox.showwarning("Escudo detenido", "Activa el escudo antes de abrir la aplicación.")
            return
        try:
            self.launcher.launch(profile)
        except Exception as exc:
            messagebox.showerror("No se pudo abrir", str(exc))

    def emergency_stop(self) -> None:
        self.launcher.stop_all()
        self.tor.stop()
        self.master.deselect()
        self.status_title.configure(text="Tráfico bloqueado", text_color="#ffaaaa")
        self.status_copy.configure(text="Tor y todas las aplicaciones iniciadas por RAEV Shield se han detenido.")
        self.ip_label.configure(text="IP TOR   —", text_color=MUTED)

    def _close(self) -> None:
        self.emergency_stop()
        self.destroy()


def main() -> None:
    ShieldApp().mainloop()

