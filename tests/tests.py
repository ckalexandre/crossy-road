from src.game import objects
from src.game import generation
from src.game import spawn
from src.game import player_movement
from src.game import collision

# ===================== Tests of functions from generation =====================

def test_generate_roads() :
    """Tests the generation of lines"""
    set_of_roads = generation.generate_roads(0,None, "road")
    assert 1<=len(set_of_roads)<=5
    assert set_of_roads[0].y == 0
    if len(set_of_roads)>1:
        assert set_of_roads[0].road_type == set_of_roads[1].road_type
    print('Test de generate_roads concluant.')

def test_delete_old_lines() :
    """Tests the removal of old lines"""
    player_test = objects.Player(0,0)
    line_test = objects.Line(651, 200, "road", [], [], [], [], [])
    results = generation.delete_old_line(player_test, [line_test], [None], 0)
    assert results == -1
    print('Test de delete_old_lines concluant.')

# ======================= Tests of functions from spawn =======================

def test_spawn_cars() :
    """Test the spawn of cars"""
    road = objects.Line(651, 200, "road", [], [], [], [], [])
    vehicle_length = 200
    direction = road.speed / abs(road.speed)
    x = 650 - direction * (650 + vehicle_length/2)
    results = spawn.spawn_cars(road, vehicle_length)
    assert (results.x == x and results.y == road.y and results.length == vehicle_length and results.color == (255, 0, 0))
    print('Test de spawn_cars concluant.')

def test_spawn_wood() :
    """Tests the spawn of wood"""
    # When direction = +1
    river = objects.Line(60, 100, 'water', [], [], [], [], [])
    result = spawn.spawn_wood(river, 400)
    assert (result.x == -400 and result.y == 60 and result.length == 400)
    # When direction = -1
    river.speed = -100
    result = spawn.spawn_wood(river, 200)
    assert (result.x == 1500 and result.y == 60 and result.length == 200)
    print('Test de spawn_wood concluant.')


# ================== Tests of functions from player_movement ==================

def test_movement_in_water() :
    """Test the movement on water"""
    player = objects.Player(300, 60)
    coord_init = [350, 60]
    wood1 = objects.Wood(250, 0, 100, 200)
    wood2 = objects.Wood(1050, 0, 100, 400)
    river = objects.Line(60, 100, 'water', [wood1, wood2], [], [], [], [])
    current_roads = [river]
    player_line = 0
    dt = 1
    result1_player, result1_coord_init = player_movement.movement_in_water(player, coord_init, current_roads, player_line, dt)
    assert (result1_player.x == 400 and result1_coord_init[0] == 350)
    player.x = 400
    result2_player, result2_coord_init = player_movement.movement_in_water(player, coord_init, current_roads, player_line, dt)
    assert (result2_player.x == 450 and result2_coord_init[0] == 450)
    river.speed = -100
    player.x = 300
    coord_init = [350, 60]
    result3_player, result3_coord_init = player_movement.movement_in_water(player, coord_init, current_roads, player_line, dt)
    assert (result3_player.x == 250 and result3_coord_init[0] == 250)
    print('Test de movement_in_water concluant.')

def test_horizontal_deplacement_on_water_check() :
    """Tests the check of the horizontal deplacement when on a wood"""
    d = 1
    wood1 = objects.Wood(250, 0, 100, 200)
    wood2 = objects.Wood(1050, 0, 100, 400)
    river = objects.Line(60, 200, 'water', [wood1, wood2], [], [], [], [])
    current_roads = [river]
    player = objects.Player(1150, 60)
    player_line = 0
    result_dpt_on_wood, result_plc_on_wood, result_move_dir, result_which_wood_x, result_speed = player_movement.horizontal_deplacement_on_water_check(d, current_roads, player, player_line)
    assert (result_dpt_on_wood == True and result_plc_on_wood == 100 and result_move_dir == 'right' and result_which_wood_x == 1050 and result_speed == 200)
    print('Test de horizontal_deplacement_on_water_check concluant.')

# ====================== Tests of functions from collision ======================

def test_collision() :
    """Tests the collisions"""
    player = objects.Player(550, 100)
    obstacles = [objects.Vehicle(x, 100, 200, (100,100,100), 0) for x in range(100, 1300, 50)]
    results = [collision.collision(obstacle, player) for obstacle in obstacles]
    assert results == [False]*6 + [True]*7 + [False]*11
    print("Test de collision concluant.")

def test_collision_in_water() :
    """Tests if the collision is detected in the water"""

    # water line with lilypads
    water = objects.Line(60, 0, 'water', [], [], [], [], [])
    player = objects.Player(350, 60)
    moving = False
    water.lilypads = [(250, 0), (550, 0)]
    assert collision.collision_in_water(water, player, moving) == False
    moving = True
    assert collision.collision_in_water(water, player, moving) == True
    
    # water line with wood with player inside the screen
    radeau1 = objects.Wood(250, 0, 100, 200)
    radeau2 = objects.Wood(1050, 0, 100, 400)
    water.lilypads = []
    water.list_cars = [radeau1, radeau2]
    assert collision.collision_in_water(water, player, moving) == True
    player.x = 550
    assert collision.collision_in_water(water, player, moving) == False
    
    # water line with wood with player outside the screen
    player.x = -6
    assert collision.collision_in_water(water, player, moving) == False
    player.x = 1500
    assert collision.collision_in_water(water, player, moving) == False
    
    print('Test de collision_in_water concluant.')

def test_catch_coin() :
    """Tests the catch of a coin"""
    coin = (250, 0)
    player = objects.Player(350, 60)
    assert collision.catch_coin(coin, player) == False
    coin = (350, 0)
    assert collision.catch_coin(coin, player) == True
    coin = (350, 60)
    assert collision.catch_coin(coin, player) == False
    print('Test de catch_coin concluant.')
