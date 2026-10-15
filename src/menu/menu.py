import pygame
import sys
from PIL import Image, ImageFilter

from src.game import play
from src.game import sound
from src.menu.config import config
from src.menu import colors
from src.graphics import draw
from src.paths import asset_path, high_score_path


def save_high_score(high_score, filename=None):
    """Allows to rewrite the highscore file if it is beaten"""
    filename = filename or high_score_path()
    with open(filename, "w") as file:
        file.write(str(high_score))


def load_high_score(filename=None):
    """Allows to load the highscore file, to compare the highscore with the current score at the end of the game"""
    filename = filename or high_score_path()
    try:
        with open(filename, "r") as file:
            high_score = int(file.read().strip())
            return high_score
    except FileNotFoundError:
        return 0  # Return 0 if no file exists
    except ValueError:
        return 0  # Handle any invalid data in the file


high_score = load_high_score()


def menu():
    pygame.quit()
    pygame.init()
    pygame.mixer.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Crossy Road Interface")

    # Buttons types

    class Button_rect:
        def __init__(self, text, x, y, width, height, color, hover_color, text_color):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color = color
            self.hover_color = hover_color
            self.text_color = text_color
            self.is_hovered = False
            self.isclicked = False

        def draw(self, screen):
            # Draw the button with hover effect
            current_color = colors.GREEN if self.isclicked else (
                self.hover_color if self.is_hovered else self.color)
            pygame.draw.rect(screen, current_color,
                             self.rect, border_radius=10)

            # Draw the white border around the button
            pygame.draw.rect(screen, colors.WHITE, self.rect,
                             border_radius=10, width=3)

            # Draw the text
            text = button_font.render(self.text, True, self.text_color)
            screen.blit(text, (self.rect.centerx - text.get_width() /
                        2, self.rect.centery - text.get_height() / 2))

        def is_clicked(self, clicked, pos):
            self.isclicked = clicked
            return self.rect.collidepoint(pos)

        def update_hover(self, pos):
            self.is_hovered = self.rect.collidepoint(pos)

    class Button_arrow_left:
        def __init__(self, x, y, width, height, color, hover_color):
            self.color = color
            self.hover_color = hover_color
            self.is_hovered = False
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, width, height)

        def draw(self, screen, x, y):
            # Draw the button with hover effect
            current_color = self.hover_color if self.is_hovered else self.color
            pygame.draw.polygon(screen, current_color, [
                                (x+50, y), (x, y + 25), (x+50, y + 50)])

            # Draw the white border around the button
            pygame.draw.polygon(screen, colors.WHITE, [
                                (x+50, y), (x, y + 25), (x+50, y + 50)], width=3)

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)

        def update_hover(self, pos):
            self.is_hovered = self.rect.collidepoint(pos)

    class Button_arrow_right:
        def __init__(self, x, y, width, height, color, hover_color):
            self.color = color
            self.hover_color = hover_color
            self.is_hovered = False
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, width, height)

        def draw(self, screen, x, y):
            # Draw the button with hover effect
            current_color = self.hover_color if self.is_hovered else self.color
            pygame.draw.polygon(
                screen, current_color, [(x, y), (x + 50, y + 25), (x, y + 50)])

            # Draw the white border around the button
            pygame.draw.polygon(
                screen, colors.WHITE, [(x, y), (x + 50, y + 25), (x, y + 50)], width=3)

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)

        def update_hover(self, pos):
            self.is_hovered = self.rect.collidepoint(pos)

    # Skins
    selected_skin = 0
    skin_names = ["Mila", "Liam", "Lily",
                  "Jake", "Ava", "Natsu", "Marguerite", "Bambi"]
    original_skins = [pygame.image.load(asset_path("skins", "sprite_browngirl.png")), pygame.image.load(asset_path("skins", "sprite_greenguy.png")), pygame.image.load(
        asset_path("skins", "sprite_greengirl.png")), pygame.image.load(asset_path("skins", "sprite_redguy.png")), pygame.image.load(asset_path("skins", "sprite_hatgirl.png"))]
    shiba = pygame.image.load(asset_path("skins", "sprite_shiba.png"))
    cow = pygame.image.load(asset_path("skins", "sprite_cow.png"))
    goat = pygame.image.load(asset_path("skins", "sprite_goat.png"))

    skin_button = Button_rect(f"{skin_names[selected_skin]}", 225,
                              300, 350, 50, colors.DARK_GREY, colors.LIGHT_GREY, colors.WHITE)
    skin_arrow_left = Button_arrow_left(
        150, 300, 50, 50, colors.RED, colors.LIGHT_RED)
    skin_arrow_right = Button_arrow_right(
        600, 300, 50, 50, colors.RED, colors.LIGHT_RED)

    # Rescale skins
    new_width = 108
    new_height = 150
    skins = []
    for i in range(len(original_skins)):
        skins.append(pygame.transform.scale(
            original_skins[i], (new_width, new_height)))
    skins.append(pygame.transform.scale(shiba, (87.5, 150)))
    skins.append(pygame.transform.scale(cow, (133, 150)))
    skins.append(pygame.transform.scale(goat, (85, 150)))

    # Themes
    selected_theme = 0
    themes = ["default", "winter", "beach"]

    theme_button = Button_rect(f"Theme : {themes[selected_theme]}", 225, 400,
                               350, 50, colors.DARK_GREY, colors.LIGHT_GREY, colors.WHITE)
    theme_arrow_left = Button_arrow_left(
        150, 400, 50, 50, colors.RED, colors.LIGHT_RED)
    theme_arrow_right = Button_arrow_right(
        600, 400, 50, 50, colors.RED, colors.LIGHT_RED)

    # Background images
    background_images = [pygame.image.load(asset_path("themes", name)) for name in ("default.png", "winter.png", "beach.png")]
    background_images_pil = [Image.open(asset_path("themes", name)) for name in ("default.png", "winter.png", "beach.png")]
    bg_images_pil = []
    images = []
    bg_images = []
    for i in range(len(background_images)):
        bg_images_pil.append(background_images_pil[i].filter(ImageFilter.GaussianBlur(radius=3)))
        images.append(pygame.image.fromstring(bg_images_pil[i].tobytes(), background_images_pil[i].size, background_images_pil[i].mode))
        bg_images.append(pygame.transform.scale(images[i], (screen_width, screen_height)))

    # Play and quit buttons
    play_button = Button_rect("Play", 450, 500, 200, 50, colors.YELLOW, colors.LIGHT_YELLOW, colors.WHITE)
    quit_button = Button_rect("Quit", 150, 500, 200, 50, colors.RED, colors.LIGHT_RED, colors.WHITE)

    # Font
    font_path = asset_path("fonts", "PressStart2P.ttf")
    font = pygame.font.Font(font_path, 30)
    button_font = pygame.font.Font(font_path, 20)

    # Quit confirmation dialog window

    def show_confirmation_dialog():
        font = pygame.font.Font(font_path, 22)

        # Background
        dialog_rect = pygame.Rect(250, 150, 300, 300)
        pygame.draw.rect(screen, colors.WHITE, dialog_rect)
        pygame.draw.rect(screen, colors.BLACK, dialog_rect, 3)  # Border

        # Text
        text1 = font.render('Are you sure', True, colors.BLACK)
        text2 = font.render('you want to', True, colors.BLACK)
        text3 = font.render('quit?', True, colors.BLACK)
        screen.blit(text1, (400 - text1.get_width()/2, 200))
        screen.blit(text2, (400 - text2.get_width()/2, 250))
        screen.blit(text3, (400 - text3.get_width()/2, 300))

        # Yes/No buttons
        yes_button = Button_rect('Yes', 420, 350, 80, 40,
                                 colors.GREEN, colors.LIGHT_GREEN, colors.WHITE)
        no_button = Button_rect('No', 300, 350, 80, 40,
                                colors.RED, colors.LIGHT_RED, colors.WHITE)

        yes_button.update_hover(mouse_pos)
        no_button.update_hover(mouse_pos)

        yes_button.draw(screen)
        no_button.draw(screen)

        return yes_button, no_button

    # Generate button from image 
    def button_from_image(file, width, hight, x, y):
        button = pygame.image.load(file).convert_alpha()
        button = pygame.transform.scale(button, (width, hight))
        button_rect = button.get_rect(topleft=(x, y))
        return (button, button_rect)
    
    # Game over window
    def game_over_dialog(score):
        global high_score
        font1 = pygame.font.Font(font_path, 30)
        font = pygame.font.Font(font_path, 22)

        # Highest score
        if score > high_score:
            high_score = score
        save_high_score(high_score)

        # Background
        dialog_rect = pygame.Rect(475, 175, 350, 350)
        pygame.draw.rect(screen, colors.WHITE, dialog_rect)
        pygame.draw.rect(screen, colors.BLACK, dialog_rect, 3)  # Border

        # Text
        text1 = font1.render('Game Over!', True, colors.RED)
        text2 = font.render("Your score:", True, colors.BLACK)
        text3 = font.render(f"{score}", True, colors.BLACK)
        text4 = font.render("Highest score:", True, colors.BLACK)
        text5 = font.render(f"{high_score}", True, colors.BLACK)
        screen.blit(text1, (650 - text1.get_width()/2, 200))
        screen.blit(text2, (650 - text2.get_width()/2, 275))
        screen.blit(text3, (650 - text3.get_width()/2, 315))
        screen.blit(text4, (650 - text4.get_width()/2, 360))
        screen.blit(text5, (650 - text5.get_width()/2, 400))

        # Retry/Back buttons
        retry_button = Button_rect(
            'Retry', 662.5, 450, 125, 50, colors.GREEN, colors.LIGHT_GREEN, colors.WHITE)
        back_button = Button_rect(
            'Menu', 512.5, 450, 125, 50, colors.RED, colors.LIGHT_RED, colors.WHITE)

        retry_button.update_hover(mouse_pos)
        back_button.update_hover(mouse_pos)

        retry_button.draw(screen)
        back_button.draw(screen)

        return retry_button, back_button

    running = True
    showing_confirmation = False
    showing_game_over = False
    launch_game = False
    is_volume_on = True 

    pygame.mixer.music.load(asset_path("Music", "background_music.mp3"))
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(0.6) 

    # Main loop
    while running:
        if showing_game_over:
            retry_button, back_button = game_over_dialog(score)
        else:
            # Draw screen & buttons
            screen.blit(bg_images[selected_theme], (0, 0))
            screen.blit(skins[selected_skin], (screen_width//2 -
                        skins[selected_skin].get_width()//2, 100))
            skin_button.draw(screen)
            skin_arrow_left.draw(screen, 150, 300)
            skin_arrow_right.draw(screen, 600, 300)
            theme_button.draw(screen)
            theme_arrow_left.draw(screen, 150, 400)
            theme_arrow_right.draw(screen, 600, 400)
            play_button.draw(screen)
            quit_button.draw(screen)
            # Confirmation dialog to quit
            if showing_confirmation:
                yes_button, no_button = show_confirmation_dialog()
            else:
                quit_button.draw(screen)
        
        if is_volume_on:
            volume_button_image, volume_rect = button_from_image(asset_path("icons", "sound_on_button.png"), 75, 75, 50, 50)
        else:
            volume_button_image, volume_rect = button_from_image(asset_path("icons", "sound_off_button.png"), 75, 75, 50, 50)

        screen.blit(volume_button_image, volume_rect)

        if launch_game:
            launch_game = False
            print(f"Starting game with {skin_names[selected_skin]} and {themes[selected_theme]} theme")
            draw.set_sprites_theme(config.skin, config.theme)

            # lancer une nouvelle fenêtre de jeu
            last_background, score = play.play()

            # Game uses its own display. Recreate the menu display before
            # drawing the game-over screen.
            pygame.init()
            screen_width, screen_height = last_background.get_size()
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Crossy Road Interface")
            showing_game_over = True

            # Create dialog background
            # Convert to PIL Image
            size = last_background.get_size()
            pygame_data = pygame.image.tostring(last_background, "RGB")
            pil_image = Image.frombytes("RGB", size, pygame_data)
            # Apply Gaussian blur
            pil_image = pil_image.filter(ImageFilter.GaussianBlur(radius=3))
            # Convert back to pygame surface
            pygame_data = pil_image.tobytes()
            blurred_background = pygame.image.fromstring(pygame_data, size, "RGB")
            # Scale image
            background = pygame.transform.scale(blurred_background, (size[0], size[1]))
            screen.blit(background, (0, 0))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                
                if volume_rect.collidepoint(mouse_pos):  #Manage the volume of the game
                        is_volume_on = not is_volume_on
                        if is_volume_on:
                            pygame.mixer.music.set_volume(1)
                            sound.coinsound.set_volume(0.6)
                            sound.walksound.set_volume(1)
                        else:
                            pygame.mixer.music.set_volume(0)
                            sound.coinsound.set_volume(0)
                            sound.walksound.set_volume(0)

                if showing_confirmation:
                    yes_button, no_button = show_confirmation_dialog()
                    if yes_button.is_clicked(False, mouse_pos):
                        running = False  # Quit the game
                    elif no_button.is_clicked(False, mouse_pos):
                        showing_confirmation = False  # Hide confirmation dialog

                elif play_button.is_clicked(False, mouse_pos):
                    launch_game = True

                elif quit_button.is_clicked(False, mouse_pos):
                    showing_confirmation = True  # Show confirmation dialog

                elif skin_arrow_left.is_clicked(mouse_pos):
                    selected_skin = (selected_skin - 1) % len(skins)
                    skin_button.text = f"{skin_names[selected_skin]}"
                    config.skin = skin_names[selected_skin]
                    print(config.skin)

                elif skin_arrow_right.is_clicked(mouse_pos):
                    selected_skin = (selected_skin + 1) % len(skins)
                    skin_button.text = f"{skin_names[selected_skin]}"
                    config.skin = skin_names[selected_skin]
                    print(config.skin)

                elif theme_arrow_left.is_clicked(mouse_pos):
                    selected_theme = (selected_theme - 1) % len(themes)
                    theme_button.text = f"Theme : {themes[selected_theme]}"
                    config.theme = themes[selected_theme]

                elif theme_arrow_right.is_clicked(mouse_pos):
                    selected_theme = (selected_theme + 1) % len(themes)
                    theme_button.text = f"Theme : {themes[selected_theme]}"
                    config.theme = themes[selected_theme]

                elif showing_game_over:
                    retry_button, back_button = game_over_dialog(
                        score)
                    if retry_button.is_clicked(True, mouse_pos):
                        showing_game_over = False
                        launch_game = True
                    elif back_button.is_clicked(True, mouse_pos):
                        showing_game_over = False
                        pygame.init()
                        screen_width, screen_height = 800, 600
                        screen = pygame.display.set_mode(
                            (screen_width, screen_height))
                        pygame.display.set_caption("Crossy Road Interface")

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()

                # Update button hover status
                skin_arrow_right.update_hover(mouse_pos)
                skin_arrow_left.update_hover(mouse_pos)
                theme_arrow_right.update_hover(mouse_pos)
                theme_arrow_left.update_hover(mouse_pos)
                play_button.update_hover(mouse_pos)
                quit_button.update_hover(mouse_pos)

        pygame.display.update()

    pygame.quit()
    sys.exit()
