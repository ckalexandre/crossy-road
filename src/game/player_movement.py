def movement_in_water(player, coord_init, current_roads, player_line, dt):
    """If the player is on the wood, he moves with it on the water"""
    if coord_init[0] + 100 > player.x > coord_init[0] - 100: # as long as his movement (with the arrows) isn't over
        player.x += current_roads[player_line].speed * dt
        if player.x < coord_init[0] - 100: 
            player.x = coord_init[0] - 100 # if he theoretically went further than his 100 pixels movement from his starting position, he stops at 100 pixels
            coord_init[0] -= 100 # we actualize his initial coordonates for a future movement
        elif player.x > coord_init[0] + 100:
            player.x = coord_init[0] + 100
            coord_init[0] += 100
    return player, coord_init


def vertical_deplacement_check(d, current_roads, player, player_line):
    """checks if the player can move up or down"""
    moving = True
    if current_roads[player_line].road_type == "water" and current_roads[player_line].lilypads == []: # on a line of wood
        if (player.x-50) % 100 != 0:
            player.x = round((player.x-50)/100)*100 + 50 # we replace the player on the closest square of the grid
    if current_roads[player_line + d].road_type == "grass": # his movement can be blocked by trees and rocks
        for rock in current_roads[player_line + d].rocks:
            if rock[0] == player.x:
                moving = False
        for tree in current_roads[player_line + d].trees:
            if tree[0] == player.x:
                moving = False
    return moving

def horizontal_deplacement_check(d, current_roads, player, player_line, moving):
    """checks if the player can move to the left or to the right"""
    if current_roads[player_line].road_type == "grass": # his movement can be blocked by trees and rocks
        for rock in current_roads[player_line].rocks:
            if rock[0] == player.x + d*100:
                moving = False
        for tree in current_roads[player_line].trees:
            if tree[0] == player.x + d*100:
                moving = False
    return moving

def horizontal_deplacement_on_water_check(d, current_roads, player, player_line):
    """returns necessary informations to move horizontally on a wood in the water"""
    deplacement_on_boat = False
    init_place_on_boat = 0
    move_direction = "up" # this parameter will not be changed in the function only if we die (it just prevents errors)
    wood_we_are_moving_on_x = 0
    wood_speed = 0
    for wood in current_roads[player_line].list_cars:
        if wood.x - wood.length/2 <= player.x <= wood.x + wood.length/2: # we are on a wood
            deplacement_on_boat = True
            init_place_on_boat = player.x - wood.x
            if d == -1:
                move_direction = "left"
            if d == 1:
                move_direction = "right"
            wood_we_are_moving_on_x = wood.x
            wood_speed = current_roads[player_line].speed
    return deplacement_on_boat, init_place_on_boat, move_direction, wood_we_are_moving_on_x, wood_speed

def vertical_deplacement(d, player, coord_init, dt):
    """moves the player vertically"""
    moving = True
    if d*player.y > d*coord_init[1] - 100: # If the player hasn't yet reached the end of his move (a move = 100px)
        player.y -= d*400*dt
        if d*player.y < d*coord_init[1] - 100: # Without that "if", the move may exceed 100px, because we don't add 1 px at a time
            player.y = coord_init[1] - d*100
    else:
        moving = False # the movement is over
        coord_init[1] = player.y
    return player, coord_init, moving

def horizontal_deplacement(d, player, coord_init, dt, deplacement_on_boat, wood_we_are_moving_on_x, init_place_on_boat, wood_speed):
    """moves the player horizontally, and adjusts if the player is on a wood"""
    moving = True
    if not deplacement_on_boat: # not on a wood
        if d*player.x < d*coord_init[0] + 100:
            player.x += d*400*dt
            if d*player.x > d*coord_init[0] + 100:
                player.x = coord_init[0] + d*100
        else:
            moving = False
            coord_init[0] = player.x
    else: # on a wood
        ecart = player.x - wood_we_are_moving_on_x
        if d == 1: # right
            if ecart < init_place_on_boat + 100:
                player.x += (400 + abs(wood_speed))*dt # the movement is considered in the reference system of the wood
                wood_we_are_moving_on_x += wood_speed*dt
                ecart = player.x - wood_we_are_moving_on_x
                if ecart > init_place_on_boat + 100:
                    player.x = wood_we_are_moving_on_x + init_place_on_boat + 100
                    moving = False
                    deplacement_on_boat = False
                    coord_init[0] = player.x
            else:
                moving = False
                deplacement_on_boat = False
                coord_init[0] = player.x
        else: # left
            if ecart > init_place_on_boat - 100:
                player.x -= (400 + abs(wood_speed))*dt
                wood_we_are_moving_on_x += wood_speed*dt
                ecart = player.x - wood_we_are_moving_on_x
                if ecart < init_place_on_boat - 100:
                    player.x = wood_we_are_moving_on_x + init_place_on_boat - 100
                    moving = False
                    deplacement_on_boat = False
                    coord_init[0] = player.x
            else:
                moving = False
                deplacement_on_boat = False
                coord_init[0] = player.x

    return player, coord_init, moving, deplacement_on_boat, wood_we_are_moving_on_x