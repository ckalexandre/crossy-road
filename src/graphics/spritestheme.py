import pygame
from src.menu.config import config
from src.paths import asset_path


# We load all designs 
road_up_img = pygame.image.load(asset_path("sprites", "road_up.png"))
road_mid_img = pygame.image.load(asset_path("sprites", "road_mid.png"))
road_down_img = pygame.image.load(asset_path("sprites", "road_down.png"))
road_solo_img = pygame.image.load(asset_path("sprites", "road_solo.png"))
lilypad_img = pygame.image.load(asset_path("sprites", "lilypad.png"))
car_img = [pygame.image.load(asset_path("car", f"{i}.png")) for i in range(1,24)]
car_img = [pygame.transform.scale(car_img[i], (140, 90)) for i in range(len(car_img))]
traffic_green = pygame.image.load(asset_path("sprites", "traffic_green.png"))
traffic_red = pygame.image.load(asset_path("sprites", "traffic_red.png"))
coin_img = [pygame.image.load(asset_path("sprites", f"coin{i}.png")) for i in range (1,7)]
train_img = pygame.image.load(asset_path("sprites", "train.png"))
raft_img = {300: pygame.image.load(asset_path("sprites", "raft300.png")),
            400: pygame.image.load(asset_path("sprites", "raft400.png")),
            500: pygame.image.load(asset_path("sprites", "raft500.png"))}
blood_img = pygame.image.load(asset_path("death", "blood.png"))
drop_img = pygame.image.load(asset_path("sprites", "waterdrop.png"))

# Theme and skin choice
theme = config.theme
skin = config.skin

images_background = [pygame.image.load(asset_path(theme, f"{i}.png")) for i in range(0, 10)]

if theme == "winter":
    images_river = [pygame.image.load(asset_path("winter", f"{i}.png")) for i in range(2, 6)]
else:
    images_river = [pygame.image.load(asset_path("default", f"{i}.png")) for i in range(2, 6)]

images_skin = {
    "up": [pygame.image.load(asset_path(skin, f"up{i}.png")) for i in range(1, 5)],
    "down": [pygame.image.load(asset_path(skin, f"down{i}.png")) for i in range(1, 5)],
    "left": [pygame.image.load(asset_path(skin, f"left{i}.png")) for i in range(1, 5)],
    "right": [pygame.image.load(asset_path(skin, f"right{i}.png")) for i in range(1, 5)],
    "idle_up": [pygame.image.load(asset_path(skin, "idle_up.png"))],
    "idle_down": [pygame.image.load(asset_path(skin, "idle_down.png"))],
    "idle_left": [pygame.image.load(asset_path(skin, "idle_left.png"))],
    "idle_right": [pygame.image.load(asset_path(skin, "idle_right.png"))]}

for key in images_skin:
    for i in range(len(images_skin[key])):
        images_skin[key][i] = pygame.transform.scale(
            images_skin[key][i], (80, 80))