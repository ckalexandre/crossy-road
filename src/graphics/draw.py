import pygame
import random
from time import time

from src.game import generation
from src.game import objects
from src.graphics import animation
from src.menu.config import config
from src.graphics import spritestheme
from src.paths import asset_path


def set_sprites_theme(skin, theme):
    """imports the right images for the choice of the skin and of the theme"""
    spritestheme.images_background = [pygame.image.load(asset_path(theme, f"{i}.png")) for i in range(0, 10)]

    if theme == "winter":
        spritestheme.images_river = [pygame.image.load(asset_path("winter", f"{i}.png")) for i in range(2, 6)]
    else:
        spritestheme.images_river = [pygame.image.load(asset_path("default", f"{i}.png")) for i in range(2, 6)]

    spritestheme.images_skin = {
        "up": [pygame.image.load(asset_path(skin, f"up{i}.png")) for i in range(1, 5)],
        "down": [pygame.image.load(asset_path(skin, f"down{i}.png")) for i in range(1, 5)],
        "left": [pygame.image.load(asset_path(skin, f"left{i}.png")) for i in range(1, 5)],
        "right": [pygame.image.load(asset_path(skin, f"right{i}.png")) for i in range(1, 5)],
        "idle_up": [pygame.image.load(asset_path(skin, "idle_up.png"))],
        "idle_down": [pygame.image.load(asset_path(skin, "idle_down.png"))],
        "idle_left": [pygame.image.load(asset_path(skin, "idle_left.png"))],
        "idle_right": [pygame.image.load(asset_path(skin, "idle_right.png"))]}

    for key in spritestheme.images_skin:
        for i in range(len(spritestheme.images_skin[key])):
            spritestheme.images_skin[key][i] = pygame.transform.scale(
                spritestheme.images_skin[key][i], (80, 80))


def draw_background(screen):
    """Fill the screen before world layers are rendered."""
    background = spritestheme.images_background[0]
    for y in range(0, screen.get_height(), background.get_height()):
        screen.blit(background, (0, y))


def draw_lines(player, current_roads, screen, index_animation_coin):
    """draws lines of texture on screen"""
    for road_num in range(len(current_roads)):

        current_road = current_roads[road_num]
        objects.Line.lilypads_generated = False

        if current_road.road_type == "grass": # we draw the line with trees, rocks and coins
            screen.blit(spritestheme.images_background[0],
                        (0, - player.y + current_road.y + 350))
            for tree_pos in current_road.trees:
                tree_x = tree_pos[0]
                tree_y = - player.y + \
                    current_roads[road_num].y + tree_pos[1] + 400
                screen.blit(spritestheme.images_background[8], (tree_x-50, tree_y-50))
            for rocks_pos in current_road.rocks:
                rocks_x = rocks_pos[0]
                rocks_y = - player.y + \
                    current_roads[road_num].y + rocks_pos[1] + 400
                screen.blit(spritestheme.images_background[6], (rocks_x-50, rocks_y-50))
            coins = current_road.coin
            if len(coins) > 0:
                coin_x = coins[0][0]
                coin_y = -player.y + current_road.y + coins[0][1] + 400
                screen.blit(spritestheme.coin_img[index_animation_coin], (coin_x-45, coin_y-45))

        if current_road.road_type == "road": # we draw the line with cars
            if road_num != 0:
                if road_num != len(current_roads)-1:
                    # if this road is in the middle of other roads
                    if current_roads[road_num-1].road_type == "road" and current_roads[road_num+1].road_type == "road":
                        screen.blit(spritestheme.road_mid_img, (0, - player.y +
                                    current_roads[road_num].y + 350))
                    # if there is only another road under it
                    elif current_roads[road_num-1].road_type == "road":
                        screen.blit(spritestheme.road_up_img, (0, - player.y +
                                    current_roads[road_num].y + 350))
                    # if there is only another road above it
                    elif current_roads[road_num+1].road_type == "road":
                        screen.blit(spritestheme.road_down_img, (0, - player.y +
                                    current_roads[road_num].y + 350))
                    # if the road is alone
                    else:
                        screen.blit(spritestheme.road_solo_img, (0, - player.y +
                                    current_roads[road_num].y + 350))
                else:
                    if current_roads[road_num-1].road_type == "road": # only roads under
                        screen.blit(spritestheme.road_up_img, (0, - player.y +
                                    current_roads[road_num].y + 350))
                    else: # road alone
                        screen.blit(spritestheme.road_solo_img, (0, - player.y +
                                    current_roads[road_num].y + 350))
            else:
                if current_roads[road_num+1].road_type == "road": # only roads above
                    screen.blit(spritestheme.road_down_img, (0, - player.y +
                                current_roads[road_num].y + 350))
                else: # road alone
                    screen.blit(spritestheme.road_solo_img, (0, - player.y +
                                current_roads[road_num].y + 350))
                    
            coins = current_road.coin
            if len(coins) > 0:
                coin_x = coins[0][0]
                coin_y = -player.y + current_road.y + coins[0][1] + 400
                screen.blit(spritestheme.coin_img[index_animation_coin], (coin_x-45, coin_y-45))

        if current_road.road_type == "water": # we draw the line and eventually lilypads
            # we check if the lilypads positions are correct
            if road_num != 0:
                generation.verify_lilypads(
                    current_roads[road_num - 1], current_road)
            if road_num != len(current_roads)-1:
                generation.verify_lilypads(
                    current_roads[road_num + 1], current_road)
    
            for lilypad_pos in current_road.lilypads:
                lilypad_x = lilypad_pos[0]
                lilypad_y = - player.y + \
                    current_roads[road_num].y + lilypad_pos[1] + 400
                screen.blit(spritestheme.lilypad_img, (lilypad_x - 50, lilypad_y - 50))

        if current_road.road_type == "rail": # we draw the line and coins
            screen.blit(spritestheme.images_background[1], (0, - player.y +
                        current_roads[road_num].y + 350))
            coins = current_road.coin
            if len(coins) > 0:
                coin_x = coins[0][0]
                coin_y = -player.y + current_road.y + coins[0][1] + 400
                screen.blit(spritestheme.coin_img[index_animation_coin], (coin_x-45, coin_y-45))


def draw_moving(player, current_roads, screen):
    """draws every moving object : car, wood and train"""
    for road in current_roads:
        if road.road_type == "road":
            for car in road.list_cars:
                if road.speed < 0:
                    screen.blit(spritestheme.car_img[car.type], (car.x-car.length/2, - player.y + road.y + 350 - 10))
                else: # we must flip the design of the car
                    screen.blit(pygame.transform.flip(spritestheme.car_img[car.type], True, False),(car.x-car.length/2, - player.y + road.y + 350 - 10))
        
        if road.road_type == "water":
            for raft in road.list_cars:
                screen.blit(spritestheme.raft_img[raft.length], (raft.x-raft.length/2, - player.y + road.y + 350))

        if road.road_type == "rail":
            for train in road.list_cars:
                if road.speed > 0:
                    screen.blit(spritestheme.train_img, (train.x-train.length /2, - player.y + road.y + 350-70))
                else:
                    screen.blit(pygame.transform.flip(spritestheme.train_img, True, False),(train.x-train.length/2, - player.y + road.y + 350-70))
            if animation.traffic_light(road) == "green":
                screen.blit(spritestheme.traffic_green, (600 - 550*road.speed /
                            abs(road.speed), - player.y + road.y + 350))
            else:
                screen.blit(spritestheme.traffic_red, (600 - 550*road.speed /
                            abs(road.speed), - player.y + road.y + 350))


def movement_character(moving, move_direction, index_animation, x, y, screen):
    """draws the player, creating an animation if he is moving"""
    if moving:
        image_actuelle = spritestheme.images_skin[move_direction][index_animation]
    else:
        image_actuelle = spritestheme.images_skin[f"idle_{move_direction}"][0]
    screen.blit(image_actuelle, (x, y))


def animation_water(index_animation, y, screen):
    """animates water"""
    image_actuelle = spritestheme.images_river[index_animation]
    screen.blit(image_actuelle, (0, y))


def death_animation(x,y,screen, death_type):
    """The player can get hit by a vehicle or drown in the water"""
    if death_type == "road":
        screen.blit(spritestheme.blood_img, (x,y))
    else:
        screen.blit(spritestheme.drop_img, (x-10,y))