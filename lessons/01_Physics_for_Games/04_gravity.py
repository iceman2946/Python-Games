"""
Implementing Gravity

This program will demonstrate a simple implementation of gravity in a game, 
the the player constantly jumping. Notice that using gravity makes the player
jump more realistic. The player goes up quickly, but falls slowly. 

"""
import pygame
from dataclasses import dataclass

# Initialize Pygame
pygame.init()


# This is a data class, one way of storing settings and constants for a game.
# We will create an instance of the data class, but since there is only one of
# them, we could also use the class directly, like GameSettings.screen_width.
# You can check that the instance has the same values as the class:
#    settings = GameSettings()
#    assert GameSettings.screen_width == settings.screen_width
@dataclass
class GameSettings:
    """Class for keeping track of game settings."""
    screen_width: int = 500
    screen_height: int = 500
    player_size: int = 10
    player_x: int = 100 # Initial x position of the player
   
    jump_velocity: int = 200
    white: tuple = (255, 255, 255)
    black: tuple = (0, 0, 0)

    gravity: float = 60.0 # acceleration, the change in velocity per frame
    d_t: float = 1.0/30
    m: float = 2.0 # mass of the player, used to calculate acceleration

# Initialize game settings
settings = GameSettings()


# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

# Define player
player = pygame.Rect(settings.player_x, 
                     settings.screen_height - settings.player_size, 
                     settings.player_size, settings.player_size)

is_jumping = False

# Main game loop
running = True
clock = pygame.time.Clock()
d_v_y=0 
while running:

    # Handle events, such as quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Continuously jump. If the player is not jumping, initialize a new jump
    if is_jumping is False:
        keys = pygame.key.get_pressed()
        # Jumping means that the player is going up. The top of the 
        # screen is y=0, and the bottom is y=SCREEN_HEIGHT. So, to go up,
        # we need to have a negative y velocity
        if keys[pygame.K_SPACE] and keys[pygame.K_LSHIFT]:
            print("Jump")
            is_jumping = True
            #jump_velocity+=150
            d_v_y= -settings.jump_velocity - 1000
        if keys[pygame.K_SPACE]:
            is_jumping = True
            d_v_y = -settings.jump_velocity

    # acelleration in sht y direction
    a_y = settings.gravity

    # Change in the velocity due to accelleration
    d_v_y += a_y * settings.d_t

    # Change in the position due to the velocity
    d_y = d_v_y * settings.d_t

    player.y += d_y

    # If the player hits the ground, stop the player from falling.
    # The player's position is measured from the top left corner, so the
    # bottom of the player is player.y + PLAYER_SIZE. If the bottom of the
    # player is greater than the height of the screen, the player is on the
    # ground. So, set the player's y position to the bottom of the screen
    # and stop the player from falling
    if player.bottom >= settings.screen_height:
        player.bottom = settings.screen_height 
        jump_velocity = 200; 
        d_v_y = 0 
        is_jumping = False

    # Draw everything
    screen.fill(settings.white)
    pygame.draw.rect(screen, settings.black, player)

    pygame.display.flip()
    clock.tick( int(1/settings.d_t))

pygame.quit()
