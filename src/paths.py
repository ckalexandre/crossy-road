"""Project paths that do not depend on the current working directory."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_ROOT = PROJECT_ROOT / "src" / "static"


def asset_path(*parts: str) -> str:
    """Return an absolute path to a bundled asset."""
    return str(ASSETS_ROOT.joinpath(*parts))


def high_score_path() -> str:
    """Return the path to the persistent high-score file."""
    return str(PROJECT_ROOT / "src" / "high_score.txt")
