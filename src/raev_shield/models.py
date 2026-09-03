from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class AppProfile:
    name: str
    executable: str
    arguments: list[str]
    protected: bool = True

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("El nombre de la aplicación es obligatorio")
        path = Path(self.executable)
        if not path.is_file():
            raise ValueError(f"No existe el ejecutable: {path}")
        if path.suffix.lower() not in {".exe", ".com", ".bat", ".cmd"}:
            raise ValueError("Selecciona un ejecutable de Windows")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AppProfile":
        return cls(
            name=str(data["name"]),
            executable=str(data["executable"]),
            arguments=[str(value) for value in data.get("arguments", [])],
            protected=bool(data.get("protected", True)),
        )

