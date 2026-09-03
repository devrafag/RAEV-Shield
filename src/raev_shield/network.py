from __future__ import annotations

import requests


def check_tor(socks_port: int = 9050, timeout: int = 12) -> dict:
    proxies = {
        "http": f"socks5h://127.0.0.1:{socks_port}",
        "https": f"socks5h://127.0.0.1:{socks_port}",
    }
    response = requests.get("https://check.torproject.org/api/ip", proxies=proxies, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    return {"is_tor": bool(data.get("IsTor")), "ip": str(data.get("IP", "—"))}

