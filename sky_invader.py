import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sky Invader")

# Set up the font
font = pygame.font.SysFont("Arial", 24)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed_x = 0

    def update(self, keys):
        self.speed_x = 0
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 5)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Initialize player and enemies
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game variables
score = 0
lives = 3

# Game loop
running = True
clock = pygame.time.Clock()

while running: 
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update game
    keys = pygame.key.get_pressed()
    player.update(keys)
    enemies.update()
    bullets.update()

    # Check for bullet-enemy collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for enemy-player collisions
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        lives -= 1
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        if lives <= 0:
            running = False

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

    # Flip the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
game_over_text = font.render("Game Over", True, WHITE)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + final_score_text.get_height()))
pygame.display.flip()

# Wait for a few seconds before closing
pygame.time.wait(3000)

pygame.quit()
