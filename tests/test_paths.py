from pathlib import Path

from src.paths import ASSETS_ROOT, PROJECT_ROOT, asset_path, high_score_path


def test_project_paths_are_absolute_and_inside_project():
    assert PROJECT_ROOT.is_absolute()
    assert ASSETS_ROOT.is_dir()
    assert Path(asset_path("fonts", "PressStart2P.ttf")).is_file()
    assert Path(high_score_path()) == PROJECT_ROOT / "src" / "high_score.txt"


def test_asset_path_does_not_depend_on_current_directory(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    resolved = Path(asset_path("themes", "default.png"))

    assert resolved.is_absolute()
    assert resolved.is_file()
