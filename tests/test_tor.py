from pathlib import Path

from raev_shield.tor import TorManager


def test_tor_starts_stopped() -> None:
    manager = TorManager(socks_port=19050)
    assert manager.running is False


def test_stop_is_idempotent() -> None:
    manager = TorManager()
    manager.stop()
    manager.stop()

