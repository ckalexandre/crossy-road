import random

from src.game import objects


def spawn_cars(road, vehicle_length):
    """generates a vehicle of a certain lenth on a road"""
    direction = road.speed / abs(road.speed)
    x = 650 - direction * (650 + vehicle_length/2) # spawn at the end of the line
    if road.road_type == "rail":
        x = 650 - direction * (5000 + vehicle_length/2) # spawn further for a train (traffic light system)
    return objects.Vehicle(x, road.y, vehicle_length, (255, 0, 0), random.randint(0, 22))


def spawn_wood(river, wood_length):
    """generates a wood of a certain length on a river"""
    direction = river.speed / abs(river.speed)
    x = 650 - direction * (650 + wood_length) # spawn at the end of the line
    return objects.Wood(x, river.y, objects.side, wood_length)
