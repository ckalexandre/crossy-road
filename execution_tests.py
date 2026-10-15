from tests import tests

# Tests of functions of generation
print('============= Tests des fonctions de generation.py ============')
tests.test_generate_roads()
tests.test_delete_old_lines()

# Tests of functions of spawn
print('=============== Tests des fonctions de spawn.py ===============')
tests.test_spawn_cars()
tests.test_spawn_wood()

# Tests of functions of player_movement
print('========== Tests des fonctions de player_movement.py ==========')
tests.test_movement_in_water()
tests.test_horizontal_deplacement_on_water_check()

# Tests of functions of collision
print('============= Tests des fonctions de collision.py =============')
tests.test_collision()
tests.test_collision_in_water()
tests.test_catch_coin()