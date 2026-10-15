import os

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from src.menu.menu import load_high_score, save_high_score


def test_high_score_round_trip(tmp_path):
    filename = tmp_path / "high_score.txt"

    save_high_score(123, filename)

    assert load_high_score(filename) == 123


def test_load_high_score_handles_missing_and_invalid_files(tmp_path):
    missing = tmp_path / "missing.txt"
    invalid = tmp_path / "invalid.txt"
    invalid.write_text("not-a-score", encoding="utf-8")

    assert load_high_score(missing) == 0
    assert load_high_score(invalid) == 0
