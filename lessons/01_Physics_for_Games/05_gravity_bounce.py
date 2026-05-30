"""
Gravity bounce with x motion

If we add X velocity, from side to side, the player will bounce around the
screen. We will need to add a check to see if the player hits the left or right
side of the screen.

"""
import pygame
from dataclasses import dataclass

@dataclass
class GameSettings:
    """Class for keeping track of game settings and constants."""
    screen_width: int = 500
    screen_height: int = 500
    square_size: int = 20
    square_color: tuple = (0, 0, 0)  # Black
    background_color: tuple = (255, 255, 255)  # White
    fps: int = 30
    gravity: float = 60.0  # Acceleration due to gravity
    jump_velocity_y: float = 200.0  # Initial jump velocity in y direction
    jump_velocity_x: float = 100.0  # Initial jump velocity in x direction
    d_t: float = 1.0/30  # Time step for physics calculations

# Initialize Pygame
pygame.init()

# Initialize game settings
settings = GameSettings()

# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Gravity Bounce")

# Square starting position
x_pos = 100
y_pos = settings.screen_height - settings.square_size

# Initial velocities  
velocity_x = 0
velocity_y = 0
x_direction = 1  # Either 1 or -1, to keep track of direction after hitting the ground

is_jumping = False

# Main loop
running = True
clock = pygame.time.Clock()

while running:

    # Handle events, such as quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Continuously jump. If the square is not jumping, make it jump
    if is_jumping is False:
        keys = pygame.key.get_pressed()
        # Jumping means that the square is going up. The top of the 
        # screen is y=0, and the bottom is y=screen_height. So, to go up,
        # we need to have a negative y velocity
        if keys[pygame.K_SPACE]:
            velocity_y = -settings.jump_velocity_y
            velocity_x = settings.jump_velocity_x * x_direction 
            is_jumping = True
        
    else: # the square is jumping
        # Update square position. Gravity is always pulling the square down,
        # which is the positive y direction, so we add settings.gravity to the y velocity
        # to make the square go up more slowly. Eventually, the square will have
        # a positive y velocity, and gravity will pull the square down.

        velocity_y += settings.gravity * settings.d_t
        
        # Update the position with the velocity. Like with the velocity, we change
        # the position by adding the velocity, not setting it to the velocity, and
        # we change it a bit each frame.
        y_pos += velocity_y * settings.d_t
        x_pos += velocity_x * settings.d_t
        
    # If the square hits one side of the screen or the other, bounce the square
    if x_pos <= 0 or x_pos + settings.square_size >= settings.screen_width:
        velocity_x = -velocity_x
        
        # Update direction tracking
        x_direction = -x_direction 
        # This way is more reliable, since it will always be 1 or -1 and direction is tied to velocity
        if velocity_x != 0:
            x_direction = int(velocity_x / abs(velocity_x))

    # If the square hits the top of the screen, bounce the square
    if y_pos <= 0:
        velocity_y = -velocity_y

    # If the square hits the ground, stop the square from falling.
    if y_pos + settings.square_size > settings.screen_height:
        y_pos = settings.screen_height - settings.square_size
        velocity_y = 0
        velocity_x = 0
        is_jumping = False

    # Fill the screen with background color (clears previous frame)
    screen.fill(settings.background_color)

    # Draw the square
    pygame.draw.rect(screen, settings.square_color, (x_pos, y_pos, settings.square_size, settings.square_size))

    # Update the display
    pygame.display.flip()

    # Frame rate control
    clock.tick(settings.fps)

pygame.quit()
