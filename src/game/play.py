import os
import sys
import time

import pygame
from PIL import Image, ImageFilter

from src.game import collision
from src.game import constants
from src.game import generation
from src.game import objects
from src.game import player_movement
from src.game import sound
from src.graphics import draw
from src.menu import colors
from src.paths import asset_path


class ButtonRect:
    """A rectangular button used by the in-game pause dialog."""

    def __init__(self, text, x, y, width, height, color, hover_color, text_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.isclicked = False

    def draw(self, screen, font):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(
            screen, colors.WHITE, self.rect,
            border_radius=10, width=constants.UI_BORDER_WIDTH,
        )
        text = font.render(self.text, True, self.text_color)
        screen.blit(
            text,
            (self.rect.centerx - text.get_width() / 2,
             self.rect.centery - text.get_height() / 2),
        )

    def is_clicked(self, clicked, pos):
        self.isclicked = clicked
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)


def button_from_image(file, width, height, x, y):
    """Load an image button and return its image and screen rectangle."""
    button = pygame.image.load(file).convert_alpha()
    button = pygame.transform.scale(button, (width, height))
    return button, button.get_rect(topleft=(x, y))


class Game:
    """Owns the game state and coordinates one frame of gameplay."""

    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.font_path = asset_path("fonts", "PressStart2P.ttf")
        self.button_font = pygame.font.Font(self.font_path, constants.FONT_SIZE)
        self.player = objects.Player(
            constants.PLAYER_START_X, constants.PLAYER_START_Y
        )
        self.coord_init = [
            constants.PLAYER_START_X, constants.PLAYER_START_Y
        ]
        self.current_roads = []
        self.next_spawn_roads = []
        generation.init_lines(self.current_roads, self.next_spawn_roads)

        self.player_line = constants.PLAYER_START_LINE
        self.player_dead = False
        self.moving = False
        self.move_direction = "down"
        self.deplacement_on_boat = False
        self.init_place_on_boat = None
        self.wood_we_are_moving_on_x = None
        self.wood_speed = None
        self.score_coins = 0
        self.score_pos = 0
        self.done = False
        self.pause = False
        self.is_volume_on = True
        self.launch_pause = False
        self.last_background = None
        self.result = None
        self.blurred_background = None
        self.pause_controls = None
        self.dt = 0
        self.actual = 0
        self.last_time = 0
        self.last_time_coin = 0
        self.index_animation = 0
        self.index_animation_coin = 0

        self.pause_button_image_default, self.button_rect = button_from_image(
            asset_path("icons", "pause_button.png"),
            constants.BUTTON_SIZE,
            constants.BUTTON_SIZE,
            *constants.BUTTON_POSITION,
        )
        self.pause_button_image_hover, _ = button_from_image(
            asset_path("icons", "pause_button_hover.png"),
            constants.BUTTON_SIZE,
            constants.BUTTON_SIZE,
            *constants.BUTTON_POSITION,
        )

    def run(self):
        """Run the game until the player dies or the window closes."""
        while not self.done:
            self._run_frame()

        if self.result is not None:
            return self.result
        pygame.quit()
        sys.exit()

    def _run_frame(self):
        self.dt = self.clock.tick(constants.FPS) / constants.MILLISECONDS_PER_SECOND
        self.actual = pygame.time.get_ticks()
        self.screen.fill(colors.BLACK)
        mouse_pos = pygame.mouse.get_pos()

        self._synchronise_player_position()
        self._prepare_pause_background()

        if self.pause:
            self._draw_pause_screen(mouse_pos)
        else:
            self._update_gameplay()

        self._draw_score()
        self._draw_pause_button(mouse_pos)
        self._handle_events(mouse_pos)
        self.last_background = self.screen.copy()
        pygame.display.flip()

    def _synchronise_player_position(self):
        if (
            (self.player.x - constants.PLAYER_MIN_X) % constants.CELL_SIZE == 0
            and not self.moving
        ):
            self.coord_init = [self.player.x, self.player.y]

    def _prepare_pause_background(self):
        if not self.launch_pause:
            return
        image = Image.frombytes(
            "RGB",
            self.last_background.get_size(),
            pygame.image.tostring(self.last_background, "RGB"),
        )
        blurred = image.filter(ImageFilter.GaussianBlur(constants.BLUR_RADIUS))
        self.blurred_background = pygame.image.fromstring(
            blurred.tobytes(), blurred.size, "RGB"
        )
        self.launch_pause = False

    def _update_gameplay(self):
        self._update_world()
        draw.draw_background(self.screen)
        self._draw_world()
        self._move_player_on_water()
        self._draw_player_and_check_collisions()
        self._collect_coin()
        self._handle_keyboard()
        self._finish_player_move()

    def _update_world(self):
        generation.add_moving_on_lines(
            self.current_roads, self.next_spawn_roads
        )
        self.player_line = generation.delete_old_line(
            self.player, self.current_roads, self.next_spawn_roads,
            self.player_line,
        )
        generation.add_lines(
            self.player, self.current_roads, self.next_spawn_roads
        )
        for road in self.current_roads:
            if road.road_type in ("road", "water", "rail"):
                for vehicle in road.list_cars:
                    vehicle.x += road.speed * self.dt

    def _draw_world(self):
        for road in self.current_roads:
            if road.road_type == "water":
                draw.animation_water(
                    self.index_animation,
                    -self.player.y + road.y + constants.WORLD_SCREEN_Y_OFFSET,
                    self.screen,
                )
        draw.draw_lines(
            self.player, self.current_roads, self.screen,
            self.index_animation_coin,
        )
        draw.draw_moving(self.player, self.current_roads, self.screen)

        if self.actual - self.last_time_coin > constants.ANIMATION_DURATION_MS:
            self.index_animation_coin = (
                self.index_animation_coin + 1
            ) % constants.COIN_ANIMATION_FRAMES
            self.last_time_coin = self.actual

    def _move_player_on_water(self):
        road = self.current_roads[self.player_line]
        if (
            -self.player.y + road.y == constants.WATER_PLAYER_OFFSET
            and road.road_type == "water"
            and road.lilypads == []
        ):
            self.player, self.coord_init = player_movement.movement_in_water(
                self.player, self.coord_init, self.current_roads,
                self.player_line, self.dt,
            )

    def _draw_player_and_check_collisions(self):
        if self.player_dead:
            draw.death_animation(
                self.player.x - constants.PLAYER_SCREEN_X_OFFSET,
                constants.PLAYER_SCREEN_Y - constants.DEATH_SCREEN_Y_OFFSET,
                self.screen,
                self.player_dead[1],
            )
            if time.time() - self.player_dead[0] > constants.DEATH_DISPLAY_DURATION_S:
                print("Votre score : ", self.score_pos + self.score_coins)
                self.result = (
                    self.last_background,
                    self.score_pos + self.score_coins,
                )
                self.done = True
            return

        if self.actual - self.last_time > constants.ANIMATION_DURATION_MS:
            self.index_animation = (
                self.index_animation + 1
            ) % constants.PLAYER_ANIMATION_FRAMES
            self.last_time = self.actual
        draw.movement_character(
            self.moving,
            self.move_direction,
            self.index_animation,
            self.player.x - constants.PLAYER_SCREEN_X_OFFSET,
            constants.PLAYER_SCREEN_Y,
            self.screen,
        )

        road = self.current_roads[self.player_line]
        if road.road_type in ("road", "rail"):
            if any(collision.collision(vehicle, self.player) for vehicle in road.list_cars):
                self.player_dead = [time.time(), "road"]
        elif road.road_type == "water" and not collision.collision_in_water(
            road, self.player, self.moving
        ):
            self.player_dead = [time.time(), "water"]

    def _collect_coin(self):
        coins = self.current_roads[self.player_line].coin
        if coins and collision.catch_coin(coins[0], self.player):
            self.score_coins += constants.COIN_SCORE
            self.current_roads[self.player_line].coin = []
            sound.coin_sound()

    def _handle_keyboard(self):
        keys = pygame.key.get_pressed()
        if (
            (keys[pygame.K_s] or keys[pygame.K_DOWN])
            and not self.moving
            and self.player.y < self.current_roads[0].y - constants.PLAYER_BACK_LIMIT
        ):
            self.moving = player_movement.vertical_deplacement_check(
                -1, self.current_roads, self.player, self.player_line
            )
            if self.moving:
                self.move_direction = "down"
                self.coord_init[1] = self.player.y
                self.player_line -= 1
                sound.walk_sound()

        if (keys[pygame.K_z] or keys[pygame.K_UP]) and not self.moving:
            self.moving = player_movement.vertical_deplacement_check(
                1, self.current_roads, self.player, self.player_line
            )
            if self.moving:
                self.move_direction = "up"
                self.coord_init[1] = self.player.y
                self.player_line += 1
                sound.walk_sound()

        self._handle_horizontal_key(
            keys[pygame.K_q] or keys[pygame.K_LEFT], -1, "left"
        )
        self._handle_horizontal_key(
            keys[pygame.K_d] or keys[pygame.K_RIGHT], 1, "right"
        )

    def _handle_horizontal_key(self, pressed, direction, direction_name):
        if not pressed or self.moving:
            return
        if direction == -1 and self.player.x <= constants.PLAYER_MIN_X:
            return
        if direction == 1 and self.player.x >= constants.PLAYER_MAX_X:
            return

        self.moving = True
        road = self.current_roads[self.player_line]
        if road.road_type == "water" and road.lilypads == []:
            (
                self.deplacement_on_boat,
                self.init_place_on_boat,
                self.move_direction,
                self.wood_we_are_moving_on_x,
                self.wood_speed,
            ) = player_movement.horizontal_deplacement_on_water_check(
                direction, self.current_roads, self.player, self.player_line
            )
        else:
            self.moving = player_movement.horizontal_deplacement_check(
                direction, self.current_roads, self.player,
                self.player_line, self.moving,
            )
            if self.moving:
                self.move_direction = direction_name
                self.coord_init[0] = self.player.x
        if self.moving:
            sound.walk_sound()

    def _finish_player_move(self):
        if not self.moving or self.player_dead:
            return
        if self.move_direction == "up":
            self.player, self.coord_init, self.moving = player_movement.vertical_deplacement(
                1, self.player, self.coord_init, self.dt
            )
        elif self.move_direction == "down":
            self.player, self.coord_init, self.moving = player_movement.vertical_deplacement(
                -1, self.player, self.coord_init, self.dt
            )
        elif self.move_direction in ("left", "right"):
            direction = -1 if self.move_direction == "left" else 1
            (
                self.player,
                self.coord_init,
                self.moving,
                self.deplacement_on_boat,
                self.wood_we_are_moving_on_x,
            ) = player_movement.horizontal_deplacement(
                direction, self.player, self.coord_init, self.dt,
                self.deplacement_on_boat, self.wood_we_are_moving_on_x,
                self.init_place_on_boat, self.wood_speed,
            )

    def _draw_score(self):
        self.score_pos = max(
            self.score_pos,
            round(-self.player.y - abs(constants.PLAYER_START_Y)),
        )
        text = self.button_font.render(
            f"Score : {self.score_pos + self.score_coins}", 1, (255, 0, 0)
        )
        self.screen.blit(text, constants.SCORE_POSITION)

    def _draw_pause_screen(self, mouse_pos):
        self.screen.blit(self.blurred_background, (0, 0))
        self.pause_controls = self._draw_pause_dialog(mouse_pos)

    def _draw_pause_dialog(self, mouse_pos):
        font = pygame.font.Font(self.font_path, constants.PAUSE_FONT_SIZE)
        dialog_rect = pygame.Rect(constants.PAUSE_DIALOG_RECT)
        pygame.draw.rect(self.screen, colors.WHITE, dialog_rect)
        pygame.draw.rect(
            self.screen, colors.BLACK, dialog_rect, constants.UI_BORDER_WIDTH
        )
        for text, y in zip(("Taking a", "break?"), constants.PAUSE_TEXT_POSITIONS):
            rendered = font.render(text, True, colors.BLACK)
            self.screen.blit(
                rendered,
                (constants.PAUSE_TEXT_CENTER_X - rendered.get_width() / 2, y),
            )

        play_button = ButtonRect(
            "Play", *constants.PAUSE_PLAY_BUTTON,
            colors.YELLOW, colors.LIGHT_YELLOW, colors.WHITE,
        )
        quit_button = ButtonRect(
            "Quit", *constants.PAUSE_QUIT_BUTTON,
            colors.RED, colors.LIGHT_RED, colors.WHITE,
        )
        volume_name = "sound_on_button.png" if self.is_volume_on else "sound_off_button.png"
        volume_button, volume_rect = button_from_image(
            asset_path("icons", volume_name),
            constants.BUTTON_SIZE,
            constants.BUTTON_SIZE,
            *constants.VOLUME_BUTTON_POSITION,
        )
        play_button.update_hover(mouse_pos)
        quit_button.update_hover(mouse_pos)
        play_button.draw(self.screen, self.button_font)
        quit_button.draw(self.screen, self.button_font)
        self.screen.blit(volume_button, volume_rect)
        return play_button, quit_button, volume_rect

    def _draw_pause_button(self, mouse_pos):
        image = (
            self.pause_button_image_hover
            if self.button_rect.collidepoint(mouse_pos)
            else self.pause_button_image_default
        )
        self.screen.blit(image, self.button_rect)

    def _handle_events(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(mouse_pos)

    def _handle_mouse_click(self, mouse_pos):
        if self.button_rect.collidepoint(mouse_pos):
            if not self.pause:
                self.launch_pause = True
            self.pause = not self.pause

        if not self.pause or self.pause_controls is None:
            return
        play_button, quit_button, volume_rect = self.pause_controls
        if play_button.is_clicked(False, mouse_pos):
            self.pause = False
        elif quit_button.is_clicked(False, mouse_pos):
            self.done = True
        elif volume_rect.collidepoint(mouse_pos):
            self._toggle_volume()

    def _toggle_volume(self):
        self.is_volume_on = not self.is_volume_on
        volume = 1 if self.is_volume_on else 0
        pygame.mixer.music.set_volume(volume)
        sound.coinsound.set_volume(0.6 if self.is_volume_on else 0)
        sound.walksound.set_volume(volume)


def play():
    """Keep the original public entry point used by the menu."""
    return Game().run()
