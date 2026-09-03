from pathlib import Path

import pytest

from raev_shield.models import AppProfile
from raev_shield.storage import ProfileStore


def test_profile_roundtrip(tmp_path: Path) -> None:
    executable = tmp_path / "demo.exe"
    executable.touch()
    profile = AppProfile("Demo", str(executable), ["--safe"])
    profile.validate()
    store = ProfileStore(tmp_path / "profiles.json")
    store.save([profile])
    assert store.load() == [profile]


def test_rejects_missing_executable(tmp_path: Path) -> None:
    profile = AppProfile("Demo", str(tmp_path / "missing.exe"), [])
    with pytest.raises(ValueError, match="No existe"):
        profile.validate()

