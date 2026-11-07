"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path

# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

# Screen dimensions
class Settings: 
    WIDTH, HEIGHT = 600, 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dino Jump")

    # Colors
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # FPS
    FPS = 60

    # Player attributes
    PLAYER_SIZE = 25

    player_speed = 5

    # Obstacle attributes
    OBSTACLE_WIDTH = 20
    OBSTACLE_HEIGHT = 20
    obstacle_speed = 5

# Font
font = pygame.font.SysFont(None, 36)


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    exploded = False
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load(images_dir / "cactus_9.png")
        self.image = pygame.transform.scale(self.image,(Settings.OBSTACLE_WIDTH,Settings.OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.WIDTH
        self.rect.y = Settings.HEIGHT - Settings.OBSTACLE_HEIGHT - 10
        self.player = player
        self.explosion = pygame.image.load(images_dir / "explosion1.gif")
       


    def update(self):  
        self.rect.x -= Settings.obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.exploded :
            return
        
        if self.rect.right < 0:
            self.kill()
            player.score +=1

        
    
    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image.    
        
        self.image = self.explosion 
        self.image = pygame.transform.scale(self.image, (Settings.OBSTACLE_WIDTH, Settings.OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.exploded = True

         



# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image =pygame.image.load(images_dir/"dino_0.png")
        self.image = pygame.transform.scale(self.image,(Settings.PLAYER_SIZE,Settings.PLAYER_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = Settings.HEIGHT - Settings.PLAYER_SIZE - 10
        self.speed = Settings.player_speed
        self.jump_velocity = 0
        self.space_was_down = False
        self.hitbyObstacle= False
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        floor_y = Settings.HEIGHT - 10
        space_down = keys[pygame.K_SPACE]

        if space_down and not self.space_was_down and self.rect.bottom == floor_y:
            self.jump_velocity = -12

        self.space_was_down = space_down
        self.jump_velocity += 1
        self.rect.y += self.jump_velocity

        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.jump_velocity = 0
        # Keep the player on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Settings.HEIGHT:
            self.rect.bottom = Settings.HEIGHT


# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)

# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    
    if random.random() < 0.4:
        obstacle = Obstacle(player)
        obstacles.add(obstacle)
        return 1
    return 0


# Main game loop
class Game:
    def __init__(self):
        self.restart_button = pygame.Rect(220, 170, 160, 50)

    def reset(self):
        global player
        player = Player()

    def game_loop(self):
        clock = pygame.time.Clock()
        game_over = False
        last_obstacle_time = pygame.time.get_ticks()

        # Group for obstacles
        obstacles = pygame.sprite.Group()
        obstacle_count = 0
        was_colliding = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.restart_button.collidepoint(event.pos):
                        self.reset()
                        game_over = False
                        obstacles = pygame.sprite.Group()
                        obstacle_count = 0
                        last_obstacle_time = pygame.time.get_ticks()
                        was_colliding = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.reset()
                        game_over = False
                        obstacles = pygame.sprite.Group()
                        obstacle_count = 0
                        last_obstacle_time = pygame.time.get_ticks()
                        was_colliding = False

            if not game_over:
                # Update player
                player.update()

                # Add obstacles and update
                if pygame.time.get_ticks() - last_obstacle_time > 500:
                    last_obstacle_time = pygame.time.get_ticks()
                    obstacle_count += add_obstacle(obstacles)

                obstacles.update()

                # Check for collisions
                collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
                is_colliding = bool(collider)
                if is_colliding and not was_colliding:
                    collider[0].explode()
                    game_over = True
                    was_colliding = True
                elif not is_colliding:
                    was_colliding = False

            # Draw everything
            Settings.screen.fill(Settings.WHITE)
            Settings.screen.blit(player.image, player.rect)
            obstacles.draw(Settings.screen)

            if not game_over:
                obstacle_text = font.render(f"Obstacles: {obstacle_count}", True, Settings.BLACK)
                score_text = font.render(f"Score: {player.score}", True, Settings.BLACK)
                Settings.screen.blit(obstacle_text, (10, 10))
                Settings.screen.blit(score_text, (10,40))
            else:
                gameDone_text = font.render("GAME OVER", True, Settings.BLACK)
                Settings.screen.blit(gameDone_text, (220, 120))
                pygame.draw.rect(Settings.screen, Settings.BLUE, self.restart_button)
                restart_text = font.render("Restart", True, Settings.WHITE)
                Settings.screen.blit(restart_text, (self.restart_button.x + 30, self.restart_button.y + 10))

            pygame.display.update()
            clock.tick(Settings.FPS)

if __name__ == "__main__":
    game = Game()
    game.game_loop()
