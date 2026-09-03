from __future__ import annotations

import os
import subprocess

from .models import AppProfile


class ProtectedLauncher:
    def __init__(self, socks_port: int = 9050) -> None:
        self.socks_port = socks_port
        self.processes: list[subprocess.Popen] = []

    def launch(self, profile: AppProfile) -> subprocess.Popen:
        profile.validate()
        environment = os.environ.copy()
        if profile.protected:
            proxy = f"socks5h://127.0.0.1:{self.socks_port}"
            environment.update({"ALL_PROXY": proxy, "all_proxy": proxy})
        process = subprocess.Popen(
            [profile.executable, *profile.arguments],
            env=environment,
            cwd=os.path.dirname(profile.executable) or None,
        )
        self.processes.append(process)
        return process

    def stop_all(self) -> None:
        for process in self.processes:
            if process.poll() is None:
                process.terminate()
        self.processes = []

