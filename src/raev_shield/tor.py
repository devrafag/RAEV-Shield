from __future__ import annotations

import os
import socket
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Callable


class TorError(RuntimeError):
    pass


def candidate_tor_paths() -> list[Path]:
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    program_files = Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
    program_files_x86 = Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"))
    candidates = [
        program_files / "Tor Browser" / "Browser" / "TorBrowser" / "Tor" / "tor.exe",
        program_files_x86 / "Tor Browser" / "Browser" / "TorBrowser" / "Tor" / "tor.exe",
        local / "Tor Browser" / "Browser" / "TorBrowser" / "Tor" / "tor.exe",
        Path.cwd() / "tor" / "tor.exe",
    ]
    return [path for path in candidates if str(path) and path.is_file()]


class TorManager:
    def __init__(self, socks_port: int = 9050) -> None:
        self.socks_port = socks_port
        self.process: subprocess.Popen[str] | None = None
        self.data_dir: Path | None = None
        self._reader: threading.Thread | None = None

    @property
    def running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def start(self, executable: Path, on_log: Callable[[str], None] | None = None) -> None:
        if self.running:
            return
        if not executable.is_file():
            raise TorError("No se encuentra tor.exe")
        self.data_dir = Path(tempfile.mkdtemp(prefix="raev-shield-tor-"))
        command = [
            str(executable),
            "--SocksPort", f"127.0.0.1:{self.socks_port}",
            "--DataDirectory", str(self.data_dir),
            "--ClientOnly", "1",
            "--AvoidDiskWrites", "1",
            "--SafeLogging", "1",
        ]
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=flags,
        )
        if on_log and self.process.stdout:
            self._reader = threading.Thread(target=self._read_logs, args=(on_log,), daemon=True)
            self._reader.start()

    def _read_logs(self, callback: Callable[[str], None]) -> None:
        assert self.process and self.process.stdout
        for line in self.process.stdout:
            callback(line.rstrip())

    def wait_ready(self, timeout: float = 45) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.process and self.process.poll() is not None:
                return False
            try:
                with socket.create_connection(("127.0.0.1", self.socks_port), timeout=0.5):
                    return True
            except OSError:
                time.sleep(0.4)
        return False

    def stop(self) -> None:
        process, self.process = self.process, None
        if not process or process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)

