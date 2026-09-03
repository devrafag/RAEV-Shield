from __future__ import annotations

import json
from pathlib import Path

from platformdirs import user_config_dir

from .models import AppProfile


class ProfileStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(user_config_dir("RAEV Shield", "Rafael GG")) / "profiles.json"

    def load(self) -> list[AppProfile]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            return [AppProfile.from_dict(item) for item in raw if isinstance(item, dict)]
        except (OSError, ValueError, KeyError, TypeError):
            return []

    def save(self, profiles: list[AppProfile]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps([profile.to_dict() for profile in profiles], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary.replace(self.path)

