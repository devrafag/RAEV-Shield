import runpy
from pathlib import Path


def test_entrypoint_works_without_package_context() -> None:
    entrypoint = Path(__file__).parents[1] / "src" / "raev_shield" / "__main__.py"
    namespace = runpy.run_path(str(entrypoint), run_name="raev_shield_packaging_test")
    assert callable(namespace["main"])
