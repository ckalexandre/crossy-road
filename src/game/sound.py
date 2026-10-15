import pygame
from src.paths import asset_path
pygame.mixer.init()

coinsound = pygame.mixer.Sound(asset_path("Music", "coin_sound.wav"))
walksound =pygame.mixer.Sound(asset_path("Music", "walk_sound.wav"))
coinsound.set_volume(0.6)
walksound.set_volume(1)

def coin_sound():
    coinsound.play()

def walk_sound():
    walksound.play()