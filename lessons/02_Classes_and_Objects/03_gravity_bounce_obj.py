"""
Gravity bounce in Object Oriented style

This version of the gravity bounce program uses an object oriented style to
organize the code. The main game loop is in the Game class, and the player is
a separate class. This makes the code easier to read and understand, and
allows for more complex games with multiple objects.

## Assignment 5

1. Open `03_gravity_bounce_obj.py` 
2. Review the program and try to understand how it works.
3. Change the program so that the player's initial velocity and position are set
   in the initializer to the `Player` class. 
4. Add a color for the player, configurable in the initializer.
5. Add a second player to the game. The second player should be a different
   color and have different initial position and velocity.

When you are done, your program should have two player objects ( but only one
Player class!), of different colors, bouncing around in different trajectories. 

"""
import pygame


class Colors():
    """Constants for Colors"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)


class GameSettings:
    """Settings for the game"""
    width: int = 500
    height: int = 500
    player_width: int = 20
    player_height: int = 20

    player_start_x: int = 100
    player_start_y: int = None

    gravity: float = 200
    v_0_y: float = 0  # Initial y velocity
    v_0_x: float = 75 # Initial x velocity

    jump_v_y: float = 400

    FPS = 30
    d_t = 1 / FPS # Time step


class Game:
    """Main object for the top level of the game. Holds the main loop and other
    update, drawing and collision methods that operate on multiple other
    objects, like the player and obstacles."""
    
    def __init__(self, settings: GameSettings):
        pygame.init()

        self.settings = settings
        self.running = True

        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.clock = pygame.time.Clock()

        self.players = []

    def add_player(self, player):
        self.players.append(player)


    def run(self):
        """Main game loop"""

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            self.screen.fill(Colors.WHITE)

            for player in self.players:
                player.update()
                player.draw(self.screen)
                
            pygame.display.flip()
            self.clock.tick(self.settings.FPS)

        pygame.quit()


class Player:
    """Player class, just a bouncing rectangle"""

    def __init__(self, game: Game,x:int,y:int,v_x:int,v_y,color:tuple):
        self.game = game
        settings = game.settings

        self.width = settings.player_width
        self.height = settings.player_height
      
        self.is_jumping = False
        self.v_jump = settings.jump_v_y

        self.y = y #settings.player_start_y if settings.player_start_y is not None else settings.height - self.height
        self.x = x #settings.player_start_x
        
        self.v_x = v_x#settings.v_0_x  # X Velocity
        self.v_y = v_y#settings.v_0_y  # Y Velocity

        self.color = color

    def update(self):
        """Update player position, continuously jumping"""
        self.update_jump()
        self.update_y()
        self.update_x()

    def update_y(self):
        """Update the player's y position based on gravity and velocity"""
        self.v_y += self.game.settings.gravity * self.game.settings.d_t # Add gravity to the y velocity
        self.y += self.v_y * self.game.settings.d_t # Update the player's y position, based on the current velocity

        if self.y >= self.game.settings.height - self.height:
            self.y = self.game.settings.height - self.height
            self.v_y = 0
            self.is_jumping = False

    def update_x(self):
        """Update the player's x position based on horizontal velocity and bounce on edges"""
        self.x += self.v_x * self.game.settings.d_t  # Update the player's x position based on the current velocity

        if self.x <= 0:
            self.x = 0
            self.v_x = -self.v_x
        elif self.x >= self.game.settings.width - self.width:
            self.x = self.game.settings.width - self.width
            self.v_x = -self.v_x

    def update_jump(self):
        """Handle the player's jumping logic"""
        
        if not self.is_jumping:
            self.v_y = -self.v_jump
            self.is_jumping = True

    def draw(self, screen):
        pygame.draw.rect(screen, Colors.BLACK, (self.x, self.y, self.width, self.height))


settings = GameSettings()
game = Game(settings)

p1 = Player(
    game,
    settings.player_start_x,
    settings.player_start_y,
    settings.v_0_x,
    settings.v_0_y,
    (255,0,0)
    )
p2 = Player(
    game,
    settings.player_start_x+30,
    settings.player_start_y,
    settings.v_0_x+30,
    settings.v_0_y+30,
    (0,0,0)
)
game.add_player(p1)


game.run()
