from src.game import constants


def collision(obstacle, player):
    """Check if the player is hit by a vehicle"""
    if obstacle.x - obstacle.length/2 <= player.x + player.width/2 and obstacle.x + obstacle.length/2 >= player.x - player.width/2:
        return True
    return False


def collision_in_water(water, player, moving):
    """Check if the player is safe in water (on a lilypad or on a wood)"""
    if water.lilypads != []: # there are lilypads on this line
        if moving: # the last movement isn't over, so we don't check yet if the player is on a lilypad
            return True
        for lily in water.lilypads:
            if player.x == lily[0]: # the player is immobile → he only stays alive if he is exactly on a lilypad
                return True
        return False

    else: # line of wood
        if player.x < 0 or player.x > constants.SCREEN_WIDTH: # if he went out of the screen (because he stayed on a wood for too long)
            return False
        for wood in water.list_cars:
            if wood.x - wood.length/2 <= player.x <= wood.x + wood.length/2: # we consider that he is on the wood if its center is
                return True
        return False

def catch_coin(coin, player) :
    """Check if the player can collect a coin"""
    if coin[0] == player.x and coin[1] == 0 : # the coin must be on the same line as the player
        return True
    return False
