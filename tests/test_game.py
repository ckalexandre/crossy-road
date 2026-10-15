import os
from types import SimpleNamespace

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from src.game import constants
from src.game import objects
from src.game.play import ButtonRect, Game


def make_game():
    pygame.init()
    return Game()


def test_button_rect_tracks_hover_and_click():
    button = ButtonRect("Play", 10, 20, 100, 40, (1, 2, 3), (4, 5, 6), (255, 255, 255))

    button.update_hover((20, 30))
    assert button.is_hovered is True
    assert button.is_clicked(True, (20, 30)) is True
    assert button.isclicked is True

    button.update_hover((0, 0))
    assert button.is_hovered is False
    assert button.is_clicked(False, (0, 0)) is False


def test_game_initializes_play_state():
    game = make_game()

    try:
        assert game.done is False
        assert game.pause is False
        assert game.player.x == constants.PLAYER_START_X
        assert len(game.current_roads) == 5
        assert game.font_path.endswith("PressStart2P.ttf")
    finally:
        pygame.quit()


def test_quit_event_marks_game_done():
    game = make_game()

    try:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        game._handle_events((0, 0))
        assert game.done is True
    finally:
        pygame.quit()


def test_pause_button_event_toggles_pause():
    game = make_game()

    try:
        position = game.button_rect.center
        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": position})
        )
        game._handle_events(position)
        assert game.pause is True
        assert game.launch_pause is True

        game.pause_controls = None
        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": position})
        )
        game._handle_events(position)
        assert game.pause is False
    finally:
        pygame.quit()


def test_pause_dialog_buttons_resume_or_quit():
    game = make_game()
    play = ButtonRect("Play", 10, 10, 100, 40, (0, 0, 0), (0, 0, 0), (255, 255, 255))
    quit_button = ButtonRect("Quit", 120, 10, 100, 40, (0, 0, 0), (0, 0, 0), (255, 255, 255))
    volume = pygame.Rect(230, 10, 40, 40)

    try:
        game.pause = True
        game.pause_controls = (play, quit_button, volume)
        game._handle_mouse_click((20, 20))
        assert game.pause is False

        game.pause = True
        game._handle_mouse_click((130, 20))
        assert game.done is True
    finally:
        pygame.quit()


def test_score_updates_when_drawing():
    game = make_game()

    try:
        game.player.y = -250
        game._draw_score()
        assert game.score_pos == 241
    finally:
        pygame.quit()


def test_horizontal_key_respects_screen_boundaries():
    game = make_game()

    try:
        game.player.x = constants.PLAYER_MIN_X
        game._handle_horizontal_key(True, -1, "left")
        assert game.moving is False

        game.player.x = constants.PLAYER_MAX_X
        game._handle_horizontal_key(True, 1, "right")
        assert game.moving is False
    finally:
        pygame.quit()


def test_frame_delta_time_converts_milliseconds_to_seconds(monkeypatch):
    game = make_game()

    try:
        game.clock = SimpleNamespace(tick=lambda fps: 16)
        game._run_frame()
        assert game.dt == 0.016
    finally:
        pygame.quit()
