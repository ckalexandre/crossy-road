import time
import random
from math import sqrt

from src.game import objects
from src.game import spawn


def generate_roads(y, imposed_type, last_type):
    """generates between 1 and 4 roads of a random type (if imposed_type is None) or else of the given type, which must be different from the last type"""
    if imposed_type == "None":
        road_type = last_type
        while road_type == last_type: # we keep generating as long as the new type of road is the same as the last type in current_roads
            road_type = random.randint(1, 6) # we generate a random road type
            dico_road_type = {1: ['grass', 1, 2], 2: [
                'road', 1, 5], 3: ['water', 2, 3], 4: ['rail', 1, 2], 5: ['grass', 1, 2], 6: ['grass', 1, 2], 7: ['road', 1, 5]}
                # we indicate how many roads from any given type can form a block
                # several times road and grass because we often want grass after a dangerous path and want more roads than water and rail
            list_road_type = dico_road_type[road_type]
            road_type = list_road_type[0]
            axes = random.randint(list_road_type[1], list_road_type[2])

    else:
        road_type = imposed_type
        axes = random.randint(1, 5)
    lines = []
    for i in range(axes):
        d = random.choice([1, -1])
        if road_type == "water":
            speed = random.randint(100, max(150,sqrt(abs(y))/5)) # y is used so that the speed of the obstacles increases if we go far enough
        elif road_type == "rail":
            speed = random.randint(1000, max(2000, sqrt(abs(y))/5))
        elif road_type == "road":
            speed = random.randint(100, max(400, sqrt(abs(y))))
        else: #
            speed = 0
        lines += [objects.Line(y - i*100, d *
                               speed, road_type, [], 0, 0, 0, 0)] # Line speed parameter is positive if objects move from left to right, and negative otherwise
    return lines


def verify_lilypads(previous_line, water_line):
    """generates new lilypads if they're blocked by obstacles from the previous line (so that wa can't go on them)"""
    if previous_line.road_type == "grass": # only trees and rocks (so on the grass) can block the path
        occupied_positions = [
            tree[0] for tree in previous_line.trees] + [rock[0] for rock in previous_line.rocks] # x positions of the obstacles
        x = [250, 350, 450, 550, 650, 750, 850, 950, 1050] # possible lilypad's position (not on the edges)

        verified = True
        for lilypad in water_line.lilypads:
            if lilypad[0] in occupied_positions:
                verified = False # if one lilypad isn't accessible, we generate again

        if not verified:
            new_list = []
            l = len(water_line.lilypads)
            for _ in range(l):
                available_positions = [
                    pos for pos in x if pos not in occupied_positions] # where we can generate the new lilypads
                if available_positions:
                    new_position = random.choice(available_positions)
                    new_list.append((new_position, 0))

            water_line.lilypads = new_list.copy() # we remplace the old lilypads positions by the new positions


def add_moving_on_lines(current_roads, next_spawn_roads):
    """generate cars, trains and wood on lines"""
    for i in range(len(current_roads)):
        road = current_roads[i]
        if road.road_type == "road" and time.time() > next_spawn_roads[i]: #cars
            vehicle_length = 120
            road.list_cars.append(spawn.spawn_cars(road, vehicle_length))
            next_spawn_roads[i] = time.time() + 3*random.random() + 300/abs(road.speed) 
                # next generation is later if the speed of the road is lower

        if road.road_type == "water" and road.lilypads == [] and time.time() > next_spawn_roads[i]: # wood
            wood_length = random.choice([300, 400, 500])
            road.list_cars.append(spawn.spawn_wood(road, wood_length))
            next_spawn_roads[i] = time.time() + 2*random.random() + 300/abs(road.speed)
        
        if road.road_type == "rail" and time.time() > next_spawn_roads[i]: # trains
            vehicle_length = 1500
            road.list_cars.append(spawn.spawn_cars(road, vehicle_length))
            next_spawn_roads[i] = time.time() + 10*random.random() + 5


def init_lines(current_roads, next_spawn_roads):
    """initialize 5 grass lines in the beginning"""
    first_grass_line = objects.Line(300 - 10, 0, "grass", [], 0, 0, 0, 0)
    first_grass_line.rocks = []
    first_grass_line.trees = [(50, 0,random.randint(8,9)), (150, 0,random.randint(8,9)), (250, 0,random.randint(8,9)), (350, 0,random.randint(8,9)), (450, 0,random.randint(8,9)), (
        550, 0,random.randint(8,9)), (650, 0,random.randint(8,9)), (750, 0,random.randint(8,9)), (850, 0,random.randint(8,9)), (950, 0,random.randint(8,9)), (1050, 0,random.randint(8,9)), (1150, 0,random.randint(8,9)), (1250, 0,random.randint(8,9))]
        # we generate trees on the entire first line, to show that we can't go back
    first_grass_line.coin = []
    current_roads += [first_grass_line]
    for i in range(1, 5): # we generate the next 4 lines
        grass_line = objects.Line(300-i*100 - 10, 0, "grass", [], 0, 0, 0, 0)
        current_roads += [grass_line]
        next_spawn_roads.append(None) # there will be no spawn of moving obstacles on the grass


def delete_old_line(player, current_roads, next_spawn_roads, player_line):
    """deletes the lines which are too far behind the player, to avoid dealing with too many objects"""
    for i in range(len(current_roads)-1, -1, -1): # we begin with the end of the list, in order not to disturb the indexation while we remove elements from the lists
        road = current_roads[i]
        if road.y > player.y + 650: # the road is far behind the player
            current_roads.remove(road)
            next_spawn_roads.remove(next_spawn_roads[i]) # the times in next_spawn_road are linked to a specific road, and must disappear with it
            return player_line - 1 # because we deleted a line, the road from the list on which the player stands is on the lower index
    return player_line


def add_lines(player, current_roads, next_spawn_roads):
    """generates new lines in front of the player if he gets too close from the last generated line"""
    if player.y < current_roads[-1].y + 800:
        current_roads += generate_roads(
            current_roads[-1].y - 100, "None", current_roads[-1].road_type) # we add a new block of roads
    for i in range(len(next_spawn_roads), len(current_roads)): # we add a position in next_spawn_road for each new created line
        if current_roads[i].road_type in ("road", "water","rail"):
            next_spawn_roads.append(time.time())
        else: # no moving object on the grass
            next_spawn_roads.append(None)
