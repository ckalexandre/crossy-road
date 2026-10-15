import pygame

def traffic_light(rail):
    """determines if the traffic light is red (train is comming) or green (no train)"""
    for train in rail.list_cars:
        if (rail.speed < 0 and -1000 <= train.x <= -rail.speed * 2) or (rail.speed > 0 and -rail.speed * 2 <= train.x <= 2300): 
            return "red"
    return "green"


