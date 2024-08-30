import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 768
TT_WIDTH = 100
COIN_WIDTH = 50
POWERUP_WIDTH = 50
INITIAL_SPEED = 5
POWERUP_DURATION = 300  # Frames (about 5 seconds at 60 FPS)

# Initialize pygame
pygame.init()

class Player:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TT_WIDTH, self._get_scaled_height()))
        self.flipped = False
        self.x = (SCREEN_WIDTH - self.image.get_width()) // 2
        self.y = SCREEN_HEIGHT - self.image.get_height() - 50
        self.speed = INITIAL_SPEED
        self.boosted = False
        self.boost_timer = 0

    def _get_scaled_height(self):
        return int(self.image.get_height() * (TT_WIDTH / self.image.get_width()))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            if not self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = True

        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = False

        self._check_boundaries()

        if self.boosted:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.speed = INITIAL_SPEED
                self.boosted = False

    def _check_boundaries(self):
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.image.get_width():
            self.x = SCREEN_WIDTH - self.image.get_width()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

    def activate_powerup(self):
        self.speed = INITIAL_SPEED * 2
        self.boosted = True
        self.boost_timer = POWERUP_DURATION


class Coin:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (COIN_WIDTH, self._get_scaled_height()))
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = SCREEN_HEIGHT - self.image.get_height() - 60

    def _get_scaled_height(self):
        return int(self.image.get_height() * (COIN_WIDTH / self.image.get_width()))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def reset_position(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))


class PowerUp:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (POWERUP_WIDTH, self._get_scaled_height()))
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = SCREEN_HEIGHT - self.image.get_height() - 60

    def _get_scaled_height(self):
        return int(self.image.get_height() * (POWERUP_WIDTH / self.image.get_width()))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def reset_position(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        # self.y = random.randint(0, SCREEN_HEIGHT - self.image.get_height())

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("婷婷&草莓號")
    bg = pygame.image.load('bg.png')

    player = Player('tt.png')
    coin = Coin('coins.png')
    powerup = PowerUp('powerup.png')

    font = pygame.font.Font(None, 36)
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys)

        # Collision detection
        if player.get_rect().colliderect(coin.get_rect()):
            score += 1
            coin.reset_position()

        if player.get_rect().colliderect(powerup.get_rect()):
            player.activate_powerup()
            powerup.reset_position()

        # Drawing
        screen.blit(bg, (0, 0))
        player.draw(screen)
        coin.draw(screen)
        powerup.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()
